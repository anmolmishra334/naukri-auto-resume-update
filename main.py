# main.py
import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def refresh_resume(email, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        await page.goto("https://www.naukri.com/mnjuser/login")
        await page.fill('input[name="username"]', email)
        await page.fill('input[name="password"]', password)
        await page.click('//button[@type="submit"]')
        await page.wait_for_load_state('networkidle')

        await page.goto("https://www.naukri.com/mnjuser/profile")
        await page.wait_for_timeout(5000)

        try:
            download_btn = await page.wait_for_selector("//a[contains(text(), 'Download')]", timeout=5000)
            download = await download_btn.click(force=True)
            download_file = await page.wait_for_event('download')
            await download_file.save_as("resume.pdf")
            print(f"✅ [{email}] Resume downloaded.")
        except:
            print(f"⚠️ [{email}] Resume download failed. Proceeding to re-upload.")

        try:
            await page.set_input_files('input[type="file"]', "resume.pdf")
            await page.wait_for_timeout(5000)
            print(f"✅ [{email}] Resume uploaded successfully.")
        except Exception as e:
            print(f"❌ [{email}] Resume upload failed:", e)
            raise e

        await browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <email> <password>")
    else:
        email = sys.argv[1]
        password = sys.argv[2]
        asyncio.run(refresh_resume(email, password))
