import asyncio

from utils.logger import setup_logging
from scraper.live_scraper import run_live_scraper


if __name__ == "__main__":
    setup_logging()
    asyncio.run(run_live_scraper())