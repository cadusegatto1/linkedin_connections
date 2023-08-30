from time import sleep
import random
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login_linkedin(user, pw):
    nav.get(URL)

    # Clica em Sign in
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div/p[1]/a'))).click()

    # Envia user e pw
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(user)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(pw)

    # Clica em Entrar
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))).click()


def find_buttons():
    # Find both 'Connect' and 'Follow' buttons
    sleep(random.uniform(1, 3))
    return nav.find_elements(By.XPATH, "//button/span[text()='Connect' or text()='Follow']")


def click_send_button():
    try:
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button/span[text()="Send"]')))
        send_button.click()
    except NoSuchElementException:
        print("Botão 'Send' não encontrado.")
    except Exception as e:
        print(f"Erro ao clicar no botão Send: {e}")


def click_buttons(button_list):
    global contagem
    for button in button_list:
        if contagem > 60:
            break
        else:
            try:
                if button.text == "Follow":
                    # Vá até o ancestral comum
                    common_ancestor = button.find_element(By.XPATH, './ancestor::li')

                    # Do ancestral comum, encontre o link do perfil
                    profile_link = common_ancestor.find_element(By.XPATH, './/div/div/div[2]/div[1]/div[1]/div/span['
                                                                          '1]/span/a')

                    # Abra o perfil em uma nova aba
                    profile_link.send_keys(Keys.CONTROL + Keys.SHIFT + Keys.RETURN)
                    nav.switch_to.window(nav.window_handles[0])
                    sleep(random.uniform(2, 5))

                elif button.text == "Connect":
                    button.click()
                    sleep(random.uniform(2, 5))
                    click_send_button()
                    contagem += 1
                    print(contagem, " conexões enviadas")

            except Exception as e:
                print(f"Erro ao clicar no botão: {e}")


def tab_connect():
    try:
        # Botão 'More'
        more = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div["
                                                                "2]/div/div/main/section[1]/div[2]/div[3]/div/div["
                                                                "2]/button/span")))
        more.click()

        # Botão 'Connect'
        con = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div["
                                                               "2]/div/div/main/section[1]/div[2]/div[3]/div/div["
                                                               "2]/div/div/ul/li[3]/div/span")))
        con.click()

        click_send_button()
        return True
    except NoSuchElementException:
        print("Botão 'Connect' não encontrado")
        return False


def process_opened_tabs():
    # Lista de abas abertas
    tabs = nav.window_handles
    for tab in tabs[1:]:  # Pula a primeira aba, pois é a aba principal do LinkedIn
        nav.switch_to.window(tab)
        tab_connect()
        sleep(2)
        nav.close()  # Fecha a aba atual
    nav.switch_to.window(tabs[0])  # Volta para a aba principal


def go_to_next_page():
    try:
        sleep(random.uniform(3, 6))
        nav.find_element(By.XPATH, "//button/span[text()='Next']").click()
        return True
    except NoSuchElementException:
        print("Botão 'Next' não encontrado.")
        return False


if __name__ == '__main__':
    # Inicia as variáveis
    contagem = 0
    service = Service(executable_path=ChromeDriverManager().install())

    # Solicita os dados relevantes
    URL = input("Digite a URL da página de pesquisa: ")
    username = input("Digite seu usuário: ")
    password = input("Digite sua senha: ")

    # Inicia o navegador
    print("Iniciando o navegador...")
    nav = webdriver.Chrome(service=service)
    wait = WebDriverWait(nav, random.uniform(7, 10))
    nav.maximize_window()

    # Faz o login
    print("Logando no LinkedIn...")
    login_linkedin(username, password)
    print("Logado!")

    # Loop principal
    while True:
        try:
            sleep(random.uniform(7, 10))
            buttons = find_buttons()
            if not buttons:
                print("Não foram encontrados botões, tentando novamente...")
                sleep(random.uniform(5, 8))
                buttons = find_buttons()
                if not buttons:
                    print("Não foram encontrados botões novamente. Indo para a próxima página...")
                    success = go_to_next_page()
                    sleep(random.uniform(2, 5))
                    if not success:
                        print("Não há mais páginas. Saindo...")
                        break

            print(f"Encontrados {len(buttons)} botões. Processando...")
            sleep(random.uniform(2, 5))
            click_buttons(buttons)

            print("Indo para a próxima página...")

            success = go_to_next_page()
            if not success:
                print("Não há mais páginas. Saindo...")
                break
        except ElementClickInterceptedException:
            print("Chegamos à última página.")
            break

    print("Processando abas abertas...")
    process_opened_tabs()

    input("Pressione Enter para sair...")
