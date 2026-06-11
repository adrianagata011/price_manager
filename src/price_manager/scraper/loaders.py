from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from price_manager.scraper.items import ProductoWebItem


def limpiar_texto(valor: str) -> str:
  """Limpia espacios innecesarios en textos obtenidos desde la web."""

  return " ".join(valor.split())


class ProductoWebLoader(ItemLoader):
  """Loader usado para ordenar los datos del producto web."""

  default_item_class = ProductoWebItem
  default_input_processor = MapCompose(limpiar_texto)
  default_output_processor = TakeFirst()
