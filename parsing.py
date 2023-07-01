from scrapy.crawler import CrawlerProcess
from spider import PerekrestokSpider, AromatniyMirSpider, SimpleWineSpider


def scrap():
    process = CrawlerProcess(settings={
        'ITEM_PIPELINES': {'pipelines.SavingToPostgresPipeline': 200},
        'DOWNLOAD_DELAY': 2,
    })
    process.crawl(PerekrestokSpider)
    # process.crawl(AromatniyMirSpider)  # FIX FIRST
    # process.crawl(SimpleWineSpider)  # FIX
    process.start()
