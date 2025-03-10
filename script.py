from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re

# Inicia o navegador
service = Service('geckodriver.exe')
driver = webdriver.Firefox(service=service)
driver.get('https://googlefonts.github.io/noto-emoji-animation/')

# Rola a página até o fim
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Espera e encontra os botões de emojis
wait = WebDriverWait(driver, 2)
elements = driver.find_elements(By.CSS_SELECTOR, 'button.is-svg')

emoji_data_list = []

# Para cada emoji encontrado, extraímos os dados e guardamos
for element in elements:
    try:
        wait.until(EC.visibility_of(element))
        driver.execute_script("arguments[0].scrollIntoView();", element)

        element.click()

        # Extrai o conteúdo HTML do código
        content = driver.find_element(By.CSS_SELECTOR, '.multiline > code:nth-child(1)').get_attribute('innerHTML')

        # Substitui os códigos HTML e extrai dados com regex
        content = content.replace("&lt;", "<").replace("&gt;", ">")
        srcset = re.search(r'srcset="(https://[^\"]+)"', content)
        src = re.search(r'src="(https://[^\"]+)"', content)
        alt = re.search(r'alt="([^"]+)"', content)

        emoji_data = {
            "source": {"srcset": srcset.group(1) if srcset else None},
            "img": {"src": src.group(1) if src else None, "alt": alt.group(1) if alt else None}
        }

        emoji_data_list.append(emoji_data)

        print(f"Emoji encontrado: {emoji_data}")
    except Exception as e:
        print(f"Erro: {e}")

print(f"Total de emojis extraídos: {len(emoji_data_list)}")

# Salva os dados no formato JSON
driver.quit()
with open('emojis.json', 'w', encoding='utf-8') as json_file:
    json.dump({"emojis": emoji_data_list}, json_file, ensure_ascii=False, indent=4)
