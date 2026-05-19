# scraper/navigation.py

import asyncio
from datetime import datetime


class Navigator:

    def __init__(self, page):

        self.page = page

    async def open_site(self, url):

        print("\n🌐 Opening Website...")

        await self.page.goto(
            url,
            wait_until="networkidle",
            timeout=120000
        )

        await asyncio.sleep(5)

    async def open_current_date(self):

        today = datetime.now().strftime("%d %b, %Y")

        print(f"\n📅 Searching Date: {today}")

        try:

            # ALL DATE BUTTONS
            buttons = await self.page.query_selector_all(
                ".sr-tabbednav__item"
            )

            print(f"Found {len(buttons)} date tabs")

            for btn in buttons:

                text = await btn.inner_text()

                text = text.strip()

                print(f"DATE TAB: {text}")

                if today in text:

                    print(f"\n✅ Clicking Current Date: {text}")

                    await btn.click()

                    await asyncio.sleep(3)

                    return

            print("\n⚠ Current Date Not Found")

        except Exception as e:

            print(f"\n❌ Date Error: {e}")