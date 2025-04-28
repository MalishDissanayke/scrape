# scraper/scraper.py

import asyncio
import json
from playwright.async_api import async_playwright

URL = "https://1wywg.com/v3/3991/landing-betting-india?lang=en&bonus=hi&subid={sub1}&payout={amount}&p=zgpn&sub1=14t2n34f8hpef"

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL)

        # Wait for important betting content to load
        await page.wait_for_selector('.betting-card')  # wait until match cards appear

        # Now extract all betting cards
        cards = await page.query_selector_all('.betting-card')

        prematch_data = []
        live_data = []

        for card in cards:
            try:
                status_el = await card.query_selector('.betting-card-header-status')
                match_status = await status_el.inner_text() if status_el else ''

                match_name_el = await card.query_selector('.betting-card-header')
                match_name = await match_name_el.inner_text() if match_name_el else ''

                odds_el = await card.query_selector('.betting-card-footer')
                odds_text = await odds_el.inner_text() if odds_el else ''

                match_data = {
                    "match_name": match_name.strip(),
                    "odds_info": odds_text.strip(),
                }

                if 'Live' in match_status:
                    live_data.append(match_data)
                elif 'Prematch' in match_status:
                    prematch_data.append(match_data)

            except Exception as e:
                print(f"Error parsing card: {e}")
                continue

        # Save to docs/prematch.json and docs/live.json
        with open('docs/prematch.json', 'w', encoding='utf-8') as f:
            json.dump(prematch_data, f, indent=2, ensure_ascii=False)

        with open('docs/live.json', 'w', encoding='utf-8') as f:
            json.dump(live_data, f, indent=2, ensure_ascii=False)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape())
