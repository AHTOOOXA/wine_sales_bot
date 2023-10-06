from scrapy import Item, Field


class WineItem(Item):
    name = Field(default='null')
    price_new = Field(default='null')
    price_old = Field(default='null')
    updated = Field(default='null')
    shop = Field(default='null')
    url = Field(default='null')
    rating = Field(default='null')
    rating_count = Field(default='null')
    vivino_url = Field(default='null')
    img_url = Field(default='null')
    post_id = Field(default='null')
