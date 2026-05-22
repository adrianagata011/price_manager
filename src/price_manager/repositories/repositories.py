import datetime
from typing import Optional

from price_manager.database.connection import ConexionDB
from price_manager.entities.entities import (
    Almacen,
    Categoria,
    CotizacionDolar,
    Moneda,
    Precio,
    Producto,
    Proveedor,
    Stock,
    TipoCotizacion
)
from price_manager.models.models import (
    AlmacenModel,
    CategoriaModel,
    CotizacionModel,
    MonedaModel,
    ProductoModel,
    ProveedorModel,
    StockModel,
    TipoCotizacionModel
)


class RepositorioDBBase:
  """Clase base para repositorios que utilizan base de datos."""

  def __init__(self) -> None:
    """Inicializa la conexión compartida con la base de datos."""

    self._conexion = ConexionDB()


class RepositorioCategoria(RepositorioDBBase):
  """Repositorio de categorías usando base de datos."""

  def crear(self, e: Categoria) -> Categoria:
    """Crea una categoría."""

    with self._conexion.manejar_transaccion() as sesion:
      if sesion.get(CategoriaModel, e.id):
        raise ValueError("Ya existe una categoría con ese ID.")

      sesion.add(
          CategoriaModel(
              id=e.id,
              nombre=e.nombre
          )
      )

    return e

  def leer_todos(self) -> list[Categoria]:
    """Obtiene todas las categorías."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = sesion.query(CategoriaModel).all()

      return [
          Categoria(
              r.id,
              r.nombre
          )
          for r in registros
      ]

  def leer_por_id(self, id: int) -> Optional[Categoria]:
    """Obtiene una categoría por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(CategoriaModel, id)

      if not registro:
        return None

      return Categoria(
          registro.id,
          registro.nombre
      )

  def actualizar(self, e: Categoria) -> Categoria:
    """Actualiza una categoría existente."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(CategoriaModel, e.id)

      if not registro:
        raise ValueError("No existe una categoría con ese ID.")

      registro.nombre = e.nombre

    return e

  def eliminar(self, id: int) -> bool:
    """Elimina una categoría por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(CategoriaModel, id)

      if not registro:
        raise ValueError("No existe una categoría con ese ID.")

      sesion.delete(registro)

    return True


class RepositorioProveedor(RepositorioDBBase):
  """Repositorio de proveedores usando base de datos."""

  def crear(self, e: Proveedor) -> Proveedor:
    """Crea un proveedor."""

    with self._conexion.manejar_transaccion() as sesion:
      if sesion.get(ProveedorModel, e.id):
        raise ValueError("Ya existe un proveedor con ese ID.")

      sesion.add(
          ProveedorModel(
              id=e.id,
              nombre=e.nombre,
              contacto=e.contacto
          )
      )

    return e

  def leer_todos(self) -> list[Proveedor]:
    """Obtiene todos los proveedores."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = sesion.query(ProveedorModel).all()

      return [
          Proveedor(
              r.id,
              r.nombre,
              r.contacto
          )
          for r in registros
      ]

  def leer_por_id(self, id: int) -> Optional[Proveedor]:
    """Obtiene un proveedor por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(ProveedorModel, id)

      if not registro:
        return None

      return Proveedor(
          registro.id,
          registro.nombre,
          registro.contacto
      )

  def actualizar(self, e: Proveedor) -> Proveedor:
    """Actualiza un proveedor existente."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(ProveedorModel, e.id)

      if not registro:
        raise ValueError("No existe un proveedor con ese ID.")

      registro.nombre = e.nombre
      registro.contacto = e.contacto

    return e

  def eliminar(self, id: int) -> bool:
    """Elimina un proveedor por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(ProveedorModel, id)

      if not registro:
        raise ValueError("No existe un proveedor con ese ID.")

      sesion.delete(registro)

    return True


class RepositorioAlmacen(RepositorioDBBase):
  """Repositorio de almacenes usando base de datos."""

  def crear(self, e: Almacen) -> Almacen:
    """Crea un almacén."""

    with self._conexion.manejar_transaccion() as sesion:
      if sesion.get(AlmacenModel, e.id):
        raise ValueError("Ya existe un almacén con ese ID.")

      sesion.add(
          AlmacenModel(
              id=e.id,
              nombre=e.nombre,
              ubicacion=e.ubicacion
          )
      )

    return e

  def leer_todos(self) -> list[Almacen]:
    """Obtiene todos los almacenes."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = sesion.query(AlmacenModel).all()

      return [
          Almacen(
              r.id,
              r.nombre,
              r.ubicacion
          )
          for r in registros
      ]

  def leer_por_id(self, id: int) -> Optional[Almacen]:
    """Obtiene un almacén por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(AlmacenModel, id)

      if not registro:
        return None

      return Almacen(
          registro.id,
          registro.nombre,
          registro.ubicacion
      )

  def actualizar(self, e: Almacen) -> Almacen:
    """Actualiza un almacén existente."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(AlmacenModel, e.id)

      if not registro:
        raise ValueError("No existe un almacén con ese ID.")

      registro.nombre = e.nombre
      registro.ubicacion = e.ubicacion

    return e

  def eliminar(self, id: int) -> bool:
    """Elimina un almacén por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(AlmacenModel, id)

      if not registro:
        raise ValueError("No existe un almacén con ese ID.")

      sesion.delete(registro)

    return True


class RepositorioMoneda(RepositorioDBBase):
  """Repositorio de monedas usando base de datos."""

  def crear(self, e: Moneda) -> Moneda:
    """Crea una moneda."""

    with self._conexion.manejar_transaccion() as sesion:
      if sesion.get(MonedaModel, e.id):
        raise ValueError("Ya existe una moneda con ese ID.")

      sesion.add(
          MonedaModel(
              id=e.id,
              nombre=e.nombre,
              codigo=e.codigo
          )
      )

    return e

  def leer_todos(self) -> list[Moneda]:
    """Obtiene todas las monedas."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = sesion.query(MonedaModel).all()

      return [
          Moneda(
              r.id,
              r.nombre,
              r.codigo
          )
          for r in registros
      ]

  def leer_por_id(self, id: int) -> Optional[Moneda]:
    """Obtiene una moneda por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(MonedaModel, id)

      if not registro:
        return None

      return Moneda(
          registro.id,
          registro.nombre,
          registro.codigo
      )

  def actualizar(self, e: Moneda) -> Moneda:
    """Actualiza una moneda existente."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(MonedaModel, e.id)

      if not registro:
        raise ValueError("No existe una moneda con ese ID.")

      registro.nombre = e.nombre
      registro.codigo = e.codigo

    return e

  def eliminar(self, id: int) -> bool:
    """Elimina una moneda por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(MonedaModel, id)

      if not registro:
        raise ValueError("No existe una moneda con ese ID.")

      sesion.delete(registro)

    return True


class RepositorioTipoCotizacion(RepositorioDBBase):
  """Repositorio de tipos de cotización usando base de datos."""

  def crear(self, e: TipoCotizacion) -> TipoCotizacion:
    """Crea un tipo de cotización."""

    with self._conexion.manejar_transaccion() as sesion:
      if sesion.get(TipoCotizacionModel, e.id):
        raise ValueError("Ya existe un tipo de cotización con ese ID.")

      sesion.add(
          TipoCotizacionModel(
              id=e.id,
              nombre=e.nombre
          )
      )

    return e

  def leer_todos(self) -> list[TipoCotizacion]:
    """Obtiene todos los tipos de cotización."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = sesion.query(TipoCotizacionModel).all()

      return [
          TipoCotizacion(
              r.id,
              r.nombre
          )
          for r in registros
      ]

  def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
    """Obtiene un tipo de cotización por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(TipoCotizacionModel, id)

      if not registro:
        return None

      return TipoCotizacion(
          registro.id,
          registro.nombre
      )

  def actualizar(self, e: TipoCotizacion) -> TipoCotizacion:
    """Actualiza un tipo de cotización existente."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(TipoCotizacionModel, e.id)

      if not registro:
        raise ValueError("No existe un tipo de cotización con ese ID.")

      registro.nombre = e.nombre

    return e

  def eliminar(self, id: int) -> bool:
    """Elimina un tipo de cotización por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(TipoCotizacionModel, id)

      if not registro:
        raise ValueError("No existe un tipo de cotización con ese ID.")

      sesion.delete(registro)

    return True


class RepositorioProducto(RepositorioDBBase):
  """Repositorio de productos usando base de datos."""

  def crear(self, p: Producto) -> Producto:
    """Crea un producto."""

    with self._conexion.manejar_transaccion() as sesion:
      if sesion.get(ProductoModel, p.id):
        raise ValueError("Ya existe un producto con ese ID.")

      sesion.add(
          ProductoModel(
              id=p.id,
              nombre=p.nombre,
              descripcion=p.descripcion,
              precio=p.precio.valor,
              moneda_id=p.precio.moneda.id,
              cat_id=p.categoria.id,
              prov_id=p.proveedor.id
          )
      )

    return p

  def leer_todos(self) -> list[Producto]:
    """Obtiene todos los productos."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = sesion.query(ProductoModel).all()

      return [
          self._modelo_a_entidad(r)
          for r in registros
      ]

  def leer_por_id(self, id: int) -> Optional[Producto]:
    """Obtiene un producto por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(ProductoModel, id)

      if not registro:
        return None

      return self._modelo_a_entidad(registro)

  def actualizar(self, p: Producto) -> Producto:
    """Actualiza un producto existente."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(ProductoModel, p.id)

      if not registro:
        raise ValueError("No existe un producto con ese ID.")

      registro.nombre = p.nombre
      registro.descripcion = p.descripcion
      registro.precio = p.precio.valor
      registro.moneda_id = p.precio.moneda.id
      registro.cat_id = p.categoria.id
      registro.prov_id = p.proveedor.id

    return p

  def eliminar(self, id: int) -> bool:
    """Elimina un producto por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(ProductoModel, id)

      if not registro:
        raise ValueError("No existe un producto con ese ID.")

      sesion.delete(registro)

    return True

  def _modelo_a_entidad(self, registro: ProductoModel) -> Producto:
    """Convierte un modelo ORM ProductoModel a entidad Producto."""

    moneda = Moneda(
        registro.moneda.id,
        registro.moneda.nombre,
        registro.moneda.codigo
    )

    precio = Precio(
        registro.precio,
        moneda
    )

    categoria = Categoria(
        registro.categoria.id,
        registro.categoria.nombre
    )

    proveedor = Proveedor(
        registro.proveedor.id,
        registro.proveedor.nombre,
        registro.proveedor.contacto
    )

    return Producto(
        registro.id,
        registro.nombre,
        registro.descripcion,
        precio,
        categoria,
        proveedor
    )


class RepositorioStock(RepositorioDBBase):
  """Repositorio de stock usando base de datos."""

  def crear(self, s: Stock) -> Stock:
    """Crea un registro de stock."""

    with self._conexion.manejar_transaccion() as sesion:
      existente = (
          sesion.query(StockModel)
          .filter_by(
              producto_id=s.producto.id,
              almacen_id=s.almacen.id
          )
          .first()
      )

      if existente:
        raise ValueError("Ya existe stock para ese producto en ese almacén.")

      sesion.add(
          StockModel(
              producto_id=s.producto.id,
              almacen_id=s.almacen.id,
              cantidad=s.cantidad
          )
      )

    return s

  def leer_todos(self) -> list[Stock]:
    """Obtiene todos los registros de stock."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = sesion.query(StockModel).all()

      return [
          self._modelo_a_entidad(r)
          for r in registros
      ]

  def leer_por_producto_y_almacen(
      self,
      producto_id: int,
      almacen_id: int
  ) -> int:
    """Obtiene la cantidad de stock para producto y almacén."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = (
          sesion.query(StockModel)
          .filter_by(
              producto_id=producto_id,
              almacen_id=almacen_id
          )
          .first()
      )

      if not registro:
        return 0

      return registro.cantidad

  def actualizar(self, s: Stock) -> Stock:
    """Actualiza el stock de un producto en un almacén."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = (
          sesion.query(StockModel)
          .filter_by(
              producto_id=s.producto.id,
              almacen_id=s.almacen.id
          )
          .first()
      )

      if not registro:
        raise ValueError("No existe stock para ese producto en ese almacén.")

      registro.cantidad = s.cantidad

    return s

  def eliminar(
      self,
      producto_id: int,
      almacen_id: int
  ) -> bool:
    """Elimina un registro de stock."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = (
          sesion.query(StockModel)
          .filter_by(
              producto_id=producto_id,
              almacen_id=almacen_id
          )
          .first()
      )

      if not registro:
        raise ValueError("No existe stock para ese producto en ese almacén.")

      sesion.delete(registro)

    return True

  def _modelo_a_entidad(self, registro: StockModel) -> Stock:
    """Convierte un modelo ORM StockModel a entidad Stock."""

    producto_model = registro.producto
    almacen_model = registro.almacen

    producto = Producto(
        producto_model.id,
        producto_model.nombre,
        producto_model.descripcion,
        Precio(
            producto_model.precio,
            Moneda(
                producto_model.moneda.id,
                producto_model.moneda.nombre,
                producto_model.moneda.codigo
            )
        ),
        Categoria(
            producto_model.categoria.id,
            producto_model.categoria.nombre
        ),
        Proveedor(
            producto_model.proveedor.id,
            producto_model.proveedor.nombre,
            producto_model.proveedor.contacto
        )
    )

    almacen = Almacen(
        almacen_model.id,
        almacen_model.nombre,
        almacen_model.ubicacion
    )

    return Stock(
        producto,
        almacen,
        registro.cantidad
    )


class RepositorioCotizacionDolar(RepositorioDBBase):
  """Repositorio de cotizaciones usando base de datos."""

  def crear(self, c: CotizacionDolar) -> CotizacionDolar:
    """Crea una cotización."""

    with self._conexion.manejar_transaccion() as sesion:
      if c.id and sesion.get(CotizacionModel, c.id):
        raise ValueError("Ya existe una cotización con ese ID.")

      sesion.add(
          CotizacionModel(
              id=c.id if c.id else None,
              valor=c.valor,
              fecha=datetime.datetime.combine(
                  c.fecha,
                  datetime.time.min
              ),
              tipo_id=c.tipo.id
          )
      )

    return c

  def leer_todos(self) -> list[CotizacionDolar]:
    """Obtiene todas las cotizaciones."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = sesion.query(CotizacionModel).all()

      return [
          self._modelo_a_entidad(r)
          for r in registros
      ]

  def leer_por_id(self, id: int) -> Optional[CotizacionDolar]:
    """Obtiene una cotización por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(CotizacionModel, id)

      if not registro:
        return None

      return self._modelo_a_entidad(registro)

  def leer_historico_por_tipo(
      self,
      tipo_id: int
  ) -> list[CotizacionDolar]:
    """Obtiene cotizaciones por tipo."""

    with self._conexion.manejar_transaccion() as sesion:
      registros = (
          sesion.query(CotizacionModel)
          .filter_by(tipo_id=tipo_id)
          .all()
      )

      return [
          self._modelo_a_entidad(r)
          for r in registros
      ]

  def actualizar(self, c: CotizacionDolar) -> CotizacionDolar:
    """Actualiza una cotización existente."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(CotizacionModel, c.id)

      if not registro:
        raise ValueError("No existe una cotización con ese ID.")

      registro.valor = c.valor
      registro.fecha = datetime.datetime.combine(
          c.fecha,
          datetime.time.min
      )
      registro.tipo_id = c.tipo.id

    return c

  def eliminar(self, id: int) -> bool:
    """Elimina una cotización por ID."""

    with self._conexion.manejar_transaccion() as sesion:
      registro = sesion.get(CotizacionModel, id)

      if not registro:
        raise ValueError("No existe una cotización con ese ID.")

      sesion.delete(registro)

    return True

  def _modelo_a_entidad(
      self,
      registro: CotizacionModel
  ) -> CotizacionDolar:
    """Convierte un modelo ORM CotizacionModel a entidad CotizacionDolar."""

    tipo = TipoCotizacion(
        registro.tipo.id,
        registro.tipo.nombre
    )

    return CotizacionDolar(
        valor=registro.valor,
        fecha=registro.fecha.date(),
        tipo=tipo,
        id=registro.id
    )
