import scrapy


class WineItem(scrapy.Item):
    name = scrapy.Field()
    price_new = scrapy.Field()
    price_old = scrapy.Field()
    rating = scrapy.Field()
    shop = scrapy.Field()
    url = scrapy.Field()
    updated = scrapy.Field()
    posted = scrapy.Field()
    tags = scrapy.Field()
