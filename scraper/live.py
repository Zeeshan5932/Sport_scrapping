import asyncio

class LiveScraper:
    def __init__(self, extractor):
        self.extractor = extractor

    async def start(self):
        while True:
            data = await self.extractor.get_match_data()
            print("\n🔥 LIVE MATCH DATA")
            print(data)

            await asyncio.sleep(5)  # refresh every 5 sec