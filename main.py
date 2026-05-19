# main.py

import asyncio

from config import URL

from scraper.browser import Browser
from scraper.navigation import Navigator
from scraper.extractor import Extractor
from scraper.live import LiveScraper


async def main():

    browser = Browser()

    page = await browser.start()

    navigator = Navigator(page)

    # OPEN WEBSITE
    await navigator.open_site(URL)

    # OPEN TODAY DATE
    await navigator.open_current_date()

    # EXTRACTOR
    extractor = Extractor(page)

    # LIVE SCRAPER
    live = LiveScraper(extractor)

    # START LOOP
    await live.start()

    # CLOSE
    await browser.close()


if __name__ == "__main__":

    asyncio.run(main())