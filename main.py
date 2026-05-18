import asyncio
from scraper.browser import Browser
from scraper.navigation import Navigator
from scraper.extractor import Extractor
from scraper.live import LiveScraper

async def main():
    browser = Browser()
    page = await browser.start()

    navigator = Navigator(page)
    await navigator.open_site()
    await navigator.click_ipl()
    await navigator.open_match()

    extractor = Extractor(page)
    live = LiveScraper(extractor)

    await live.start()

    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())