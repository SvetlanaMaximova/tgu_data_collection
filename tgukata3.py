"""Скрещиваем Selenium и BeautifulSoup
Соберите информацию с сайта nbcomputers.ru
(https://www.nbcomputers.ru/catalog/noutbuki/)
о ноутбуках данного интернет-магазина.
Данные, которые необходимы:
•	Название ноутбука
•	Цена ноутбука
•	Код товара
Результат необходимо записать в CSV файл.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path='/usr/lib/chromium-browser/chromedriver')
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://www.nbcomputers.ru/catalog/noutbuki/")
    driver.implicitly_wait(15)
    actions = ActionChains(driver)

    actions.move_to_element(driver.find_element(By.CLASS_NAME, "sc-47746e2f-0"))
    actions.perform()
    wait = WebDriverWait(driver, timeout=15)

    while True:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sc-47746e2f-0"))).click()

except Exception as ex:
    print(f'Error: {ex}')

html = driver.page_source
# print(html)
with open("html-file.html", "w", encoding="utf-8") as output:
    output.write(html)
driver.quit()



from bs4 import BeautifulSoup
import csv

# with open("html-file.html", "r", encoding="utf-8") as file:
#     html = file.read()

soup = BeautifulSoup(html, 'lxml')
cards_list = soup.select_one('div.sc-26679455-1')
cards = cards_list.select('article.sc-5133e97-0')

spec_info_list = []
for card in cards:
    # код code
    if card.select_one('span.sc-5133e97-16 p'):
        code = card.select_one('span.sc-5133e97-16 p').text
        code = code.replace('Код:', '').strip()
    else:
        code = 'проверить теги'

    # цена price
    if card.select_one('span.sc-96470d6e-2'):
        price = card.select_one('span.sc-96470d6e-2').text
        price = price.replace('₽', '')
        price = price.replace(' ', '').strip()
    else:
        price = 'проверить теги'

    # наименование name
    if card.select_one('div.sc-5133e97-15 h2'):
        name = card.select_one('div.sc-5133e97-15 h2').text
    else:
        name = 'проверить теги'

    spec_info_list.append({
        "название": name,
        "цена": price,
        "код": code
    })

with open("noutbooksKata3.csv", "w", encoding="utf-8") as f:
    writer = csv.DictWriter(f, spec_info_list[0].keys())
    writer.writeheader()
    for row in spec_info_list:
        writer.writerow(row)
