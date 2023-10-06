import scrapy
from items import WineItem
from loaders import SimpleWineItemLoader
from datetime import date


class SimpleWineSpider(scrapy.Spider):
    name = 'simplewine'
    allowed_domains = ['simplewine.ru']

    start_urls = [
        f'https://simplewine.ru/catalog/vino/filter/sale-1/page{i}' for i in range(15)
    ]

    def parse(self, response):
        wines = response.css('.catalog-grid__item')
        for wine in wines:
            wine_loader = SimpleWineItemLoader(item=WineItem(), selector=wine)
            wine_loader.add_css('name', 'article > div.product-snippet__top > div.product-snippet__right > a ::text')
            wine_loader.add_css('price_new', 'article > div.product-snippet__bottom > div > div.product-snippet__prices-wrapper > div.product-snippet__price.product-snippet__price_discount ::text')
            wine_loader.add_css('price_old', 'article > div.product-snippet__bottom > div > div.product-snippet__prices-wrapper > div.product-snippet__discount > span:nth-child(1) ::text')
            wine_loader.add_value('rating', -1)
            wine_loader.add_value('shop', '#SimpleWine')
            wine_loader.add_css('url', 'article > div.product-snippet__top > div.product-snippet__left > a ::attr(href)')
            wine_loader.add_value('updated', date.today().strftime("%Y-%m-%d"))
            yield wine_loader.load_item()
