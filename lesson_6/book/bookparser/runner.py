from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from lesson_6.book.bookparser.spiders.bookru import BookruSpider
from lesson_6.book.bookparser.spiders.labru import LabruSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(LabruSpider)
    runner.crawl(BookruSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
