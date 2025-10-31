import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        file_path = "file://" + os.path.abspath("Gerador")

        await page.goto(file_path)

        # Wait for the main app container to be visible
        await page.wait_for_selector("#main-app-container", state="visible", timeout=60000)

        # 1. Take a screenshot of the client view
        await page.screenshot(path="jules-scratch/verification/01_client_view.png")

        # 2. Click the login button and take a screenshot of the login modal
        await page.wait_for_selector("#btn-logout", state="visible", timeout=60000)
        await page.click("#btn-logout")
        await page.wait_for_selector("#login-modal.visible")
        await page.screenshot(path="jules-scratch/verification/02_login_modal.png")

        # 3. Log in as a vendor (simulation)
        await page.fill("#login-email", "test@example.com")
        await page.fill("#login-password", "password")
        await page.evaluate("() => document.getElementById('login-modal').classList.remove('visible')")

        await page.evaluate("""() => {
            const vendorOnlyTabs = [
                document.querySelector('.tab-button[data-tab="clients"]'),
                document.querySelector('.tab-button[data-tab="preview-contract"]'),
                document.querySelector('.tab-button[data-tab="prices"]'),
                document.querySelector('.tab-button[data-tab="saved"]')
            ];
            vendorOnlyTabs.forEach(tab => tab && (tab.style.display = ''));
            const financialParams = document.getElementById('financial-parameters');
            if (financialParams) financialParams.style.display = '';
            document.getElementById('generator-add-client-btn').style.display = '';
            document.getElementById('btn-save-proposal').style.display = '';
            document.getElementById('btn-accept-proposal').style.display = 'none';
            document.getElementById('btn-new-proposal').style.display = '';
            document.getElementById('btn-logout').textContent = 'Sair';
        }""")

        await page.wait_for_timeout(2000) # Increased wait time

        # 4. Take a screenshot of the vendor view
        await page.screenshot(path="jules-scratch/verification/03_vendor_view.png")

        # 5. Navigate to the price table and take a screenshot
        await page.click('.tab-button[data-tab="prices"]')
        await page.wait_for_selector('#tab-prices.active')
        await page.screenshot(path="jules-scratch/verification/04_price_table.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
