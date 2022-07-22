# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        self.RE_SALARY_FROM_TO = re.compile(r'от (\d+) до (\d+) ([а-яёA-Z]+)')
        self.RE_SALARY_FROM = re.compile(r'от (\d+) ([а-яёA-Z]+)')
        self.RE_SALARY_TO = re.compile(r'до (\d+) ([а-яёA-Z]+)')
        self.RE_SALARY = re.compile(r'(\d+) – (\d+) ([а-яёA-Z]+)')
        self.RE_SALARY2 = re.compile(
            r'((?:\d{,3}\xa0{1})+)—((?:\d{,3}\xa0{1})+) ([а-яёA-Z]+)')
        self.RE_SALARY_FROM2 = re.compile(
            r'от\xa0((?:\d{,3}\xa0{1})+) ([а-яёA-Z]+)')
        self.RE_SALARY_TO2 = re.compile(
            r'до\xa0((?:\d{,3}\xa0{1})+) ([а-яёA-Z]+)')
        self.RE_SALARY_EQ = re.compile(r'((?:\d{,3}\xa0{1})+) ([а-яёA-Z]+)')
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies1507

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary'] = self.process_salary_hh(item['salary'])
        if spider.name == 'sjru':
            item['salary'] = self.process_salary_sj(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        for_salary = ''.join(salary).replace('\xa0', '')
        if 'от' in for_salary and 'до' in for_salary:
            sal_str = self.RE_SALARY_FROM_TO.findall(for_salary)
            return (' '.join([sal_str[0][0], sal_str[0][2]]),
                    ' '.join([sal_str[0][1], sal_str[0][2]]))
        elif 'от' in for_salary:
            sal_str = self.RE_SALARY_FROM.findall(for_salary)
            return ' '.join([sal_str[0][0], sal_str[0][1]]), None
        elif 'до' in for_salary:
            sal_str = self.RE_SALARY_TO.findall(for_salary)
            return None, ' '.join([sal_str[0][0], sal_str[0][1]])
        elif '–' in for_salary:
            sal_str = self.RE_SALARY.findall(for_salary)
            return (' '.join([sal_str[0][0], sal_str[0][2]]),
                    ' '.join([sal_str[0][1], sal_str[0][2]]))
        else:
            return None, None

    def process_salary_sj(self, salary):
        for_salary = ''.join(salary)
        if 'от' in for_salary:
            sal_str = self.RE_SALARY_FROM2.findall(for_salary)
            return ' '.join([sal_str[0][0].replace('\xa0', ''),
                             sal_str[0][1]]), None
        elif 'до\xa0' in for_salary:
            sal_str = self.RE_SALARY_TO2.findall(for_salary)
            return None, ' '.join([sal_str[0][0].replace('\xa0', ''),
                                   sal_str[0][1]])
        elif '—' in for_salary:
            sal_str = self.RE_SALARY2.findall(for_salary)
            return ' '.join([sal_str[0][0].replace('\xa0', ''),
                             sal_str[0][2]]), ' '.join(
                [sal_str[0][1].replace('\xa0', ''), sal_str[0][2]])
        elif 'По' in for_salary:
            return None, None
        else:
            sal_str = self.RE_SALARY_EQ.findall(for_salary)
            return ' '.join([sal_str[0][0].replace('\xa0', ''),
                             sal_str[0][1]]), ' '.join(
                [sal_str[0][0].replace('\xa0', ''), sal_str[0][1]])
