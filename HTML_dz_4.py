# 1. Написать приложение, которое собирает основные новости с сайта
# на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга
# использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/103.0.0.0 Safari/537.36'}

session = requests.Session()

news_list = []

lenta = 'https://lenta.ru'

response = session.get(lenta, headers=headers)

dom = html.fromstring(response.text)

articles = dom.xpath("//a[contains(@class,'topnews')]")

for article in articles[:-1]:
    news = {}
    source = 'lenta.ru'

    name = article.xpath("./div/h3[contains(@class,'card-big__"
                         "title')]/text() | ./div/span[contains"
                         "(@class,'card-mini__title')]/text()")
    link = article.xpath("./@href")
    date = article.xpath(".//div/time[contains(@class,'card-')"
                         "]/text()")
    news['source'] = source
    news['name'] = name[0]
    news['link'] = source + link[0]
    news['date'] = date[0]
    news_list.append(news)

yandex = 'https://yandex.ru/news/'

response2 = session.get(yandex, headers=headers)

dom2 = html.fromstring(response2.text)

articles2 = dom2.xpath("//section[@aria-labelledby"
                       "='top-heading']/div/div")

for article in articles2:
    news = {}
    source = article.xpath(".//a[@class='mg-card__source-link']/text()")
    name = article.xpath(".//a[@class='mg-card__link']/text()")
    link = article.xpath(".//a/@href")
    date = article.xpath(".//span[@class='mg-card-source__time']/text()")
    news['source'] = source[0]
    news['name'] = name[0].replace('\xa0', ' ')
    news['link'] = link[0]
    news['date'] = date[0]
    news_list.append(news)

mail = ('https://news.mail.ru/?_ga=2.3615600.'
        '1520428100.1657566067-909586527.1646163189')

response3 = session.get(mail, headers=headers)

dom3 = html.fromstring(response3.text)

links = dom3.xpath("//div[@data-logger='news__"
                   "MainTopNews']//td//a/@href | "
                   "//div[@data-logger='news__MainTopNews']"
                   "//li[@class='list__item']/a/@href")

for link in links:
    news = {}
    resp_link = session.get(link, headers=headers)
    for_article = html.fromstring(resp_link.text)
    article = for_article.xpath("//div[contains(@class,'js-article')]")
    source = article[0].xpath(".//span[@class='link__text']/text()")
    name = article[0].xpath(".//h1/text()")
    date = article[0].xpath(".//span[@datetime]/@datetime")
    news['source'] = source[0]
    news['name'] = name[0]
    news['link'] = link
    news['date'] = date[0]
    news_list.append(news)

# 2. Сложить собранные новости в БД

client = MongoClient('127.0.0.1', 27017)
db = client['users0807']

m_news = db.m_news

m_news.insert_many(news_list)

[pprint(i) for i in m_news.find({})]

m_news.delete_many({})

client.close()
