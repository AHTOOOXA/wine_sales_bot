import scrapy
from items import WineItem
from loaders import AMWineItemLoader
from datetime import date


class AMWineSpider(scrapy.Spider):
    name = 'amwine'
    allowed_domains = ['amwine.ru']
    start_urls = ['https://amwine.ru/catalog/rasprodazha/filter/type_drink-is-vino/']
    start_urls += [f'https://amwine.ru/catalog/rasprodazha/filter/type_drink-is-vino/page={i}' for i in range(2, 15)]

    def parse(self, response):
        wines = response.css('.catalog-list-item__container')
        for wine in wines:
            wine_loader = AMWineItemLoader(item=WineItem(), selector=wine)
            wine_loader.add_css('name', '.catalog-list-item__info > a ::text')
            wine_loader.add_css('price_new', '.middle_price ::text')
            wine_loader.add_css('price_old', '.baseoldprice ::text')
            wine_loader.add_value('rating', -1)
            wine_loader.add_value('shop', '#Aromatniy')
            wine_loader.add_css('url', '.catalog-list-item__info > a ::attr(href)')
            wine_loader.add_value('updated', date.today().strftime("%Y-%m-%d"))
            yield wine_loader.load_item()
