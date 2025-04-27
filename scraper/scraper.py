import json
import asyncio
from playwright.async_api import async_playwright

async def scrape():
    url = "https://1wywg.com/v3/3991/landing-betting-india?lang=en&bonus=hi&subid=%7Bsub1%7D&payout=%7Bamount%7D&p=zgpn&sub1=14t2n34f8hpef"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        prematch_data = []
        live_data = []

        # These selectors depend on real inspection
        prematch_selector = 'div[class*="prematch"] table'
        live_selector = 'div[class*="live"] table'

        try:
            prematch_table = await page.query_selector(prematch_selector)
            if prematch_table:
                rows = await prematch_table.query_selector_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = await row.query_selector_all('td')
                    data = [await col.inner_text() for col in cols]
                    prematch_data.append(data)

        except Exception as e:
            print("Prematch table not found:", e)

        try:
            live_table = await page.query_selector(live_selector)
            if live_table:
                rows = await live_table.query_selector_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = await row.query_selector_all('td')
                    data = [await col.inner_text() for col in cols]
                    live_data.append(data)

        except Exception as e:
            print("Live match table not found:", e)

        await browser.close()

        # Save to JSON inside docs/
        with open('docs/prematch.json', 'w') as f:
            json.dump(prematch_data, f, indent=4)

        with open('docs/live.json', 'w') as f:
            json.dump(live_data, f, indent=4)

        print("Scraping complete.")

if __name__ == "__main__":
    asyncio.run(scrape())
