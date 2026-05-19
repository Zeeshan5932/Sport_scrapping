# scraper/live.py

import asyncio


class LiveScraper:

    def __init__(self, extractor):

        self.extractor = extractor

    async def start(self):

        while True:

            print("\n🚀 STARTING LIVE SCRAPING...\n")

            data = await self.extractor.scrape_all_panels()

            await self.extractor.save_data(data)

            print("\n⏳ WAITING 30 SECONDS...\n")

            await asyncio.sleep(30)