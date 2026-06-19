import asyncio
import logging
import time
from datetime import datetime

from playwright.async_api import async_playwright

from config.settings import TARGET_URL, LIVE_INTERVAL, DATA_FOLDER
from utils.storage import get_output_path, load_existing_data, save_data
import os
from utils.match_utils import is_match_live, is_match_ended, build_match_key
from scraper.extractors import get_basic_match_info, scrape_single_match


# ─── MAIN LOOP ────────────────────────────────────────────

async def run_live_scraper():
    today         = datetime.now().strftime("%Y-%m-%d")
    output_file   = get_output_path()

    logging.info("══════════════════════════════════════")
    logging.info(f"  SMART LIVE SCRAPER — {today}")
    logging.info(f"  Live update every {LIVE_INTERVAL}s")
    logging.info("══════════════════════════════════════")

    # Master data store — in-memory
    master = load_existing_data(output_file) or {
        "date":              today,
        "scraped_at":        datetime.now().isoformat(),
        "source":            TARGET_URL,
        "total_tournaments": 0,
        "total_matches":     0,
        "tournaments":       []
    }

    # Ended matches ka set — dobara scrape nahi karenge
    ended_keys = set()

    for t in master.get("tournaments", []):
        for m in t.get("matches", []):
            if not is_match_live(m.get("status", "")):
                key = build_match_key(
                    t["tournament_name"],
                    m.get("home_team", ""),
                    m.get("away_team", "")
                )
                ended_keys.add(key)

    if ended_keys:
        logging.info(
            f"  {len(ended_keys)} already-ended match(es) loaded from file — will skip re-scraping"
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--window-size=1400,900",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
        )

        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
        )

        await context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )

        page = await context.new_page()

        try:
            logging.info(f"Opening: {TARGET_URL}")

            await page.goto(
                TARGET_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            logging.info("Waiting for matches to load...")

            await page.wait_for_selector(
                ".sr-simcrick-scb__team-name",
                timeout=60000,
                state="visible"
            )

            await page.wait_for_timeout(3000)

            logging.info("Matches loaded! Starting scrape loop...\n")

            # ── MAIN LOOP ──────────────────────────────────
            while True:
                loop_start  = time.time()
                today       = datetime.now().strftime("%Y-%m-%d")
                output_file = get_output_path()

                # Agar date badal gayi (midnight) toh master reset
                if master.get("date") != today:
                    logging.info("New day detected — resetting data store")

                    master = {
                        "date":              today,
                        "scraped_at":        datetime.now().isoformat(),
                        "source":            TARGET_URL,
                        "total_tournaments": 0,
                        "total_matches":     0,
                        "tournaments":       []
                    }

                    ended_keys.clear()

                    await page.reload(wait_until="domcontentloaded")

                    await page.wait_for_selector(
                        ".sr-simcrick-scb__team-name",
                        timeout=60000,
                        state="visible"
                    )

                    await page.wait_for_timeout(3000)

                # Page refresh — latest live scores aane ke liye
                try:
                    await page.reload(
                        wait_until="domcontentloaded",
                        timeout=30000
                    )

                    await page.wait_for_selector(
                        ".sr-simcrick-scb__team-name",
                        timeout=30000,
                        state="visible"
                    )

                    await page.wait_for_timeout(2000)

                except Exception as e:
                    logging.warning(
                        f"Page reload issue: {e} — continuing with current page"
                    )

                # Tournaments dhoondo
                tournament_count = await page.evaluate(
                    "() => document.querySelectorAll('.d-cricket-lmt__cricket_wrapper').length"
                )

                for t_idx in range(tournament_count):
                    tournament_name = await page.evaluate(f"""
                        () => {{
                            const w = document.querySelectorAll('.d-cricket-lmt__cricket_wrapper')[{t_idx}];
                            return w?.querySelector('.d-cricket-lmt__cricket_league')?.textContent.trim() || 'Unknown';
                        }}
                    """)

                    match_count = await page.evaluate(f"""
                        () => document.querySelectorAll('.d-cricket-lmt__cricket_wrapper')[{t_idx}]
                              .querySelectorAll('.sr-simcrick-scb__wrapper').length
                    """)

                    # Find ya create tournament in master
                    t_master = next(
                        (
                            t for t in master["tournaments"]
                            if t["tournament_name"] == tournament_name
                        ),
                        None
                    )

                    if t_master is None:
                        t_master = {
                            "tournament_index": t_idx + 1,
                            "tournament_name":  tournament_name,
                            "date":             today,
                            "total_matches":    0,
                            "matches":          []
                        }

                        master["tournaments"].append(t_master)

                    for m_idx in range(match_count):
                        # Basic info pehle nikalo (click se pehle)
                        basic = await get_basic_match_info(page, t_idx, m_idx)

                        if not basic:
                            continue

                        match_key = build_match_key(
                            tournament_name,
                            basic["home_team"],
                            basic["away_team"]
                        )

                        # ── ENDED MATCH — skip if already scraped ──
                        if match_key in ended_keys:
                            logging.info(
                                f"  [{m_idx + 1}] SKIP (ended): "
                                f"{basic['home_team']} vs {basic['away_team']}"
                            )
                            continue

                        # ── SCRAPE THIS MATCH ──
                        logging.info(
                            f"  [{m_idx + 1}] "
                            f"{'LIVE' if is_match_live(basic['status']) else 'NEW'}: "
                            f"{basic['home_team']} {basic['home_score']} vs "
                            f"{basic['away_team']} {basic['away_score']} | "
                            f"{basic['status']}"
                        )

                        match_data = await scrape_single_match(
                            page,
                            t_idx,
                            m_idx,
                            today,
                            tournament_name,
                            basic
                        )

                        if match_data:
                            # Master mein update ya insert
                            existing_idx = next(
                                (
                                    i for i, m in enumerate(t_master["matches"])
                                    if build_match_key(
                                        tournament_name,
                                        m.get("home_team", ""),
                                        m.get("away_team", "")
                                    ) == match_key
                                ),
                                None
                            )

                            if existing_idx is not None:
                                t_master["matches"][existing_idx] = match_data
                            else:
                                t_master["matches"].append(match_data)

                            t_master["total_matches"] = len(t_master["matches"])

                            # ── TURANT SAVE ──
                            master["scraped_at"]        = datetime.now().isoformat()
                            master["total_tournaments"] = len(master["tournaments"])
                            master["total_matches"]     = sum(
                                t["total_matches"]
                                for t in master["tournaments"]
                            )

                            save_data(output_file, master)

                            logging.info(f"       SAVED → {output_file}")

                            # Agar ended ho gaya → ended set mein add karo
                            if is_match_ended(match_data.get("status", "")):
                                ended_keys.add(match_key)
                                scorecard_status = "scorecard captured" if match_data.get("scorecard") else "scorecard pending"
                                logging.info(f"       Match ended — {scorecard_status}, will not re-scrape")

                # ── WAIT BEFORE NEXT LOOP ──
                elapsed  = time.time() - loop_start
                wait_sec = max(0, LIVE_INTERVAL - elapsed)

                live_count = sum(
                    1 for t in master["tournaments"]
                    for m in t["matches"]
                    if is_match_live(m.get("status", ""))
                )

                ended_count = len(ended_keys)

                if live_count > 0:
                    logging.info(
                        f"\n  Live: {live_count} | Ended: {ended_count} | "
                        f"Next update in {wait_sec:.0f}s...\n"
                    )

                    await asyncio.sleep(wait_sec)

                else:
                    logging.info(
                        f"\n  No live matches. Checking again in {LIVE_INTERVAL}s...\n"
                    )

                    await asyncio.sleep(LIVE_INTERVAL)

        except KeyboardInterrupt:
            logging.info("\nScraper stopped by user.")

        except Exception as e:
            logging.error(f"Loop error: {e}")
            import traceback
            logging.error(traceback.format_exc())

        finally:
            await browser.close()


    async def scrape_date_once(target_date: str):
        """One-shot scrape for the specified date (YYYY-MM-DD). Runs a single pass and saves results."""
        output_file = os.path.join(DATA_FOLDER, f"cricket_{target_date}.json")

        logging.info(f"One-shot scraper started for {target_date}")

        master = {
            "date": target_date,
            "scraped_at": datetime.now().isoformat(),
            "source": TARGET_URL,
            "total_tournaments": 0,
            "total_matches": 0,
            "tournaments": []
        }

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox"]
            )

            context = await browser.new_context(
                viewport={"width": 1400, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
            )

            await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

            page = await context.new_page()

            try:
                await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
                await page.wait_for_selector(".sr-simcrick-scb__team-name", timeout=60000, state="visible")
                await page.wait_for_timeout(2000)

                tournament_count = await page.evaluate(
                    "() => document.querySelectorAll('.d-cricket-lmt__cricket_wrapper').length"
                )

                for t_idx in range(tournament_count):
                    tournament_name = await page.evaluate(f"""
                        () => {{
                            const w = document.querySelectorAll('.d-cricket-lmt__cricket_wrapper')[{t_idx}];
                            return w?.querySelector('.d-cricket-lmt__cricket_league')?.textContent.trim() || 'Unknown';
                        }}
                    """)

                    match_count = await page.evaluate(f"""
                        () => document.querySelectorAll('.d-cricket-lmt__cricket_wrapper')[{t_idx}]
                              .querySelectorAll('.sr-simcrick-scb__wrapper').length
                    """)

                    t_master = {
                        "tournament_index": t_idx + 1,
                        "tournament_name": tournament_name,
                        "date": target_date,
                        "total_matches": 0,
                        "matches": []
                    }

                    for m_idx in range(match_count):
                        basic = await get_basic_match_info(page, t_idx, m_idx)
                        if not basic:
                            continue

                        match_data = await scrape_single_match(page, t_idx, m_idx, target_date, tournament_name, basic)
                        if match_data:
                            t_master["matches"].append(match_data)

                    t_master["total_matches"] = len(t_master["matches"])
                    if t_master["matches"]:
                        master["tournaments"].append(t_master)

                master["total_tournaments"] = len(master["tournaments"])
                master["total_matches"] = sum(t["total_matches"] for t in master["tournaments"])

                save_data(output_file, master)
                logging.info(f"One-shot scrape saved to {output_file}")

            except Exception as e:
                logging.exception(f"One-shot scrape failed for {target_date}: {e}")

            finally:
                await browser.close()