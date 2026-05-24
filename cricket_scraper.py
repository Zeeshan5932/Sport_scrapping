"""
Cricket LMT - Smart Live Scraper
- Ended match → ek baar scrape, done
- Live match  → har 60 sec baad update
- Har match scrape hote hi → turant save
"""

import asyncio
import json
import os
import logging
import time
from datetime import datetime
from playwright.async_api import async_playwright

# ─── CONFIG ───────────────────────────────────────────────
TARGET_URL     = "https://sportcenter.sir.sportradar.com/cricket-lmt"
LIVE_INTERVAL  = 60       # seconds — live match update interval
DATA_FOLDER    = "data"
LOG_FOLDER     = "logs"
# ──────────────────────────────────────────────────────────

def setup_logging():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    os.makedirs(DATA_FOLDER, exist_ok=True)
    log_file = os.path.join(LOG_FOLDER, "scraper.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def get_output_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DATA_FOLDER, f"cricket_{today}.json")

def load_existing_data(output_file):
    """Existing JSON load karo — taake ended matches dobara scrape na hon."""
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def save_data(output_file, data):
    """Turant save karo."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_match_live(status: str) -> bool:
    """Status se pata karo match live hai ya nahi."""
    if not status:
        return False
    s = status.lower().strip()
    ended_keywords = ["ended", "finished", "complete", "abandoned", "no result"]
    for kw in ended_keywords:
        if kw in s:
            return False
    return True  # INN 1, INN 2, Live, In Progress etc. = live

def build_match_key(tournament_name: str, home_team: str, away_team: str) -> str:
    return f"{tournament_name}|{home_team}|{away_team}"

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
                key = build_match_key(t["tournament_name"], m.get("home_team",""), m.get("away_team",""))
                ended_keys.add(key)

    if ended_keys:
        logging.info(f"  {len(ended_keys)} already-ended match(es) loaded from file — will skip re-scraping")

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
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
            logging.info("Waiting for matches to load...")
            await page.wait_for_selector(".sr-simcrick-scb__team-name", timeout=60000, state="visible")
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
                    await page.wait_for_selector(".sr-simcrick-scb__team-name", timeout=60000, state="visible")
                    await page.wait_for_timeout(3000)

                # Page refresh — latest live scores aane ke liye
                try:
                    await page.reload(wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_selector(".sr-simcrick-scb__team-name", timeout=30000, state="visible")
                    await page.wait_for_timeout(2000)
                except Exception as e:
                    logging.warning(f"Page reload issue: {e} — continuing with current page")

                # Tournaments dhoondo
                tournament_count = await page.evaluate(
                    "() => document.querySelectorAll('.d-cricket-lmt__cricket_wrapper').length"
                )

                new_tournaments = []

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
                        (t for t in master["tournaments"] if t["tournament_name"] == tournament_name),
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

                        match_key = build_match_key(tournament_name, basic["home_team"], basic["away_team"])

                        # ── ENDED MATCH — skip if already scraped ──
                        if match_key in ended_keys:
                            logging.info(f"  [{m_idx+1}] SKIP (ended): {basic['home_team']} vs {basic['away_team']}")
                            continue

                        # ── SCRAPE THIS MATCH ──
                        logging.info(f"  [{m_idx+1}] {'LIVE' if is_match_live(basic['status']) else 'NEW'}: {basic['home_team']} {basic['home_score']} vs {basic['away_team']} {basic['away_score']} | {basic['status']}")

                        match_data = await scrape_single_match(page, t_idx, m_idx, today, tournament_name, basic)

                        if match_data:
                            # Master mein update ya insert
                            existing_idx = next(
                                (i for i, m in enumerate(t_master["matches"])
                                 if build_match_key(tournament_name, m.get("home_team",""), m.get("away_team","")) == match_key),
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
                            master["total_matches"]     = sum(t["total_matches"] for t in master["tournaments"])
                            save_data(output_file, master)
                            logging.info(f"       SAVED → {output_file}")

                            # Agar ended ho gaya → ended set mein add karo
                            if not is_match_live(match_data.get("status", "")):
                                ended_keys.add(match_key)
                                logging.info(f"       Match ended — will not re-scrape")

                # ── WAIT BEFORE NEXT LOOP ──
                elapsed  = time.time() - loop_start
                wait_sec = max(0, LIVE_INTERVAL - elapsed)

                live_count   = sum(
                    1 for t in master["tournaments"]
                    for m in t["matches"]
                    if is_match_live(m.get("status",""))
                )
                ended_count  = len(ended_keys)

                if live_count > 0:
                    logging.info(f"\n  Live: {live_count} | Ended: {ended_count} | Next update in {wait_sec:.0f}s...\n")
                    await asyncio.sleep(wait_sec)
                else:
                    logging.info(f"\n  No live matches. Checking again in {LIVE_INTERVAL}s...\n")
                    await asyncio.sleep(LIVE_INTERVAL)

        except KeyboardInterrupt:
            logging.info("\nScraper stopped by user.")
        except Exception as e:
            logging.error(f"Loop error: {e}")
            import traceback
            logging.error(traceback.format_exc())
        finally:
            await browser.close()


# ─── BASIC INFO (no click needed) ─────────────────────────

async def get_basic_match_info(page, t_idx, m_idx):
    try:
        return await page.evaluate(f"""
            () => {{
                const wrapper  = document.querySelectorAll('.d-cricket-lmt__cricket_wrapper')[{t_idx}];
                const matchEl  = wrapper.querySelectorAll('.sr-simcrick-scb__wrapper')[{m_idx}];
                const teams    = [...matchEl.querySelectorAll('.sr-simcrick-scb__team-name')].map(el => el.textContent.trim());
                const scores   = [...matchEl.querySelectorAll('.sr-simcrick-scb__result')].map(el => el.textContent.trim()).filter(s => s && s !== ':');
                const statusEl = matchEl.querySelector('.sr-simcrick-scb__status');
                const commentEl= matchEl.querySelector('.sr-simcrick-scb__comment');

                const teamWrappers = matchEl.querySelectorAll('.sr-simcrick-scb__team-wrapper');
                const runRates = [];
                teamWrappers.forEach(tw => {{
                    const rrVal = tw.querySelector('.sr-simcrick-scb__extra-value');
                    let label = 'RR';
                    tw.querySelectorAll('.sr-simcrick-scb__extra span').forEach(sp => {{
                        const t = sp.textContent.trim();
                        if (['RR','CRR','RRR'].includes(t)) label = t;
                    }});
                    if (rrVal) runRates.push({{ value: rrVal.textContent.replace(/\u00a0/g,'').trim(), label }});
                }});

                const rawStatus = statusEl?.textContent.trim() || '';
                return {{
                    home_team:     teams[0] || '',
                    away_team:     teams[1] || '',
                    home_score:    scores[0] || '',
                    away_score:    scores[1] || '',
                    home_run_rate: runRates[0]?.value || '',
                    home_rr_type:  runRates[0]?.label || 'RR',
                    away_run_rate: runRates[1]?.value || '',
                    away_rr_type:  runRates[1]?.label || 'RR',
                    status:        rawStatus.replace(/Simulated match\\s*[-]\\s*/g,'').trim(),
                    is_simulated:  rawStatus.toLowerCase().includes('simulated'),
                    result:        commentEl?.textContent.trim() || '',
                    match_id:      statusEl?.getAttribute('title') || ''
                }};
            }}
        """)
    except Exception as e:
        logging.warning(f"get_basic_match_info error: {e}")
        return None


# ─── SINGLE MATCH FULL SCRAPE ─────────────────────────────

async def scrape_single_match(page, t_idx, m_idx, today, tournament_name, basic):
    try:
        import re
        toss_winner = ""
        if basic.get("result"):
            t = re.search(r'\(Toss:\s*([^)]+)\)', basic["result"])
            if t:
                toss_winner = t.group(1).strip()

        match_data = {
            "match_index":    m_idx + 1,
            "date":           today,
            "last_updated":   datetime.now().isoformat(),
            "tournament":     tournament_name,
            "match_id":       basic.get("match_id", ""),
            "home_team":      basic["home_team"],
            "away_team":      basic["away_team"],
            "home_score":     basic["home_score"],
            "away_score":     basic["away_score"],
            "home_run_rate":  basic["home_run_rate"],
            "home_rr_type":   basic["home_rr_type"],
            "away_run_rate":  basic["away_run_rate"],
            "away_rr_type":   basic["away_rr_type"],
            "status":         basic["status"],
            "is_simulated":   basic["is_simulated"],
            "result":         basic["result"],
            "toss_winner":    toss_winner,
            "innings":        []
        }

        # Panel click → scorecard open
        await page.evaluate(f"""
            () => {{
                const wrapper = document.querySelectorAll('.d-cricket-lmt__cricket_wrapper')[{t_idx}];
                const matchEl = wrapper.querySelectorAll('.sr-simcrick-scb__wrapper')[{m_idx}];
                if (matchEl) matchEl.click();
            }}
        """)

        try:
            await page.wait_for_selector(".sr-simcrick-scc__wrapper", timeout=15000, state="visible")
            await page.wait_for_timeout(1500)
        except Exception:
            logging.warning(f"       Scorecard did not open")
            return match_data

        # Innings tabs
        tabs = await page.query_selector_all(".sr-simcrick-scc__tab")

        for tab_idx in range(len(tabs)):
            tabs = await page.query_selector_all(".sr-simcrick-scc__tab")
            if tab_idx >= len(tabs):
                break

            tab_name_el = await tabs[tab_idx].query_selector(".sr-simcrick-scc__inning-name")
            tab_name    = (await tab_name_el.inner_text()).strip().replace('\xa0', ' ') if tab_name_el else f"Innings {tab_idx+1}"
            is_active   = await tabs[tab_idx].evaluate("el => el.classList.contains('srm-is-active')")

            if not is_active:
                await tabs[tab_idx].click()
                await page.wait_for_timeout(1200)

            innings_data = await extract_innings_data(page, tab_name)
            match_data["innings"].append(innings_data)
            logging.info(f"       {tab_name}: {len(innings_data.get('batting',[]))} batters | {len(innings_data.get('bowling',[]))} bowlers")

        # Panel close
        await page.evaluate(f"""
            () => {{
                const wrapper = document.querySelectorAll('.d-cricket-lmt__cricket_wrapper')[{t_idx}];
                const matchEl = wrapper.querySelectorAll('.sr-simcrick-scb__wrapper')[{m_idx}];
                if (matchEl) matchEl.click();
            }}
        """)
        await page.wait_for_timeout(800)

        return match_data

    except Exception as e:
        logging.warning(f"scrape_single_match error: {e}")
        return None


# ─── INNINGS EXTRACTOR ────────────────────────────────────

async def extract_innings_data(page, innings_name):
    innings = {
        "innings_name":    innings_name,
        "batting":         [],
        "bowling":         [],
        "extras":          {},
        "total":           "",
        "total_detail":    "",
        "fall_of_wickets": ""
    }
    try:
        data = await page.evaluate("""
            () => {
                const scc = document.querySelector('.sr-simcrick-scc__wrapper');
                if (!scc) return null;
                const tables = scc.querySelectorAll('.sr-simcrick-scc__table');
                const result = { batting: [], bowling: [], extras: {}, total: '', total_detail: '', fall_of_wickets: '' };

                // BATTING
                const battingTable = tables[0];
                if (battingTable) {
                    let currentBatter = null;
                    battingTable.querySelectorAll('tbody tr').forEach(row => {
                        const cells = row.querySelectorAll('td');
                        if (cells.length === 6) {
                            const nameRaw = cells[0].textContent.trim();
                            if (nameRaw === 'Extras') {
                                result.extras.runs = cells[1].textContent.trim();
                                return;
                            }
                            if (cells[0].querySelector('.srt-base-1-primary-1')) {
                                result.total = cells[1].textContent.trim();
                                return;
                            }
                            currentBatter = {
                                name:      nameRaw,
                                runs:      cells[1].textContent.trim(),
                                balls:     cells[2].textContent.trim(),
                                fours:     cells[3].textContent.trim(),
                                sixes:     cells[4].textContent.trim(),
                                sr:        cells[5].textContent.trim(),
                                dismissal: ''
                            };
                            result.batting.push(currentBatter);
                        } else if (cells.length === 1) {
                            const cell = cells[0];
                            const text = cell.textContent.trim();
                            const isMeta = cell.classList.contains('srt-base-6');
                            if (isMeta && (text.includes('lb') || text.includes('nb'))) {
                                const extras = {};
                                [...text.matchAll(/(b|lb|nb|w):\s*(\d+)/g)].forEach(m => extras[m[1]] = m[2]);
                                result.extras.detail = extras;
                            } else if (isMeta && (text.includes('Over') || text.includes('RR'))) {
                                result.total_detail = text;
                            } else if (currentBatter && !isMeta) {
                                currentBatter.dismissal = text;
                            }
                        }
                    });
                }

                // BOWLING
                const bowlingTable = tables[1];
                if (bowlingTable) {
                    bowlingTable.querySelectorAll('tbody tr').forEach(row => {
                        const cells = row.querySelectorAll('td');
                        if (cells.length >= 5) {
                            result.bowling.push({
                                name:    cells[0].textContent.trim(),
                                overs:   cells[1].textContent.trim(),
                                maidens: cells[2].textContent.trim(),
                                runs:    cells[3].textContent.trim(),
                                wickets: cells[4].textContent.trim(),
                                econ:    cells[5]?.textContent.trim() || ''
                            });
                        }
                    });
                }

                // FALL OF WICKETS
                const fowEl = scc.querySelector('.sr-simcrick-scc__fall-of-wickets');
                if (fowEl) {
                    result.fall_of_wickets = fowEl.textContent.replace('Fall of wickets','').replace('|','').trim();
                }
                return result;
            }
        """)
        if data:
            innings["batting"]         = data.get("batting", [])
            innings["bowling"]         = data.get("bowling", [])
            innings["extras"]          = data.get("extras", {})
            innings["total"]           = data.get("total", "")
            innings["total_detail"]    = data.get("total_detail", "")
            innings["fall_of_wickets"] = data.get("fall_of_wickets", "")
    except Exception as e:
        logging.warning(f"extract_innings_data error: {e}")
    return innings


# ─── ENTRY POINT ──────────────────────────────────────────

if __name__ == "__main__":
    setup_logging()
    asyncio.run(run_live_scraper())