from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
  """Clase base para todos los modelos ORM del sistema."""


class CategoriaModel(Base):
  """Representa una categoría de productos."""

  __tablename__ = "categorias"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(100), nullable=False)

  productos: Mapped[list["ProductoModel"]] = relationship(
      back_populates="categoria"
  )


class ProveedorModel(Base):
  """Representa un proveedor."""

  __tablename__ = "proveedores"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(100), nullable=False)
  contacto: Mapped[str] = mapped_column(String(150), nullable=True)

  productos: Mapped[list["ProductoModel"]] = relationship(
      back_populates="proveedor"
  )


class AlmacenModel(Base):
  """Representa un almacén o depósito."""

  __tablename__ = "almacenes"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(100), nullable=False)
  ubicacion: Mapped[str] = mapped_column(String(150), nullable=False)

  stocks: Mapped[list["StockModel"]] = relationship(
      back_populates="almacen"
  )


class MonedaModel(Base):
  """Representa una moneda."""

  __tablename__ = "monedas"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(100), nullable=False)
  codigo: Mapped[str] = mapped_column(String(10), nullable=False)

  productos: Mapped[list["ProductoModel"]] = relationship(
      back_populates="moneda"
  )


class TipoCotizacionModel(Base):
  """Representa un tipo de cotización."""

  __tablename__ = "tipos_cotizacion"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(100), nullable=False)

  cotizaciones: Mapped[list["CotizacionModel"]] = relationship(
      back_populates="tipo"
  )


class ProductoModel(Base):
  """Representa un producto del catálogo."""

  __tablename__ = "productos"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  nombre: Mapped[str] = mapped_column(String(120), nullable=False)
  descripcion: Mapped[str] = mapped_column(String(255), nullable=True)
  precio: Mapped[float] = mapped_column(Float, nullable=False)
  moneda_id: Mapped[int] = mapped_column(ForeignKey("monedas.id"))
  cat_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
  prov_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"))

  moneda: Mapped["MonedaModel"] = relationship(
      back_populates="productos"
  )
  categoria: Mapped["CategoriaModel"] = relationship(
      back_populates="productos"
  )
  proveedor: Mapped["ProveedorModel"] = relationship(
      back_populates="productos"
  )
  stocks: Mapped[list["StockModel"]] = relationship(
      back_populates="producto"
  )


class StockModel(Base):
  """Representa el stock de un producto en un almacén."""

  __tablename__ = "stock"

  id: Mapped[int] = mapped_column(
      Integer,
      primary_key=True,
      autoincrement=True
  )
  producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
  almacen_id: Mapped[int] = mapped_column(ForeignKey("almacenes.id"))
  cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

  producto: Mapped["ProductoModel"] = relationship(
      back_populates="stocks"
  )
  almacen: Mapped["AlmacenModel"] = relationship(
      back_populates="stocks"
  )


class CotizacionModel(Base):
  """Representa una cotización histórica."""

  __tablename__ = "cotizaciones"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  valor: Mapped[float] = mapped_column(Float, nullable=False)
  fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False)
  tipo_id: Mapped[int] = mapped_column(ForeignKey("tipos_cotizacion.id"))

  tipo: Mapped["TipoCotizacionModel"] = relationship(
      back_populates="cotizaciones"
  )


class AuditoriaModel(Base):
  """Representa una auditoría de operación del sistema."""

  __tablename__ = "auditorias"

  id: Mapped[int] = mapped_column(
      Integer,
      primary_key=True,
      autoincrement=True
  )
  accion: Mapped[str] = mapped_column(String(100), nullable=False)
  fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False)
  detalles: Mapped[str] = mapped_column(String(500), nullable=False)
