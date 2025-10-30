
from playwright.sync_api import sync_playwright
import os

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('Gerador')

        # 1. Open the local HTML file and wait for it to be ready
        page.goto(f'file://{file_path}', wait_until='domcontentloaded')

        # 2. Simulate login to show the main app
        # Use Playwright's locator to wait for the element and ensure it exists
        login_modal = page.locator("#login-modal")
        login_modal.wait_for(state="visible")

        # Now manipulate the DOM
        page.evaluate('document.getElementById("login-modal").classList.remove("visible")')
        page.evaluate('document.getElementById("main-app-container").classList.remove("hidden")')
        page.evaluate('document.getElementById("loader").style.display = "none"')

        # Wait for the main container to be visible before proceeding
        page.locator("#main-app-container").wait_for(state="visible")

        # 3. Navigate to the "Tabela de Preços" tab
        page.locator('button[data-tab="prices"]').click()
        page.locator("#category-list-container").wait_for(state="visible") # Wait for an element inside the tab

        # 4. Take a screenshot of the new category management section
        page.screenshot(path="jules-scratch/verification/01_tabela_de_precos.png")

        # 5. Click the "Adicionar Categoria" button and take a screenshot of the modal
        page.locator('#add-category-btn').click()
        page.locator("#category-modal").wait_for(state="visible")
        page.screenshot(path="jules-scratch/verification/02_modal_adicionar_categoria.png")
        page.locator('#modal-category-cancel-btn').click() # Close modal

        # 6. Navigate to the "Gerador" tab
        page.locator('button[data-tab="generator"]').click()
        page.locator("#servicos-por-vida").wait_for(state="visible") # Wait for an element inside the tab

        # 7. Take a screenshot of the services grouped by category
        page.screenshot(path="jules-scratch/verification/03_gerador_agrupado.png")

        browser.close()

if __name__ == '__main__':
    main()
