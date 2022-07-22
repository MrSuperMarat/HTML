# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        if spider.name == 'labru':
            item['authors'] = self.process_authors(item['authors'])
        if spider.name == 'bookru':
            item['price'] = self.process_price(item['price'])
            item['discount_price'] = self.process_discount(
             item['price'], item['discount_price'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_authors(self, authors):
        if len(authors) == 1:
            return authors[0]
        else:
            return ', '.join(authors)

    def process_price(self, price):
        if price is not None:
            return price.replace('\xa0', '')
        else:
            return None

    def process_discount(self, price, discount_price):
        if discount_price is not None:
            return discount_price.replace('\xa0', '')
        else:
            return price
