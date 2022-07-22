import scrapy
from scrapy.http import HtmlResponse
from lesson_6.book.bookparser.items import BookparserItem


class LabruSpider(scrapy.Spider):
    name = 'labru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/Python/?stype=0']

    def parse(self, response):
        next_page = response.xpath("//a[@title='Следующая']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath(
            "//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        url = response.url
        name = response.xpath("//h1/text()").get()
        authors = response.xpath(
            "//a[@data-event-label='author']/text()").getall()
        price = response.xpath(
            "//span[@class='buying-priceold-val-number']/text()"
            " | //span[@class='buying-price-val-number']/text()").get()
        discount_price = response.xpath(
            "//span[@class='buying-pricenew-val-number']/text()"
            " | //span[@class='buying-price-val-number']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        yield BookparserItem(
            url=url, name=name, authors=authors,
            discount_price=discount_price, price=price, rating=rating)
