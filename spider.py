import json
import scrapy
from items import WineItem
from loaders import PerekrestokItemLoader, SimpleWineItemLoader, AromatniyMirItemLoader
from datetime import date


class PerekrestokSpider(scrapy.Spider):
    name = 'perekrestok'
    start_urls = [
        'https://www.perekrestok.ru/cat/c/2/vino?orderBy=discount&orderDirection=desc&tags=onlyDiscount',
    ]

    def parse(self, response):
        WINE_SELECTOR = '.product-card-wrapper'
        for wine in response.css(WINE_SELECTOR):
            NAME_SELECTOR = '.product-card__title ::text'
            PRICE_NEW_SELECTOR = '.price-new ::text'
            PRICE_OLD_SELECTOR = '.price-old ::text'
            LINK_SELECTOR = 'div > a ::attr(href)'

            wine_item = PerekrestokItemLoader(item=WineItem(), selector=wine)

            name = wine.css(NAME_SELECTOR).get()
            wine_item.add_value('name', name)
            wine_item.add_css('price_new', PRICE_NEW_SELECTOR)
            wine_item.add_css('price_old', PRICE_OLD_SELECTOR)
            wine_item.add_value('rating', -1)
            wine_item.add_value('shop', '#Перекрёсток')
            wine_item.add_css('url', LINK_SELECTOR)
            wine_item.add_value('updated', date.today().strftime("%Y-%m-%d"))
            wine_item.add_value('posted', '0')
            # all the beauty and editing happens in item loader to be kept all together

            yield wine_item.load_item()


class AromatniyMirSpider(scrapy.Spider):
    name = 'aromatniymir'

    start_urls = [
        'https://amwine.ru/catalog/rasprodazha/filter/type_drink-is-vino/',
    ]
    for i in range(2, 15):
        start_urls.append(f'https://amwine.ru/catalog/rasprodazha/filter/type_drink-is-vino/?page={i}')

    def parse(self, response):
        script_text: str = response.css("#fix-search > script:nth-child(31) ::text").get()
        start = 'window.products'
        end = 'window.catalogPriceCode'
        s = script_text.find(start) + len(start) + 3  # to remove extra symbols
        e = script_text.find(end) - 6  # to remove extra '; '
        text = script_text[s:e].replace("'", '"')
        json_wine_list = json.loads(text)
        for wine in json_wine_list:
            if 'old_price' in wine.keys():
                wine_item = AromatniyMirItemLoader(item=WineItem())

                name = wine['name']
                wine_item.add_value('name', name)
                # if-else for card only sales correct pricing
                if wine['price_by_card'] != '0':
                    wine_item.add_value('price_new', wine['price_by_card'])
                    wine_item.add_value('price_old', wine['price'])
                else:
                    wine_item.add_value('price_new', wine['price'])
                    wine_item.add_value('price_old', wine['old_price'])
                wine_item.add_value('rating', -1)
                wine_item.add_value('shop', '#АроматныйМир')
                wine_item.add_value('url', wine['link'])
                wine_item.add_value('updated', date.today().strftime("%Y-%m-%d"))
                wine_item.add_value('posted', '0')
                # all the beauty and editing happens in item loader to be kept all together

                yield wine_item.load_item()


class SimpleWineSpider(scrapy.Spider):
    name = 'simplewine'

    start_urls = [
        'https://simplewine.ru/stock/discount/'
    ]
    for i in range(2, 20):
        start_urls.append(f'https://simplewine.ru/stock/discount/page{i}/')

    def parse(self, response):
        WINE_SELECTOR = '.catalog-grid__item'
        for wine in response.css(WINE_SELECTOR):
            NAME_SELECTOR = 'article > div.product-snippet__top > div.product-snippet__right > a ::text'
            PRICE_NEW_SELECTOR = 'article > div.product-snippet__bottom > div > div.product-snippet__price.product-snippet__price_discount ::text'
            PRICE_OLD_SELECTOR = 'article > div.product-snippet__bottom > div > div.product-snippet__discount > span:nth-child(1) ::text'
            LINK_SELECTOR = 'article > div.product-snippet__top > div.product-snippet__left > a ::attr(href)'

            wine_item = SimpleWineItemLoader(item=WineItem(), selector=wine)

            name = wine.css(NAME_SELECTOR).get()
            wine_item.add_value('name', name)
            wine_item.add_css('price_new', PRICE_NEW_SELECTOR)
            wine_item.add_css('price_old', PRICE_OLD_SELECTOR)
            wine_item.add_value('rating', -1)
            wine_item.add_value('shop', '#SimpleWine')
            wine_item.add_css('url', LINK_SELECTOR)
            wine_item.add_value('updated', date.today().strftime("%Y-%m-%d"))
            wine_item.add_value('posted', '0')
            # all the beauty and editing happens in item loader to be kept all together

            yield wine_item.load_item()
