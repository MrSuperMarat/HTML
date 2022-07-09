# 1. Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов
# HH(обязательно) и/или Superjob(по желанию). Приложение должно
# анализировать несколько страниц сайта (также вводим через input
# или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и
# максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия. (можно прописать статично hh.ru
# или superjob.ru)
# По желанию можно добавить ещё параметры вакансии (например,
# работодателя и расположение). Структура должна быть одинаковая
# для вакансий с обоих сайтов. Общий результат можно вывести с
# помощью dataFrame через pandas. Сохраните в json либо csv.

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/103.0.0.0 Safari/537.36'}

session = requests.Session()

vacancies_list = []

params = {'page': 0}

url = ('https://hh.ru/search/vacancy?area=113&search_field='
       'name&search_field=company_name&search_field=descrip'
       'tion&text=инженер&hhtmFrom=vacancy_search_catalog'
       '&items_on_page=20')

response = session.get(url, headers=headers, params=params)

dom = BeautifulSoup(response.text, 'html.parser')

vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

RE_SALARY_FROM = re.compile(r'от ((?:\d{,3}.+)+) (руб)')
RE_SALARY_TO = re.compile(r'до ((?:\d{,3}.+)+) (руб)')
RE_SALARY = re.compile(r'((?:\d{,3}.+)+) – ((?:\d{,3}.+)+) (руб)')

# last_page = int(dom.find('span', {
#     'data-qa': 'pager-page-wrapper-100-99'}).text)

while True:
    response = session.get(url, headers=headers, params=params)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
    if len(vacancies) == 0 or response == '<Response [400]>':
        break
    for vacancy in vacancies:
        vacancy_data = {}
        name_link = vacancy.find('a')
        name = name_link.text
        link = name_link.get('href')
        for_salary = vacancy.find('span', {
            'data-qa': 'vacancy-serp__vacancy-compensation'})
        for_employer = vacancy.find('a', {
            'data-qa': 'vacancy-serp__vacancy-employer'}).text
        employer = for_employer.replace('\xa0', ' ')
        for_location = vacancy.find('div', {
            'data-qa': 'vacancy-serp__vacancy-address'}).text
        location = for_location.replace('\xa0', ' ')
        try:
            for_salary2 = for_salary.text
            if 'от' in for_salary2:
                sal_str = RE_SALARY_FROM.findall(for_salary2)
                vacancy_data['salary'] = [
                    int(sal_str[0][0].replace('\u202f', '')
                        ), None, sal_str[0][1]]
            elif 'до' in for_salary2:
                sal_str = RE_SALARY_TO.findall(for_salary2)
                vacancy_data['salary'] = [
                    None, int(sal_str[0][0].replace(
                        '\u202f', '')), sal_str[0][1]]
            else:
                sal_str = RE_SALARY.findall(for_salary2)
                vacancy_data['salary'] = [
                    int(sal_str[0][0].replace('\u202f', '')
                        ), int(sal_str[0][1].replace(
                         '\u202f', '')), sal_str[0][2]]
        except:
            vacancy_data['salary'] = [None, None, None]
        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['website'] = 'hh.ru'
        vacancy_data['employer'] = employer
        vacancy_data['location'] = location.replace('\xa0', ' ')
        vacancies_list.append(vacancy_data)
    params['page'] += 1

url2 = ('https://www.superjob.ru/vakansii/'
        'razrabotchik.html?geo%5Bt%5D%5B0%5D=4')

RE_SALARY2 = re.compile(r'((?:\d{,3}\xa0{1})+)—('
                        r'(?:\d{,3}\xa0{1})+)(руб)')
RE_SALARY_FROM2 = re.compile(r'от\xa0((?:\d{,3}\xa0{1})+)(руб)')
RE_SALARY_TO2 = re.compile(r'до\xa0((?:\d{,3}\xa0{1})+)(руб)')
RE_SALARY_EQ = re.compile(r'((?:\d{,3}\xa0{1})+)(руб)')

response2 = session.get(url2, headers=headers)
dom2 = BeautifulSoup(response2.text, 'html.parser')

# last_page = dom2.find('a', {
#     'class': '_1IHWd _6Nb0L _37aW8 _3187U '
#              'f-test-button-11 f-test-link-11'})
# last_page = int(dom2.select('a.f-test-button-11.'
#                             'f-test-link-11')[0].text)
last_page = int(dom2.select('a.f-test-button-11')[0].text)

for i in range(1, last_page + 1):
    params['page'] = i
    response2 = session.get(url2, headers=headers,
                            params=params)
    dom2 = BeautifulSoup(response2.text, 'html.parser')
    vacancies2 = dom2.find_all('div', {'class': [
        '_2J3hU f-test-vacancy-item _9tHug aoQRr _2VVbx '
        '_3gYDQ', '_2J3hU f-test-vacancy-item _9tHug '
                  'aoQRr _3gYDQ']})
    for vacancy in vacancies2:
        vacancy_data = {}
        name_link = vacancy.find('span', {
            'class': '_2TI7V _21QHd _3SmWj'})
        name = name_link.text
        link = 'https://www.superjob.ru' + name_link.find(
            'a').get('href')
        for_salary = vacancy.find('span', {
            'class', '_1Fg5m _3ndp2 _1_dH8 _1oy1C '
                     '_2eYAG _10_Fa _21QHd _36Ys4 _9Is4f'}
                                  ).text
        if 'от' in for_salary:
            sal_str = RE_SALARY_FROM2.findall(for_salary)
            vacancy_data['salary'] = [int(
                sal_str[0][0].replace('\xa0', '')
            ), None, sal_str[0][1]]
        elif 'до\xa0' in for_salary:
            sal_str = RE_SALARY_TO2.findall(for_salary)
            vacancy_data['salary'] = [None, int(
                sal_str[0][0].replace('\xa0', '')
            ), sal_str[0][1]]
        elif '—' in for_salary:
            sal_str = RE_SALARY2.findall(for_salary)
            vacancy_data['salary'] = [
                int(sal_str[0][0].replace('\xa0', '')
                    ), int(sal_str[0][1].replace(
                     '\xa0', '')), sal_str[0][2]]
        elif 'По' in for_salary:
            vacancy_data['salary'] = [None, None, None]
        else:
            sal_str = RE_SALARY_EQ.findall(for_salary)
            vacancy_data['salary'] = [int(
                sal_str[0][0].replace('\xa0', '')
            ), int(sal_str[0][0].replace('\xa0', '')
                   ), sal_str[0][1]]
        try:
            employer = vacancy.find('div', {
                'class', '_2J3hU _3_tYT LLSBE MgbFi'
            }).find('span', {
                'class', '_3nMqD f-test-text-vacancy'
                         '-item-company-name MjtUU '
                         '_21QHd _36Ys4 _9Is4f _39z8N'
            }).find('a').text
        except:
            employer = None
        location = vacancy.find('span', {
            'class': 'f-test-text-company-item-location '
                     'CJVN9 _21QHd _3lGwd _9Is4f'}).text
        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['website'] = 'superjob.ru'
        vacancy_data['employer'] = employer
        vacancy_data['location'] = location
        vacancies_list.append(vacancy_data)

df = pd.DataFrame(vacancies_list)
print(df)
# df.to_json('vacancies2.json')

with open('vacancies.json', 'w', encoding='ansi') as f,\
        open('vacancies.csv', 'w', encoding='cp1251') as f_csv:
    json.dump(vacancies_list, f, ensure_ascii=False)
    json.dump(vacancies_list, f_csv, ensure_ascii=False)
