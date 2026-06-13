import logging
import re
from datetime import datetime

from utils.match_utils import is_match_live


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
            "innings":        [],
            "scorecard":      []
        }

        # ─── FOR LIVE MATCHES: Return early without opening scorecard ──
        if is_match_live(basic["status"]):
            return match_data

        # ─── FOR ENDED MATCHES: Open scorecard and scrape details ──

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

            tab_name = (
                (await tab_name_el.inner_text()).strip().replace('\xa0', ' ')
                if tab_name_el
                else f"Innings {tab_idx + 1}"
            )

            is_active = await tabs[tab_idx].evaluate("el => el.classList.contains('srm-is-active')")

            if not is_active:
                await tabs[tab_idx].click()
                await page.wait_for_timeout(1200)

            innings_data = await extract_innings_data(page, tab_name)

            match_data["innings"].append(innings_data)
            match_data["scorecard"].append(innings_data)

            logging.info(
                f"       {tab_name}: "
                f"{len(innings_data.get('batting', []))} batters | "
                f"{len(innings_data.get('bowling', []))} bowlers"
            )

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
                                [...text.matchAll(/(b|lb|nb|w):\\s*(\\d+)/g)].forEach(m => extras[m[1]] = m[2]);
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