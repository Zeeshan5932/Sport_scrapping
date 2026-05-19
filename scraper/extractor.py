# scraper/extractor.py

import asyncio
import json
import os
from datetime import datetime
from config import SAVE_DIR


class Extractor:

    def __init__(self, page):

        self.page = page

    async def scrape_all_panels(self):

        all_data = []

        # ALL TOURNAMENT PANELS
        panels = await self.page.query_selector_all(
            ".sr-accordion__item"
        )

        print(f"\n🏆 TOTAL PANELS FOUND: {len(panels)}")

        for panel_index, panel in enumerate(panels):

            try:

                print("\n" + "=" * 60)
                print(f"📂 PANEL {panel_index + 1}")
                print("=" * 60)

                # ==========================================
                # TOURNAMENT NAME
                # ==========================================

                tournament_name = "Unknown Tournament"

                title_el = await panel.query_selector(
                    ".sr-accordion__head"
                )

                if title_el:

                    tournament_name = (
                        await title_el.inner_text()
                    ).strip()

                print(f"\n🏏 TOURNAMENT: {tournament_name}")

                # ==========================================
                # OPEN PANEL
                # ==========================================

                if title_el:

                    await title_el.click()

                    print("✅ Panel Opened")

                    await asyncio.sleep(2)

                # ==========================================
                # FIND MATCHES
                # ==========================================

                matches = await panel.query_selector_all(
                    ".sr-simcrick-scb__wrapper"
                )

                print(f"\n🎯 MATCHES FOUND: {len(matches)}")

                panel_matches = []

                for match_index, match in enumerate(matches):

                    try:

                        print("\n" + "-" * 50)
                        print(f"MATCH {match_index + 1}")
                        print("-" * 50)

                        # ==================================
                        # TEAMS
                        # ==================================

                        teams = await match.query_selector_all(
                            ".sr-simcrick-scb__team-name"
                        )

                        teamA = (
                            await teams[0].inner_text()
                            if len(teams) > 0 else None
                        )

                        teamB = (
                            await teams[1].inner_text()
                            if len(teams) > 1 else None
                        )

                        # ==================================
                        # SCORES
                        # ==================================

                        scores = await match.query_selector_all(
                            ".sr-simcrick-scb__result"
                        )

                        scoreA = (
                            await scores[0].inner_text()
                            if len(scores) > 0 else None
                        )

                        scoreB = (
                            await scores[1].inner_text()
                            if len(scores) > 1 else None
                        )

                        # ==================================
                        # EXTRA
                        # ==================================

                        extras = await match.query_selector_all(
                            ".sr-simcrick-scb__extra"
                        )

                        rrA = (
                            await extras[0].inner_text()
                            if len(extras) > 0 else None
                        )

                        rrB = (
                            await extras[1].inner_text()
                            if len(extras) > 1 else None
                        )

                        # ==================================
                        # STATUS
                        # ==================================

                        status = None

                        status_el = await match.query_selector(
                            ".sr-simcrick-scb__status"
                        )

                        if status_el:

                            status = (
                                await status_el.inner_text()
                            ).strip()

                        # ==================================
                        # COMMENT
                        # ==================================

                        comment = None

                        comment_el = await match.query_selector(
                            ".sr-simcrick-scb__comment"
                        )

                        if comment_el:

                            comment = (
                                await comment_el.inner_text()
                            ).strip()

                        # ==================================
                        # MATCH DATA
                        # ==================================

                        match_data = {

                            "teamA": teamA,
                            "scoreA": scoreA,
                            "rrA": rrA,

                            "teamB": teamB,
                            "scoreB": scoreB,
                            "rrB": rrB,

                            "status": status,
                            "comment": comment
                        }

                        print(match_data)

                        panel_matches.append(match_data)

                    except Exception as e:

                        print(f"\n❌ Match Error: {e}")

                # ==========================================
                # SAVE TOURNAMENT DATA
                # ==========================================

                tournament_data = {

                    "tournament": tournament_name,

                    "matches": panel_matches
                }

                all_data.append(tournament_data)

                # ==========================================
                # CLOSE PANEL
                # ==========================================

                if title_el:

                    await title_el.click()

                    await asyncio.sleep(1)

            except Exception as e:

                print(f"\n❌ Panel Error: {e}")

        return all_data

    async def save_data(self, data):

        os.makedirs(SAVE_DIR, exist_ok=True)

        filename = datetime.now().strftime("%Y-%m-%d") + ".json"

        filepath = os.path.join(
            SAVE_DIR,
            filename
        )

        with open(filepath, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"\n✅ DATA SAVED: {filepath}")