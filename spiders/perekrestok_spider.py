import scrapy
from items import WineItem
from loaders import PerekrestokItemLoader
from datetime import date


class PerekrestokSpider(scrapy.Spider):
    name = 'perekrestok'
    allowed_domains = ['perekrestok.ru']
    start_urls = [
        'https://www.perekrestok.ru/cat/c/2/vino?orderBy=discount&orderDirection=desc&tags=onlyDiscount'
    ]

    def parse(self, response):
        wines = response.css('.product-card-wrapper')
        for wine in wines:
            wine_loader = PerekrestokItemLoader(item=WineItem(), selector=wine)
            wine_loader.add_css('name', '.product-card__title ::text')
            wine_loader.add_css('price_new', '.price-new ::text')
            wine_loader.add_css('price_old', '.price-old ::text')
            wine_loader.add_value('rating', -1)
            wine_loader.add_value('shop', '#Perekrestok')
            wine_loader.add_css('url', 'div > a ::attr(href)')
            wine_loader.add_value('updated', date.today().strftime("%Y-%m-%d"))
            wine_loader.add_value('posted', '0')
            yield wine_loader.load_item()
