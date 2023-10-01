from scrapy.crawler import CrawlerProcess
from spiders.amwine_spider import AMWineSpider
from spiders.perekrestok_spider import PerekrestokSpider
from spiders.simplewine_spider import SimpleWineSpider


def scrap():
    settings = {
        'ITEM_PIPELINES': {'pipelines.SavingToDatabasePipeline': 200},
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(AMWineSpider)
    process.crawl(PerekrestokSpider)
    process.crawl(SimpleWineSpider)
    process.start()
