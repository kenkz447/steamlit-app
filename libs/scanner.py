import asyncio
import sys

from playwright.sync_api import sync_playwright, Playwright

if 'win32' in sys.platform:
    # Windows specific event-loop policy & cmd
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

class ScannerProfile:
    url: str
    fields: dict

def run(playwright: Playwright, profile: ScannerProfile):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.goto(profile.url)
    
    result = {}
    for field in profile.fields:
        result[field] = page.query_selector(profile.fields[field]).inner_text()

    browser.close()
    return result
    

def run_scanner(profile: ScannerProfile):
    with sync_playwright() as playwright:
        return run(playwright, profile)