import scrapy
from scrapy.http import HtmlResponse
from lesson_7.castorama.shopparser.items import ShopparserItem
from scrapy.loader import ItemLoader


class ShopSpider(scrapy.Spider):
    name = 'shop'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch"
                           f"/result/?q={kwargs.get('search')}"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath(
            "//a[contains(@class,'product-card__name')]/@href")
        for link in links:
            yield response.follow(link, callback=self.shop_parse)

    def shop_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=ShopparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//div[@class='js-zoom-"
                                   "container']/img/@data-src")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[@class='price']//text()")
        characteristics = response.xpath("//div[@id='specifications'"
                                         "]//dt/span/text()").getall()
        characteristics_val = response.xpath(
            "//div[@id='specifications']//dd/text()").getall()
        # characteristics = {n.strip(): v.strip() for n, v in
        #                   zip(characteristics_name, characteristics_val)}
        loader.add_value('characteristics', characteristics)
        loader.add_value('characteristics_val', characteristics_val)
        yield loader.load_item()

        # name = response.xpath("//h1/text()").get()
        # photos = response.xpath("//div[@class='js-zoom-container'"
        #                         "]/img/@data-src").getall()
        # url = response.url
        # price = response.xpath("//span[@class='price']//text()").get()
        # yield ShopparserItem(name=name, photos=photos,
        #                      price=price, url=url)
