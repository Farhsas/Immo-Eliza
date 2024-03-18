from immo_eliza.immo_eliza.spiders.houses import HousesSpider
from immo_eliza.immo_eliza.spiders.apartments import ApartmentsSpider

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(HousesSpider)
    process.crawl(ApartmentsSpider)
    process.start()
