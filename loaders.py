from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Compose


class PerekrestokItemLoader(ItemLoader):
    # Results are db types ready
    default_output_processor = TakeFirst()
    name_in = MapCompose(lambda x: ' '.join(x.split()[1:-2]))
    price_new_in = MapCompose(lambda x: float(x[0:-2].replace(',', '.').replace(' ', '')))
    price_old_in = MapCompose(lambda x: float(x[0:-2].replace(',', '.').replace(' ', '')))
    url_in = MapCompose(lambda x: f"https://www.perekrestok.ru{x}")


class SimpleWineItemLoader(ItemLoader):
    # Results are db types ready
    default_output_processor = TakeFirst()
    name_in = MapCompose(lambda x: x.strip()[5:-3])
    price_new_in = MapCompose(lambda x: float(x.strip().replace(' ', '').replace(',', '.')[:-1]))
    price_old_in = MapCompose(lambda x: float(x.strip().replace(' ', '').replace(',', '.')[:-1]))
    url_in = MapCompose(lambda x: f"https://simplewine.ru{x}")


class AMWineItemLoader(ItemLoader):
    # # Results are db types ready
    default_output_processor = TakeFirst()
    name_in = MapCompose(lambda x: x.strip()[5:])
    price_new_in = Compose(TakeFirst(), lambda x: float(x.strip()))
    price_old_in = Compose(TakeFirst(), lambda x: float(x.strip()))
    url_in = MapCompose(lambda x: f"https://amwine.ru{x}")
