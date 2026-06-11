import json
from pathlib import Path
from urllib.parse import quote_plus, unquote_plus, urlparse, parse_qs

import scrapy

from price_manager.scraper.loaders import ProductoWebLoader


class StarComputacionSpider(scrapy.Spider):
  """Busca productos de Price Manager en Star Computación."""

  name = "star_computacion"
  allowed_domains = [
      "starcomputacion.com.ar",
      "www.starcomputacion.com.ar"
  ]

  custom_settings = {
      "ITEM_PIPELINES": {
          "price_manager.scraper.pipelines.ProductoWebPipeline": 300
      },
      "DOWNLOAD_DELAY": 1,
      "ROBOTSTXT_OBEY": False,
      "USER_AGENT": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/120.0.0.0 Safari/537.36"
      ),
      "DEFAULT_REQUEST_HEADERS": {
          "Accept": (
              "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/avif,image/webp,*/*;q=0.8"
          ),
          "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
          "Connection": "keep-alive"
      },
      "FEEDS": {
          "reports/star_computacion_resultados.json": {
              "format": "json",
              "encoding": "utf8",
              "indent": 2,
              "overwrite": True
          }
      }
  }

  def __init__(
      self,
      productos_path: str | None = None,
      *args,
      **kwargs
  ):
    super().__init__(*args, **kwargs)

    self.productos_path = (
        Path(productos_path)
        if productos_path
        else Path("src/price_manager/scraper/productos_busqueda.json")
    )

    self.start_urls = self.armar_urls_busqueda()

  def armar_urls_busqueda(self):
    """Lee los productos internos y arma las URLs de búsqueda."""

    if not self.productos_path.exists():
      raise FileNotFoundError(
          f"No se encontró el archivo: {self.productos_path}"
      )

    productos = json.loads(
        self.productos_path.read_text(encoding="utf-8")
    )

    urls = []

    for producto in productos:
      nombre_producto = producto["nombre"]
      busqueda = quote_plus(nombre_producto)

      urls.append(
          "https://www.starcomputacion.com.ar/prods/search/"
          f"?search={busqueda}"
      )

    return urls

  def obtener_producto_buscado(self, url):
    """Recupera el texto buscado desde la URL."""

    parametros = parse_qs(
        urlparse(url).query
    )

    busqueda = parametros.get(
        "search",
        [""]
    )[0]

    return unquote_plus(busqueda)

  def limpiar_textos(self, textos):
    """Limpia una lista de textos obtenidos desde el HTML."""

    return [
        " ".join(texto.split())
        for texto in textos
        if " ".join(texto.split())
    ]

  def parse(self, response):
    """Toma hasta 10 resultados por cada búsqueda."""

    producto_buscado = self.obtener_producto_buscado(
        response.url
    )

    resultados = response.css("a.product")[:10]

    if not resultados:
      self.logger.info(
          "No se encontraron resultados para: %s",
          producto_buscado
      )

    for resultado in resultados:
      datos_listado = {
          "producto_buscado": producto_buscado,
          "nombre": " ".join(
              "".join(resultado.css(".title::text").getall()).split()
          ),
          "precio": " ".join(
              "".join(resultado.css(".price::text").getall()).split()
          ),
          "url_producto": response.urljoin(
              resultado.attrib.get("href", "")
          ),
          "url_imagen": response.urljoin(
              resultado.css("img.img::attr(src)").get("")
          )
      }

      yield response.follow(
          datos_listado["url_producto"],
          callback=self.parse_detalle,
          meta={
              "datos_listado": datos_listado
          }
      )

  def parse_detalle(self, response):
    """Completa descripción y formas de pago desde el detalle."""

    datos_listado = response.meta["datos_listado"]

    textos_formas_pago = self.limpiar_textos(
        response.css("#prices_table td::text").getall()
    )

    textos_formas_pago = [
        texto
        for texto in textos_formas_pago
        if "$" not in texto
        and "setStyle" not in texto
        and "buyBtn" not in texto
    ]

    formas_pago = " | ".join(
        textos_formas_pago
    )

    descripcion_breve = self.limpiar_textos(
        response.css("#product_desc ::text").getall()
    )

    descripcion_detallada = self.limpiar_textos(
        response.css("#contenido_desc ::text").getall()
    )

    descripcion = " ".join(
        descripcion_breve + descripcion_detallada
    )

    if not descripcion:
      descripcion = "Descripción detallada no disponible en la página del producto"

    if not formas_pago:
      formas_pago = "Formas de pago no disponibles en la página del producto"

    loader = ProductoWebLoader(
        response=response
    )

    loader.add_value(
        "producto_buscado",
        datos_listado["producto_buscado"]
    )

    loader.add_value(
        "nombre",
        datos_listado["nombre"]
    )

    loader.add_value(
        "precio",
        datos_listado["precio"]
    )

    loader.add_value(
        "url_producto",
        datos_listado["url_producto"]
    )

    loader.add_value(
        "url_imagen",
        datos_listado["url_imagen"]
    )

    loader.add_value(
        "formas_pago",
        formas_pago
    )

    loader.add_value(
        "descripcion",
        descripcion
    )

    yield loader.load_item()
