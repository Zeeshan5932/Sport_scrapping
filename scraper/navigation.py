import asyncio
from config import URL, SELECTORS

class Navigator:
    def __init__(self, page):
        self.page = page

    async def open_site(self):
        await self.page.goto(URL, wait_until="networkidle")
        await asyncio.sleep(5)

    async def click_ipl(self):
        await self.page.click(SELECTORS["ipl"])
        await asyncio.sleep(3)

    async def open_match(self):
        await self.page.click(SELECTORS["match_card"])
        await asyncio.sleep(3)