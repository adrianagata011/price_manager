
# =========================================
# SERVICIOS DEL SISTEMA
# =========================================
# Este módulo concentra la lógica de negocio del proyecto.
# La idea es que los servicios actúen como intermediarios entre
# la interfaz y los repositorios, validando reglas antes de persistir datos.

from price_manager.entities.entities import (
    Categoria,
    Proveedor,
    Almacen,
    Moneda,
    TipoCotizacion,
    CotizacionDolar,
    Producto,
    Stock
)

from price_manager.repositories.repositories import (
    RepositorioCategoria,
    RepositorioProveedor,
    RepositorioAlmacen,
    RepositorioMoneda,
    RepositorioTipoCotizacion,
    RepositorioCotizacionDolar,
    RepositorioProducto,
    RepositorioStock
)


# =========================================
# SERVICIO CATEGORIA
# =========================================
class ServicioCategoria:
    def __init__(self, repo: RepositorioCategoria):
        self._repo = repo

    def crear(self, c: Categoria):
        return self._repo.crear(c)

    def obtener(self, id: int):
        return self._repo.leer_por_id(id)

    def listar_todos(self):
        return self._repo.leer_todos()

    def actualizar(self, c: Categoria):
        return self._repo.actualizar(c)

    def eliminar(self, id: int):
        return self._repo.eliminar(id)


# =========================================
# SERVICIO PROVEEDOR
# =========================================
class ServicioProveedor:
    def __init__(self, repo: RepositorioProveedor):
        self._repo = repo

    def crear(self, p: Proveedor):
        return self._repo.crear(p)

    def obtener(self, id: int):
        return self._repo.leer_por_id(id)

    def listar_todos(self):
        return self._repo.leer_todos()

    def actualizar(self, p: Proveedor):
        return self._repo.actualizar(p)

    def eliminar(self, id: int):
        return self._repo.eliminar(id)


# =========================================
# SERVICIO ALMACEN
# =========================================
class ServicioAlmacen:
    def __init__(self, repo: RepositorioAlmacen):
        self._repo = repo

    def crear(self, a: Almacen):
        return self._repo.crear(a)

    def obtener(self, id: int):
        return self._repo.leer_por_id(id)

    def listar_todos(self):
        return self._repo.leer_todos()

    def actualizar(self, a: Almacen):
        return self._repo.actualizar(a)

    def eliminar(self, id: int):
        return self._repo.eliminar(id)


# =========================================
# SERVICIO MONEDA
# =========================================
class ServicioMoneda:
    def __init__(self, repo: RepositorioMoneda):
        self._repo = repo

    def crear(self, m: Moneda):
        return self._repo.crear(m)

    def obtener(self, id: int):
        return self._repo.leer_por_id(id)

    def listar_todos(self):
        return self._repo.leer_todos()

    def actualizar(self, m: Moneda):
        return self._repo.actualizar(m)

    def eliminar(self, id: int):
        return self._repo.eliminar(id)


# =========================================
# SERVICIO TIPO DE COTIZACION
# =========================================
class ServicioTipoCotizacion:
    def __init__(self, repo: RepositorioTipoCotizacion):
        self._repo = repo

    def crear(self, t: TipoCotizacion):
        return self._repo.crear(t)

    def obtener(self, id: int):
        return self._repo.leer_por_id(id)

    def listar_todos(self):
        return self._repo.leer_todos()

    def actualizar(self, t: TipoCotizacion):
        return self._repo.actualizar(t)

    def eliminar(self, id: int):
        return self._repo.eliminar(id)


# =========================================
# SERVICIO PRODUCTO
# =========================================
# Se validan relaciones antes de persistir, para evitar productos
# asociados a categorías o proveedores inexistentes.
class ServicioProducto:
    def __init__(self, repo: RepositorioProducto, srv_cat: ServicioCategoria, srv_prov: ServicioProveedor):
        self._repo = repo
        self._srv_cat = srv_cat
        self._srv_prov = srv_prov

    def crear(self, p: Producto):
        categoria = self._srv_cat.obtener(p.categoria.id)
        if not categoria:
            raise ValueError(f"La categoría con ID {p.categoria.id} no existe.")

        proveedor = self._srv_prov.obtener(p.proveedor.id)
        if not proveedor:
            raise ValueError(f"El proveedor con ID {p.proveedor.id} no existe.")

        return self._repo.crear(p)

    def obtener(self, id: int):
        res = self._repo.leer_por_id(id)
        if not res:
            raise ValueError(f"Producto con ID {id} no existe.")
        return res

    def listar_todos(self):
        return self._repo.leer_todos()

    def actualizar(self, p: Producto):
        categoria = self._srv_cat.obtener(p.categoria.id)
        if not categoria:
            raise ValueError(f"La categoría con ID {p.categoria.id} no existe.")

        proveedor = self._srv_prov.obtener(p.proveedor.id)
        if not proveedor:
            raise ValueError(f"El proveedor con ID {p.proveedor.id} no existe.")

        return self._repo.actualizar(p)

    def eliminar(self, id: int):
        return self._repo.eliminar(id)


# =========================================
# SERVICIO STOCK
# =========================================
# Maneja el stock por producto y almacén.
# Se controla que nunca quede una cantidad negativa.
class ServicioStock:
    def __init__(self, repo: RepositorioStock, srv_prod: ServicioProducto, srv_alm: ServicioAlmacen):
        self._repo = repo
        self._srv_prod = srv_prod
        self._srv_alm = srv_alm

    def crear(self, s: Stock):
        # Se valida que producto y almacén existan
        producto = self._srv_prod.obtener(s.producto.id)
        almacen = self._srv_alm.obtener(s.almacen.id)

        if not producto:
            raise ValueError(f"El producto con ID {s.producto.id} no existe.")
        if not almacen:
            raise ValueError(f"El almacén con ID {s.almacen.id} no existe.")

        return self._repo.crear(s)

    def obtener(self, producto_id: int, almacen_id: int):
        return self._repo.leer_por_producto_y_almacen(producto_id, almacen_id)

    def listar_todos(self):
        return self._repo.leer_todos()

    def actualizar(self, s: Stock):
        producto = self._srv_prod.obtener(s.producto.id)
        almacen = self._srv_alm.obtener(s.almacen.id)

        if not producto:
            raise ValueError(f"El producto con ID {s.producto.id} no existe.")
        if not almacen:
            raise ValueError(f"El almacén con ID {s.almacen.id} no existe.")

        return self._repo.actualizar(s)

    def eliminar(self, producto_id: int, almacen_id: int):
        return self._repo.eliminar(producto_id, almacen_id)

    def registrar_movimiento(self, producto_id: int, cantidad: int, almacen_id: int):
        # Se obtiene el producto real desde el servicio
        producto = self._srv_prod.obtener(producto_id)

        # Se valida que exista el almacén
        almacen = self._srv_alm.obtener(almacen_id)
        if not almacen:
            raise ValueError(f"El almacén con ID {almacen_id} no existe.")

        # Se consulta stock actual
        actual = self._repo.leer_por_producto_y_almacen(producto_id, almacen_id)
        nueva_cantidad = actual + cantidad

        # Regla de negocio: el stock no puede quedar negativo
        if nueva_cantidad < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")

        nuevo_stock = Stock(producto, almacen, nueva_cantidad)

        # Si ya existe, se actualiza; si no, se crea
        if actual > 0 or self._repo.leer_por_producto_y_almacen(producto_id, almacen_id) == 0:
            try:
                return self._repo.actualizar(nuevo_stock)
            except ValueError:
                return self._repo.crear(nuevo_stock)

    def obtener_stock(self, producto_id: int, almacen_id: int):
        return self._repo.leer_por_producto_y_almacen(producto_id, almacen_id)


# =========================================
# SERVICIO COTIZACION DOLAR
# =========================================
# Se valida que el tipo de cotización exista antes de registrar
# o consultar cotizaciones.
class ServicioCotizacionDolar:
    def __init__(self, repo: RepositorioCotizacionDolar, srv_tipo: ServicioTipoCotizacion):
        self._repo = repo
        self._srv_tipo = srv_tipo

    def crear(self, c: CotizacionDolar):
        tipo = self._srv_tipo.obtener(c.tipo.id)
        if not tipo:
            raise ValueError(f"El tipo de cotización con ID {c.tipo.id} no existe.")

        return self._repo.crear(c)

    def obtener(self, id: int):
        res = self._repo.leer_por_id(id)
        if not res:
            raise ValueError(f"La cotización con ID {id} no existe.")
        return res

    def listar_todos(self):
        return self._repo.leer_todos()

    def actualizar(self, c: CotizacionDolar):
        tipo = self._srv_tipo.obtener(c.tipo.id)
        if not tipo:
            raise ValueError(f"El tipo de cotización con ID {c.tipo.id} no existe.")

        return self._repo.actualizar(c)

    def eliminar(self, id: int):
        return self._repo.eliminar(id)

    def registrar_cotizacion(self, c: CotizacionDolar):
        return self.crear(c)

    def obtener_historico(self, tipo_id: int):
        tipo = self._srv_tipo.obtener(tipo_id)
        if not tipo:
            raise ValueError(f"El tipo de cotización con ID {tipo_id} no existe.")

        return self._repo.leer_historico_por_tipo(tipo_id)
