# scraper/scraper.py

import json
import asyncio
from playwright.async_api import async_playwright

URL = "https://1wywg.com/v3/3991/landing-betting-india?lang=en&bonus=hi&subid=%7Bsub1%7D&payout=%7Bamount%7D&p=zgpn&sub1=14t2n34f8hpef"

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, wait_until='networkidle')

        # Grab prematch
        prematch = await page.locator('div:has-text("Prematch")').all_inner_texts()

        # Grab live
        live = await page.locator('div:has-text("Live")').all_inner_texts()

        with open('docs/prematch.json', 'w', encoding='utf-8') as f:
            json.dump(prematch, f, ensure_ascii=False, indent=2)

        with open('docs/live.json', 'w', encoding='utf-8') as f:
            json.dump(live, f, ensure_ascii=False, indent=2)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape())
