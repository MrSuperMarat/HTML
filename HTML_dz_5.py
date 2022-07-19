# 1.Написать программу, которая собирает входящие письма из
# своего или тестового почтового ящика и сложить данные о
# письмах в базу данных (от кого, дата отправки, тема письма,
# текст письма полный).
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException,\
    ElementClickInterceptedException, NoSuchWindowException,\
    NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
from pymongo import MongoClient

# from selenium.webdriver.support.ui import WebDriverWait as wait
# from selenium.webdriver.support import expected_conditions as cond

client = MongoClient('127.0.0.1', 27017)
db = client['users1807']

m_letters = db.m_letters
m_products = db.m_products

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)  # , options=options
driver.implicitly_wait(10)

driver.get('https://mail.ru')

authorization = driver.find_element(By.CLASS_NAME, 'ph-login')
authorization.click()

# wait(driver, 1).until(
#     cond.frame_to_be_available_and_switch_to_it
#     ((By.XPATH, "//iframe[@class='ag-popup__frame__layout__iframe']")))

frame = driver.find_element(
    By.XPATH, "//iframe[@class='ag-popup__frame__layout__iframe']")
# frame = wait(driver, 5).until(
#     cond.element_to_be_clickable((
#         By.XPATH, "//iframe[@class='ag-popup__frame__layout__iframe']")))

driver.switch_to.frame(frame)

while True:
    try:
        login = driver.find_element(By.NAME, 'username')
        break
    except NoSuchWindowException:
        pass

login.send_keys('study.ai_172@mail.ru', Keys.ENTER)
# button = driver.find_element(
#     By.XPATH, "//button[@data-test-id='next-button']")
# button.click()

password = driver.find_element(By.NAME, 'password')
# password = wait(driver, 5).until(
#  cond.element_to_be_clickable((By.NAME, 'password'))
# )
# password = wait(driver, 5).until(
#  cond.visibility_of_element_located((By.NAME, 'password'))
# )
# password = wait(driver, 5).until(
#  cond.presence_of_element_located((By.NAME, 'password'))
# )

password.send_keys('NextPassword172#', Keys.ENTER)

driver.switch_to.default_content()

first = driver.find_element(
    By.XPATH, "//a[contains(@class,'llc')]")
first.click()

while True:
    try:
        from_whom = driver.find_element(
            By.XPATH, "//span[@class='letter-contact']").text
        date = driver.find_element(
            By.XPATH, "//div[@class='letter__date']").text
        title = driver.find_element(
            By.XPATH, "//h2[@class='thread-subject']").text
        text = driver.find_element(
            By.CLASS_NAME, 'letter__body').text
        down = driver.find_element(
            By.XPATH, "//span[contains(@class,'arrow-down')]")
        down.click()
        m_letters.insert_one({'from': from_whom,
                              'date': date, 'title': title,
                              'text': text})
    except StaleElementReferenceException:
        pass
    except ElementClickInterceptedException:
        m_letters.insert_one({'from': from_whom, 'date': date,
                              'title': title, 'text': text})
        break

[pprint(i) for i in m_letters.find({})]

m_letters.delete_many({})

# 2. Написать программу, которая собирает товары «В тренде» с
# сайта техники mvideo и складывает данные в БД. Сайт можно
# выбрать и свой. Главный критерий выбора: динамически
# загружаемые товары.

driver.get('https://www.mvideo.ru')

while True:
    try:
        button = driver.find_element(
            By.XPATH, "//button[@class='tab-button ng-star-inserted']")
        button.click()
        break
    except NoSuchElementException:
        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                          Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                          Keys.DOWN, Keys.DOWN)
        actions.perform()
    except WebDriverException:
        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                          Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.DOWN,
                          Keys.DOWN, Keys.DOWN)
        actions.perform()

names = driver.find_elements(
    By.XPATH, "//mvid-carousel[@class='carusel"
              " ng-star-inserted']//div[@class='title']")
rating = driver.find_elements(
    By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted'"
              "]//span[@class='value ng-star-inserted']")
count_reviews = driver.find_elements(
    By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted'"
              "]//span[contains(@class,'product-rating')]")
prices = driver.find_elements(
    By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted'"
              "]//span[@class='price__main-value']")

for i in range(len(names)):
    m_products.insert_one({
        'name': names[i].text, 'rating': rating[i].text,
        'count_reviews': count_reviews[i].text,
        'price': prices[i].text})

[pprint(i) for i in m_products.find({})]

m_products.delete_many({})

client.close()
