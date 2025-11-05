
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        page.set_default_timeout(60000)

        try:
            print("Navegando para a página na visualização de cliente...")
            await page.goto('http://localhost:8000/Gerador.html', wait_until='domcontentloaded')

            print("Esperando a UI do cliente carregar...")
            # Esperamos um elemento específico do cliente, como o título da solicitação de orçamento
            await expect(page.locator("h1:has-text('Solicite seu orçamento!')")).to_be_visible()

            print("Verificando a estrutura da tabela de serviços do cliente...")
            service_table = page.locator("table.w-full.text-sm")
            await expect(service_table.first).to_be_visible()

            # Garante que o cabeçalho 'Descrição' está presente para o cliente
            descricao_header = page.locator("th:has-text('Descrição')")
            await expect(descricao_header.first).to_be_visible()
            print("Cabeçalho 'Descrição' está visível para o cliente, como esperado.")

            # Garante que o cabeçalho 'Valor' não está presente para o cliente
            valor_header = page.locator("th:has-text('Valor')")
            await expect(valor_header).to_have_count(0)
            print("Cabeçalho 'Valor' não está presente para o cliente, como esperado.")

            screenshot_path = "tests/playwright/client_view_verification.png"
            print(f"Tirando screenshot da visualização do cliente: {screenshot_path}")
            await page.screenshot(path=screenshot_path)

            print("Verificação da UI do cliente concluída com sucesso!")

        except Exception as e:
            print(f"Ocorreu um erro durante a verificação da UI do cliente: {e}")
            await page.screenshot(path="tests/playwright/error_screenshot_client.png")
            raise

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
