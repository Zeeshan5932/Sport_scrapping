from playwright.async_api import async_playwright

class Browser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()
        return self.page

    async def close(self):
        await self.browser.close()
        await self.playwright.stop()