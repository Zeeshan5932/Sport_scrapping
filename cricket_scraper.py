# """
# Cricket LMT - Daily Scheduled Scraper (WORKING FIX)
# headless=False + stealth mode — site real browser chahti hai
# Window background mein chalta hai, minimize hoga automatically
# """

# import asyncio
# import json
# import re
# import os
# import logging
# import schedule
# import time
# from datetime import datetime
# from playwright.async_api import async_playwright


# # ─── CONFIG ───────────────────────────────────────────────
# TARGET_URL   = "https://sportcenter.sir.sportradar.com/cricket-lmt"
# RUN_TIME     = "08:00"
# DATA_FOLDER  = "data"
# LOG_FOLDER   = "logs"
# # ──────────────────────────────────────────────────────────


# def setup_logging():
#     os.makedirs(LOG_FOLDER, exist_ok=True)
#     os.makedirs(DATA_FOLDER, exist_ok=True)
#     log_file = os.path.join(LOG_FOLDER, "scraper.log")
#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s [%(levelname)s] %(message)s",
#         handlers=[
#             logging.FileHandler(log_file, encoding="utf-8"),
#             logging.StreamHandler()
#         ]
#     )


# def get_output_path():
#     today = datetime.now().strftime("%Y-%m-%d")
#     return os.path.join(DATA_FOLDER, f"cricket_{today}.json")


# async def scrape_cricket_lmt():
#     today = datetime.now().strftime("%Y-%m-%d")
#     output_file = get_output_path()

#     logging.info("══════════════════════════════════════")
#     logging.info(f"  Scraping started for date: {today}")
#     logging.info("══════════════════════════════════════")

#     all_tournaments = []

#     async with async_playwright() as p:
#         # headless=False — real browser, site isko properly render karta hai
#         browser = await p.chromium.launch(
#             headless=False,
#             args=[
#                 "--window-size=1400,900",
#                 "--window-position=0,0",
#                 "--disable-blink-features=AutomationControlled",
#                 "--no-sandbox",
#             ]
#         )

#         context = await browser.new_context(
#             viewport={"width": 1400, "height": 900},
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
#         )

#         # Automation detect hone se bachao
#         await context.add_init_script("""
#             Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
#         """)

#         page = await context.new_page()

#         try:
#             logging.info(f"Opening: {TARGET_URL}")
#             await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)

#             # Team name appear hone tak wait karo — max 60 sec
#             logging.info("Waiting for match data...")
#             await page.wait_for_selector(
#                 ".sr-simcrick-scb__team-name",
#                 timeout=60000,
#                 state="visible"
#             )
#             logging.info("✓ Match data loaded!")

#             # Thoda aur wait — baaki matches bhi load hon
#             await page.wait_for_timeout(3000)

#             # JS se sara data ek baar mein extract karo
#             tournaments_data = await page.evaluate("""
#                 () => {
#                     const results = [];
#                     const wrappers = document.querySelectorAll('.d-cricket-lmt__cricket_wrapper');

#                     wrappers.forEach((wrapper, wIdx) => {
#                         const tObj = {
#                             tournament_index: wIdx + 1,
#                             tournament_name: '',
#                             matches: []
#                         };

#                         const leagueEl = wrapper.querySelector('.d-cricket-lmt__cricket_league');
#                         if (leagueEl) tObj.tournament_name = leagueEl.textContent.trim();

#                         const matchEls = wrapper.querySelectorAll('.sr-simcrick-scb__wrapper');
#                         matchEls.forEach((matchEl, mIdx) => {
#                             const match = { match_index: mIdx + 1 };

#                             // Teams
#                             const teamNames = matchEl.querySelectorAll('.sr-simcrick-scb__team-name');
#                             if (teamNames.length >= 2) {
#                                 match.home_team = teamNames[0].textContent.trim();
#                                 match.away_team = teamNames[1].textContent.trim();
#                             } else if (teamNames.length === 1) {
#                                 match.home_team = teamNames[0].textContent.trim();
#                             }

#                             // Scores
#                             const scoreEls = [...matchEl.querySelectorAll('.sr-simcrick-scb__result')]
#                                 .map(el => el.textContent.trim())
#                                 .filter(s => s && s !== ':');
#                             if (scoreEls.length >= 2) {
#                                 match.home_score = scoreEls[0];
#                                 match.away_score = scoreEls[1];
#                             } else if (scoreEls.length === 1) {
#                                 match.home_score = scoreEls[0];
#                             }

#                             // Run rates
#                             const teamWrappers = matchEl.querySelectorAll('.sr-simcrick-scb__team-wrapper');
#                             const runRates = [];
#                             teamWrappers.forEach(tw => {
#                                 const rrVal = tw.querySelector('.sr-simcrick-scb__extra-value');
#                                 let label = 'RR';
#                                 tw.querySelectorAll('.sr-simcrick-scb__extra span').forEach(sp => {
#                                     const t = sp.textContent.trim();
#                                     if (['RR','CRR','RRR'].includes(t)) label = t;
#                                 });
#                                 if (rrVal) runRates.push({
#                                     value: rrVal.textContent.replace(/\u00a0/g, '').trim(),
#                                     label
#                                 });
#                             });
#                             if (runRates.length >= 2) {
#                                 match.home_run_rate = runRates[0].value;
#                                 match.home_rr_type  = runRates[0].label;
#                                 match.away_run_rate = runRates[1].value;
#                                 match.away_rr_type  = runRates[1].label;
#                             } else if (runRates.length === 1) {
#                                 match.home_run_rate = runRates[0].value;
#                                 match.home_rr_type  = runRates[0].label;
#                             }

#                             // Status
#                             const statusEl = matchEl.querySelector('.sr-simcrick-scb__status');
#                             if (statusEl) {
#                                 const raw = statusEl.textContent.trim();
#                                 match.status = raw.replace(/Simulated match\s*[-–]\s*/g, '').trim();
#                                 match.is_simulated = raw.toLowerCase().includes('simulated');
#                             } else {
#                                 match.is_simulated = false;
#                             }

#                             // Result comment + toss + overs
#                             const commentEl = matchEl.querySelector('.sr-simcrick-scb__comment');
#                             if (commentEl) {
#                                 match.result = commentEl.textContent.trim();
#                                 const toss = match.result.match(/\(Toss:\s*([^)]+)\)/);
#                                 if (toss) match.toss_winner = toss[1].trim();
#                                 const overs = match.result.match(/after\s+([\d.]+)\s+overs/);
#                                 if (overs) match.overs_played = overs[1];
#                             }

#                             tObj.matches.push(match);
#                         });

#                         tObj.total_matches = tObj.matches.length;
#                         results.push(tObj);
#                     });

#                     return results;
#                 }
#             """)

#             for t in tournaments_data:
#                 t["date"] = today
#                 for m in t["matches"]:
#                     m["date"] = today
#                     m["tournament"] = t["tournament_name"]
#                 all_tournaments.append(t)
#                 logging.info(f"  ✓ {t['tournament_name']} — {t['total_matches']} match(es)")
#                 for m in t["matches"]:
#                     logging.info(
#                         f"    [{m['match_index']}] {m.get('home_team','?')} {m.get('home_score','?')} "
#                         f"vs {m.get('away_team','?')} {m.get('away_score','?')} | {m.get('status','?')}"
#                     )

#         except Exception as e:
#             logging.error(f"Scrape error: {e}")
#         finally:
#             await browser.close()

#     total_matches = sum(t.get("total_matches", 0) for t in all_tournaments)

#     output = {
#         "date":              today,
#         "scraped_at":        datetime.now().isoformat(),
#         "source":            TARGET_URL,
#         "total_tournaments": len(all_tournaments),
#         "total_matches":     total_matches,
#         "tournaments":       all_tournaments
#     }

#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(output, f, ensure_ascii=False, indent=2)

#     logging.info(f"✅ {total_matches} matches across {len(all_tournaments)} tournaments → {output_file}")
#     return output


# def run_scraper():
#     asyncio.run(scrape_cricket_lmt())


# def start_scheduler():
#     setup_logging()
#     logging.info(f"🕐 Scheduler started — daily run at {RUN_TIME}")
#     logging.info(f"   Data folder : {os.path.abspath(DATA_FOLDER)}")
#     logging.info(f"   Log folder  : {os.path.abspath(LOG_FOLDER)}")
#     logging.info(f"   Press Ctrl+C to stop\n")

#     logging.info("Running immediately on startup...")
#     run_scraper()

#     schedule.every().day.at(RUN_TIME).do(run_scraper)

#     while True:
#         schedule.run_pending()
#         time.sleep(30)


# if __name__ == "__main__":
#     start_scheduler()




"""
CRICKET LIVE MATCH TRACKER
REAL-TIME LIVE SCRAPER
Updates every 60 seconds
"""

import asyncio
import json
import os
import logging
import time
from datetime import datetime

from playwright.async_api import async_playwright


# =========================================================
# CONFIG
# =========================================================

TARGET_URL = "https://sportcenter.sir.sportradar.com/cricket-lmt"

UPDATE_INTERVAL = 60

DATA_FOLDER = "data"

LOG_FOLDER = "logs"


# =========================================================
# SETUP
# =========================================================

def setup_logging():

    os.makedirs(LOG_FOLDER, exist_ok=True)

    os.makedirs(DATA_FOLDER, exist_ok=True)

    log_file = os.path.join(
        LOG_FOLDER,
        "scraper.log"
    )

    logging.basicConfig(
        level=logging.INFO,

        format="%(asctime)s [%(levelname)s] %(message)s",

        handlers=[

            logging.FileHandler(
                log_file,
                encoding="utf-8"
            ),

            logging.StreamHandler()
        ]
    )


# =========================================================
# OUTPUT PATH
# =========================================================

def get_output_path():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    return os.path.join(
        DATA_FOLDER,
        f"cricket_{today}.json"
    )


# =========================================================
# SCRAPER
# =========================================================

async def scrape_cricket_lmt():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    output_file = get_output_path()

    logging.info("══════════════════════════════════════")
    logging.info(f"🚀 LIVE SCRAPING STARTED")
    logging.info(f"📅 DATE: {today}")
    logging.info("══════════════════════════════════════")

    all_tournaments = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(

            headless=False,

            args=[

                "--window-size=1400,900",

                "--window-position=0,0",

                "--disable-blink-features=AutomationControlled",

                "--no-sandbox",
            ]
        )

        context = await browser.new_context(

            viewport={
                "width": 1400,
                "height": 900
            },

            user_agent=(
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/124.0.0.0 "
                "Safari/537.36"
            )
        )

        # REMOVE AUTOMATION DETECTION
        await context.add_init_script("""

            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get: () => undefined
                }
            );

        """)

        page = await context.new_page()

        try:

            # =================================================
            # OPEN WEBSITE
            # =================================================

            logging.info(
                f"🌐 Opening: {TARGET_URL}"
            )

            await page.goto(
                TARGET_URL,

                wait_until="domcontentloaded",

                timeout=60000
            )

            # =================================================
            # WAIT FOR DATA
            # =================================================

            logging.info(
                "⏳ Waiting for matches..."
            )

            await page.wait_for_selector(

                ".sr-simcrick-scb__team-name",

                timeout=60000,

                state="visible"
            )

            logging.info(
                "✅ Match data loaded"
            )

            await page.wait_for_timeout(5000)

            # =================================================
            # SCRAPE ALL DATA
            # =================================================

            tournaments_data = await page.evaluate("""

                () => {

                    const results = [];

                    const wrappers = document.querySelectorAll(
                        '.d-cricket-lmt__cricket_wrapper'
                    );

                    wrappers.forEach((wrapper, wIdx) => {

                        const tournament = {

                            tournament_index: wIdx + 1,

                            tournament_name: '',

                            total_matches: 0,

                            matches: []
                        };

                        // =====================================
                        // TOURNAMENT NAME
                        // =====================================

                        const leagueEl = wrapper.querySelector(
                            '.d-cricket-lmt__cricket_league'
                        );

                        if (leagueEl) {

                            tournament.tournament_name =
                                leagueEl.textContent.trim();
                        }

                        // =====================================
                        // MATCH PANELS
                        // =====================================

                        const matchEls = wrapper.querySelectorAll(
                            '.sr-simcrick-scb__wrapper'
                        );

                        matchEls.forEach((matchEl, mIdx) => {

                            const match = {

                                match_index: mIdx + 1,

                                scraped_at:
                                    new Date().toISOString()
                            };

                            // =================================
                            // TEAM NAMES
                            // =================================

                            const teamNames =
                                matchEl.querySelectorAll(
                                    '.sr-simcrick-scb__team-name'
                                );

                            if (teamNames.length >= 2) {

                                match.home_team =
                                    teamNames[0]
                                    .textContent
                                    .trim();

                                match.away_team =
                                    teamNames[1]
                                    .textContent
                                    .trim();
                            }

                            // =================================
                            // SCORES
                            // =================================

                            const scoreEls =
                                [...matchEl.querySelectorAll(
                                    '.sr-simcrick-scb__result'
                                )]

                                .map(el =>
                                    el.textContent.trim()
                                )

                                .filter(
                                    s => s && s !== ':'
                                );

                            if (scoreEls.length >= 2) {

                                match.home_score =
                                    scoreEls[0];

                                match.away_score =
                                    scoreEls[1];
                            }

                            // =================================
                            // STATUS
                            // =================================

                            const statusEl =
                                matchEl.querySelector(
                                    '.sr-simcrick-scb__status'
                                );

                            if (statusEl) {

                                match.status =
                                    statusEl.textContent
                                    .trim();
                            }

                            // =================================
                            // COMMENT
                            // =================================

                            const commentEl =
                                matchEl.querySelector(
                                    '.sr-simcrick-scb__comment'
                                );

                            if (commentEl) {

                                match.comment =
                                    commentEl.textContent
                                    .trim();
                            }

                            // =================================
                            // MATCH ID
                            // =================================

                            const titleAttr =
                                statusEl?.getAttribute(
                                    'title'
                                );

                            if (titleAttr) {

                                match.match_id =
                                    titleAttr;
                            }

                            tournament.matches.push(
                                match
                            );
                        });

                        tournament.total_matches =
                            tournament.matches.length;

                        results.push(tournament);
                    });

                    return results;
                }

            """)

            # =================================================
            # LOGGING
            # =================================================

            for tournament in tournaments_data:

                tournament["date"] = today

                all_tournaments.append(
                    tournament
                )

                logging.info(
                    f"🏏 "
                    f"{tournament['tournament_name']} "
                    f"→ "
                    f"{tournament['total_matches']} matches"
                )

                for match in tournament["matches"]:

                    logging.info(

                        f"   "
                        f"{match.get('home_team','?')} "
                        f"{match.get('home_score','')} "

                        f"vs "

                        f"{match.get('away_team','?')} "
                        f"{match.get('away_score','')} "

                        f"| "

                        f"{match.get('status','')}"
                    )

        except Exception as e:

            logging.error(f"❌ ERROR: {e}")

        finally:

            await browser.close()

    # =========================================================
    # FINAL JSON
    # =========================================================

    total_matches = sum(
        t["total_matches"]
        for t in all_tournaments
    )

    output = {

        "live_update": True,

        "date": today,

        "scraped_at":
            datetime.now().isoformat(),

        "source": TARGET_URL,

        "total_tournaments":
            len(all_tournaments),

        "total_matches":
            total_matches,

        "tournaments":
            all_tournaments
    }

    # =========================================================
    # SAVE JSON
    # =========================================================

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )

    logging.info(
        f"💾 UPDATED: {output_file}"
    )


# =========================================================
# RUN
# =========================================================

def run_scraper():

    asyncio.run(
        scrape_cricket_lmt()
    )


# =========================================================
# LIVE LOOP
# =========================================================

def start_live_scraper():

    setup_logging()

    logging.info("══════════════════════════════════════")
    logging.info("🔥 LIVE CRICKET SCRAPER STARTED")
    logging.info("══════════════════════════════════════")

    logging.info(
        f"⏱ Updating every "
        f"{UPDATE_INTERVAL} seconds"
    )

    while True:

        try:

            run_scraper()

            logging.info(
                f"\n⏳ Waiting "
                f"{UPDATE_INTERVAL} sec...\n"
            )

            time.sleep(
                UPDATE_INTERVAL
            )

        except KeyboardInterrupt:

            logging.info(
                "\n🛑 SCRAPER STOPPED"
            )

            break

        except Exception as e:

            logging.error(
                f"\n❌ LOOP ERROR: {e}"
            )

            time.sleep(10)


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    start_live_scraper()