import scrapy
from thefuzz import fuzz
import unicodedata
import json
from items import WineItem


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


class VivinoSpider(scrapy.Spider):
    name = 'vivino'
    allowed_domains = ['vivino.com']

    def __init__(self, wine_names='', **kwargs):
        print('SPIDER WORKS!!!')
        super().__init__(**kwargs)
        self.wine_names = wine_names
        print(wine_names)

    def start_requests(self):
        for wine_name in self.wine_names:
            # wine_name = self.wine_names
            print(wine_name)
            yield scrapy.Request(
                f"https://www.vivino.com/search/wines?q={wine_name}",
                cb_kwargs={'wine_name': wine_name}
            )
            # break

    def parse(self, response, wine_name):
        print('parse', wine_name)
        wines = response.css('.wine-card__content')
        parsed_wines = []
        for index, wine in enumerate(wines):
            name = remove_accents(''.join(wine.css('div > span > a > span ::text').getall()).strip())
            relative_url = wine.css('div > span > a ::attr(href)').get()
            # formula to be tuned or replaced but its better
            # maximum is 12*8 + 100 = 96 + 100 = 196
            score = (12-index) * 8 + fuzz.token_sort_ratio(name, wine_name)
            parsed_wines.append((score, name, relative_url))
        parsed_wines.sort(reverse=True)
        next_page_url = f'https://www.vivino.com{parsed_wines[0][2]}'
        yield response.follow(next_page_url, callback=self.parse_wine_page, cb_kwargs={'wine_name': wine_name})

    @staticmethod
    def parse_wine_page(response, wine_name=''):
        data = json.loads(response.xpath('//script[@type="application/ld+json"]/text()').get())
        wine_item = WineItem()
        wine_item['name'] = wine_name
        wine_item['rating'] = data['aggregateRating']['ratingValue']
        wine_item['rating_count'] = data['aggregateRating']['ratingCount']
        wine_item['vivino_url'] = vivino_url = data['url']
        wine_item['img_url'] = data['image'].pop()
        yield wine_item
