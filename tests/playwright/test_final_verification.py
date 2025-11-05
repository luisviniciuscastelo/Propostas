
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Aumenta o timeout padrão para 60 segundos
        page.set_default_timeout(60000)

        # Habilita o log do console
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

        try:
            print("Navegando para a página...")
            await page.goto('http://localhost:8000/Gerador.html', wait_until='domcontentloaded')

            print("Esperando a página carregar na visualização do cliente...")
            # Esperamos pelo botão de logout que se torna o botão de login para vendedores
            vendor_login_button = page.locator("#btn-logout:has-text('Login para Vendedores')")
            await expect(vendor_login_button).to_be_visible()

            print("Abrindo o modal de login...")
            await vendor_login_button.click()
            await expect(page.locator("#login-modal")).to_be_visible()

            # 1. Login
            print("Preenchendo credenciais e fazendo login...")
            await page.fill("#login-email", "testemedmais@gmail.com")
            await page.fill("#login-password", "1234567")
            await page.click("#btn-login")

            # 2. Espera pela UI do vendedor e verifica o botão "+ Nova Proposta"
            print("Esperando pela UI do vendedor e pelo botão 'Nova Proposta'...")
            new_proposal_button = page.locator("#btn-new-proposal")
            await expect(new_proposal_button).to_be_visible()
            print("Botão 'Nova Proposta' está visível.")

            # 3. Verifica a Tabela e os Cabeçalhos
            print("Verificando a estrutura da tabela de serviços...")
            service_table = page.locator("table.w-full.text-sm")
            await expect(service_table.first).to_be_visible()

            # Procura por um cabeçalho que contenha o texto 'Valor'
            valor_header = page.locator("th:has-text('Valor')")
            await expect(valor_header.first).to_be_visible()
            print("Cabeçalho 'Valor' encontrado.")

            # Garante que o cabeçalho 'Descrição' não está presente
            descricao_header = page.locator("th:has-text('Descrição')")
            await expect(descricao_header).to_have_count(0)
            print("Cabeçalho 'Descrição' não está presente, como esperado.")

            # 4. Verifica a exibição de preços
            print("Verificando se os preços estão sendo exibidos na tabela...")
            # Encontra a linha do serviço 'PCMSO' e depois o input de preço dentro dela
            pcmso_row = page.locator(".service-row", has_text="PCMSO")
            await expect(pcmso_row).to_be_visible()

            price_input = pcmso_row.locator("input.price-input")
            await expect(price_input).to_be_visible()

            # Verifica se o valor do input não está vazio
            await expect(price_input).not_to_have_value("")
            price_value = await price_input.input_value()
            print(f"Preço encontrado para PCMSO: {price_value}")
            assert price_value != "0,00"

            # 5. Verifica o cálculo do resumo
            print("Verificando o cálculo do resumo da proposta...")
            # Seleciona o serviço PCMSO
            await pcmso_row.locator("input.service-checkbox").check()

            # Verifica se o valor total mensal foi atualizado e não é zero
            total_mensal_locator = page.locator("#valor-total-mensal")
            await expect(total_mensal_locator).not_to_have_text("R$ 0,00")

            total_value = await total_mensal_locator.inner_text()
            print(f"Cálculo do resumo verificado. Valor Total Mensal: {total_value}")

            # 6. Captura de tela
            screenshot_path = "tests/playwright/screenshot_final.png"
            print(f"Tirando screenshot: {screenshot_path}")
            await page.screenshot(path=screenshot_path)

            print("Verificação final concluída com sucesso!")

        except Exception as e:
            print(f"Ocorreu um erro durante o teste: {e}")
            # Tira um screenshot de erro
            await page.screenshot(path="tests/playwright/error_screenshot.png")
            raise

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
