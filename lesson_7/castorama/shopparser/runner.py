from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from lesson_7.castorama.shopparser.spiders.shop import ShopSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(ShopSpider, search='бензопила')
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
