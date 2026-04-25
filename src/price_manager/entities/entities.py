
# =========================================
# ENTIDADES DEL DOMINIO
# =========================================
# En este módulo se definen las clases principales del sistema.
# Se decidió modelarlas como objetos para encapsular datos y
# mantener una estructura clara y alineada con lo visto en clase.

import datetime
from typing import Optional


# =========================================
# CLASE BASE
# =========================================
# Se utiliza una clase base para centralizar el manejo del ID,
# evitando repetir código en todas las entidades.
class EntidadBase:
    def __init__(self, id: int):
        self._id = id

    @property
    def id(self) -> int:
        return self._id


# =========================================
# ENTIDADES SIMPLES
# =========================================
class Categoria(EntidadBase):
    def __init__(self, id: int, nombre: str):
        super().__init__(id)
        self.nombre = nombre


class Proveedor(EntidadBase):
    def __init__(self, id: int, nombre: str, contacto: str):
        super().__init__(id)
        self.nombre = nombre
        self.contacto = contacto


class Almacen(EntidadBase):
    def __init__(self, id: int, nombre: str, ubicacion: str):
        super().__init__(id)
        self.nombre = nombre
        self.ubicacion = ubicacion


class Moneda(EntidadBase):
    def __init__(self, id: int, nombre: str, codigo: str = "ARS"):
        super().__init__(id)
        self.nombre = nombre
        self.codigo = codigo


# =========================================
# CLASE PRECIO
# =========================================
# Se encapsula el precio para validar reglas de negocio,
# como evitar valores negativos.
class Precio:
    def __init__(self, valor: float, moneda: Moneda, fecha: Optional[datetime.date] = None):
        # Validación: el precio no puede ser negativo
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")

        self._valor = valor
        self.moneda = moneda

        # Si no se especifica fecha, se toma la actual
        self.fecha = fecha or datetime.date.today()

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, v: float):
        # Validación en modificación del precio
        if v < 0:
            raise ValueError("Precio negativo no permitido.")
        self._valor = v


# =========================================
# COTIZACIONES
# =========================================
class TipoCotizacion(EntidadBase):
    def __init__(self, id: int, nombre: str):
        super().__init__(id)
        self.nombre = nombre


class CotizacionDolar:
    # IMPORTANTE:
    # Se deja el id como parámetro opcional al final para mantener
    # compatibilidad con los tests del sistema.
    def __init__(self, valor: float, fecha: datetime.date, tipo: TipoCotizacion, id: int = 0):
        self.id = id

        # Validación: la cotización debe ser positiva
        if valor <= 0:
            raise ValueError("Cotización debe ser positiva.")

        self.valor = valor
        self.fecha = fecha
        self.tipo = tipo


# =========================================
# PRODUCTO
# =========================================
# Representa el elemento central del sistema, vinculando
# categoría, proveedor y precio.
class Producto(EntidadBase):
    def __init__(self, id: int, nombre: str, descripcion: str, precio: Precio, categoria: Categoria, proveedor: Proveedor):
        super().__init__(id)
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.proveedor = proveedor


# =========================================
# STOCK
# =========================================
# Representa la cantidad disponible de un producto en un almacén.
class Stock:
    def __init__(self, producto: Producto, almacen: Almacen, cantidad: int):
        self.producto = producto
        self.almacen = almacen

        # Se inicializa en 0 y luego se valida mediante el setter
        self._cantidad = 0
        self.cantidad = cantidad

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, v: int):
        # Validación: no se permite stock negativo
        if v < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")
        self._cantidad = v
