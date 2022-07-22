import scrapy
from scrapy.http import HtmlResponse
from lesson_6.job.jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/'
                  'razrabotchik.html?geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[contains(@class,'button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath(
            "//span[@class='_2TI7V _21QHd _36Ys4 _3SmWj']/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath(
            "//span[@class='_4Gt5t _2nJZK']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
