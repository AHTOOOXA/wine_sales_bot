from scrapy import Item, Field


class WineItem(Item):
    name = Field()
    price_new = Field()
    price_old = Field()
    rating = Field()
    shop = Field()
    url = Field()
    updated = Field()
    posted = Field()
    tags = Field()
