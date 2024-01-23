import scrapy
from items import WineItem
from loaders import MetroItemLoader
from datetime import date


class MetroSpider(scrapy.Spider):
    name = 'metro'
    allowed_domains = ['online.metro-cc.ru']
    start_urls = [f'https://online.metro-cc.ru/category/alkogolnaya-produkciya/vino?is_action=1']
    start_urls += [f'https://online.metro-cc.ru/category/alkogolnaya-produkciya/vino?is_action=1&page={i}' for i in range(2, 15)]

    def parse(self, response):
        wines = response.css('.product-card__content')
        for wine in wines:
            wine_loader = MetroItemLoader(item=WineItem(), selector=wine)
            wine_loader.add_css('name', 'div.catalog-2-level-product-card__middle > a > span ::text')
            wine_loader.add_css('price_new', 'div.base-tooltip.product-unit-prices.catalog-2-level-product-card__prices.bottom-right.style--catalog-2-level-product-card-major-prices.can-close-on-click-outside.style--catalog-2-level-product-card-major > button > div > div.product-unit-prices__actual-wrapper > span > span.product-price__sum > span.product-price__sum-rubles ::text')
            wine_loader.add_css('price_old', 'div.base-tooltip.product-unit-prices.catalog-2-level-product-card__prices.bottom-right.style--catalog-2-level-product-card-major-prices.can-close-on-click-outside.style--catalog-2-level-product-card-major > button > div > div.product-unit-prices__old-wrapper > span > span.product-price__sum > span.product-price__sum-rubles ::text')
            wine_loader.add_value('rating', -1)
            wine_loader.add_value('shop', '#Metro')
            wine_loader.add_css('url', 'div.catalog-2-level-product-card__middle > a ::attr(href)')
            wine_loader.add_value('updated', date.today().strftime("%Y-%m-%d"))
            yield wine_loader.load_item()
