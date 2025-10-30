from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Go to the local HTML file
            page.goto(f"file:///app/Gerador")

            # Wait for the main app container to be available, but hidden
            page.wait_for_selector('#main-app-container', state='hidden')

            # Make the main app container visible for interaction
            page.evaluate("document.getElementById('main-app-container').classList.remove('hidden')")

            # Wait for the prices tab button to be visible and click it
            prices_tab_button = page.locator('button[data-tab="prices"]')
            prices_tab_button.wait_for(state='visible')
            prices_tab_button.click()
            page.screenshot(path="jules-scratch/verification/category_management.png")

            # Wait for the generator tab button to be visible and click it
            generator_tab_button = page.locator('button[data-tab="generator"]')
            generator_tab_button.wait_for(state='visible')
            generator_tab_button.click()
            page.screenshot(path="jules-scratch/verification/grouped_services.png")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")

        finally:
            browser.close()

run()
