import scrapy
from scrapy.http import HtmlResponse
from lesson_6.book.bookparser.items import BookparserItem


class BookruSpider(scrapy.Spider):
    name = 'bookru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=Python']
    page = 1

    def parse(self, response):
        next_page = f'https://book24.ru/search/page-{self.page}/?q=Python'
        if response.status == 200:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath(
            "//a[@class='product-card__name smartLink']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        self.page += 1

    def book_parse(self, response: HtmlResponse):
        url = response.url
        name = response.xpath("//h1/text()").get()
        authors = response.xpath(
            "//div[@class='product-characteristic__value']//text()").get()
        discount_price = response.xpath(
            "//span[@class='app-price product"
            "-sidebar-price__price-old']/text()").get()
        price = response.xpath(
            "//span[@class='app-price product-"
            "sidebar-price__price']/text()").get()
        rating = response.xpath(
            "//span[@class='rating"
            "-widget__main-text']/text()").get()
        yield BookparserItem(
            url=url, name=name, authors=authors,
            discount_price=discount_price, price=price, rating=rating)
