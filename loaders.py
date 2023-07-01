from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


class PerekrestokItemLoader(ItemLoader):
    # MUST!! get only str input
    #        result is db ready (dif types)
    default_output_processor = TakeFirst()
    name_in = MapCompose(lambda x: ' '.join(x.split()[1:-2]))
    price_new_in = MapCompose(lambda x: float(x[0:-2].replace(',', '.').replace(' ', '')))
    price_old_in = MapCompose(lambda x: float(x[0:-2].replace(',', '.').replace(' ', '')))
    url_in = MapCompose(lambda x: f"https://www.perekrestok.ru{x}")


class SimpleWineItemLoader(ItemLoader):
    # MUST!! get only str input
    #        result is db ready (dif types)
    default_output_processor = TakeFirst()
    name_in = MapCompose(lambda x: x.strip().replace('\xa0', ''))
    price_new_in = MapCompose(lambda x: float(x[0:-2].replace(',', '.').replace(' ', '')))
    price_old_in = MapCompose(lambda x: float(x[0:-2].replace(',', '.').replace(' ', '')))
    url_in = MapCompose(lambda x: f"https://simplewine.ru{x}")


class AromatniyMirItemLoader(ItemLoader):
    # MUST!! get only str input
    #        result is db ready (dif types)
    default_output_processor = TakeFirst()
    name_in = MapCompose(lambda x: x)
    price_new_in = MapCompose(lambda x: float(x.replace(',', '.').replace(' ', '')))
    price_old_in = MapCompose(lambda x: float(x.replace(',', '.').replace(' ', '')))
    url_in = MapCompose(lambda x: f"https://amwine.ru{x}")
