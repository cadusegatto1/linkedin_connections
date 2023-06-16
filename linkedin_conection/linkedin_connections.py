import os
import json
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

username = "insert your email"
password = "your password"

# URL below look for 'tech recruiter' in 'Spain' or 'Sao Paulo, Brazil', filtering only people and grade connections 
URL = "https://www.linkedin.com/search/results/..........."
c = 0
def login_linkedin(username, password):
    # Abre pagina do google para autenticar em SHopee Fraud Rule Engine
    nav.get(URL)
    # nav.maximize_window()

    # # Clica em Entre
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/p[1]/a'))).click()
    # # Envia user e pw
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(password)
    # # Clica em Entrar
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))).click()

def find_connect_buttons():
    return nav.find_elements(By.XPATH, "//button/span[text()='Connect']")

def click_send_button():
    try:
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button/span[text()="Send"]')))
        send_button.click()
    except NoSuchElementException:
        print("Botão 'Send' não encontrado. A janela não apareceu.")
    except Exception as e:
        print(f"Erro ao clicar no botão Send: {e}")

def click_connect_buttons(connect_buttons):
    global c  # Adicione esta linha para usar a variável global 'c'
    if connect_buttons != []:
        for button in connect_buttons:
            if c > 60:
                break
            else:
                try:
                    button.click()
                    sleep(3)  # Aguarde um pouco entre cada clique para evitar problemas de carregamento
                    click_send_button()  # Clique no botão "Send" na janela que aparece
                    c+=1
                    print(c, " connections sent")
                except Exception as e:
                    print(f"Erro ao clicar no botão Connect ou Send: {e}")

def go_to_next_page():
    try:
        sleep(5)
        nav.find_element(By.XPATH, "//button/span[text()='Next']").click()
        return True
    except NoSuchElementException:
        print("Botão 'Próxima página' não encontrado. Provavelmente estamos na última página.")
        return False

service = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=service)

wait = WebDriverWait(nav, 10)

login_linkedin(username, password)
i = 1
while True:
    print("Page: ", i)
    sleep(10)  # Aguarde um pouco para a página carregar completamente
    print("Aguardei os 10s")
    connect_buttons = find_connect_buttons()
    click_connect_buttons(connect_buttons)
    nav.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    has_next_page = go_to_next_page()
    if not has_next_page:
        break
    i+=1