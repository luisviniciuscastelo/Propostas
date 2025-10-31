from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    # Client view
    page.goto("file:///app/Gerador")
    page.screenshot(path="jules-scratch/verification/client_view.png")

    # Vendor view
    page.fill("#login-email", "test@test.com")
    page.fill("#login-password", "123456")
    page.click("#btn-login")
    page.wait_for_selector("#main-app-container:not(.hidden)")
    page.screenshot(path="jules-scratch/verification/vendor_view.png")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
