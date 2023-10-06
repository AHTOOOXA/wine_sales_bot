from twisted.internet import task
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import db_manager
from spiders.perekrestok_spider import PerekrestokSpider
from spiders.simplewine_spider import SimpleWineSpider
from spiders.amwine_spider import AMWineSpider
from spiders.vivino_spider import VivinoSpider
import logging
import telergam_manager

TIME_DELAY = 86400


def log_to_tg(func):  # MAKE IT LOG TO ADMIN BOT
    def wrap(*args, **kwargs):
        telergam_manager.post(f'Calling {func.__name__}')
        result = func(*args, **kwargs)
        return result
    return wrap


@log_to_tg
def scrap_shops():
    settings = {
        'USER_AGENT': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
        'ITEM_PIPELINES': {'pipelines.SavingToDatabasePipeline': 200},
        'DOWNLOAD_DELAY': 2,
    }
    runner = CrawlerRunner(settings=settings)
    runner.crawl(PerekrestokSpider)
    runner.crawl(AMWineSpider)
    runner.crawl(SimpleWineSpider)
    deferred = runner.join()
    deferred.addCallback(lambda _: scrap_vivino())


@log_to_tg
def scrap_vivino():
    settings = {
        'USER_AGENT': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
        'ITEM_PIPELINES': {'pipelines.VivinoSavingToDatabasePipeline': 200},
        'DOWNLOADER_MIDDLEWARES': {'middlewares.TooManyRequestsRetryMiddleware': 200},
        'DOWNLOAD_DELAY': 2,
    }
    runner = CrawlerRunner(settings=settings)
    deferred = runner.crawl(VivinoSpider, db.get_wines_to_rate())
    deferred.addCallback(lambda _: clean_db_and_post_wines())


@log_to_tg
def clean_db_and_post_wines():
    db.clean_up()
    for wine in db.get_wines_to_post():
        telergam_manager.post_wine(wine)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    db = db_manager.Database()

    loop = task.LoopingCall(scrap_shops)
    loopDeferred = loop.start(TIME_DELAY)

    reactor.run()
