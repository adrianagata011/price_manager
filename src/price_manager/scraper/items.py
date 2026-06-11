import scrapy


class ProductoWebItem(scrapy.Item):
  """Datos obtenidos desde la tienda web."""

  producto_buscado = scrapy.Field()
  nombre = scrapy.Field()
  precio = scrapy.Field()
  url_producto = scrapy.Field()
  url_imagen = scrapy.Field()
  formas_pago = scrapy.Field()
  descripcion = scrapy.Field()
