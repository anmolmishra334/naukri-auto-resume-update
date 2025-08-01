import sys
import asyncio
from playwright.async_api import async_playwright

async def run(email, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto("https://www.naukri.com/mnjuser/login", wait_until="load")

            # Fill login form using placeholder attributes
            await page.wait_for_selector('input[placeholder="Email ID / Username"]', timeout=15000)
            await page.fill('input[placeholder="Email ID / Username"]', email)
            await page.fill('input[placeholder="Password"]', password)

            await page.click('button[type="submit"]')

            # Wait for login and redirect
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(3000)

            # Go to profile and click Update
            await page.goto("https://www.naukri.com/mnjuser/profile", wait_until="load")
            await page.wait_for_selector('button:has-text("Update")', timeout=15000)
            await page.click('button:has-text("Update")')
            print(f"✅ Resume refreshed successfully for {email}")

        except Exception as e:
            print(f"❌ Error occurred for {email}: {e}")
            print(await page.content())  # Useful for debugging HTML state
            raise e

        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    email = sys.argv[1]
    password = sys.argv[2]
    asyncio.run(run(email, password))
