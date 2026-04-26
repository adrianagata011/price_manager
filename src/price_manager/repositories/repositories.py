
# =========================================
# REPOSITORIOS DEL SISTEMA (PERSISTENCIA CSV)
# =========================================
# Este módulo implementa la persistencia del sistema en archivos CSV.
# Se eligió este formato por simplicidad, legibilidad y porque cumple
# con la consigna del trabajo práctico de almacenamiento no volátil.

import csv
import os
import datetime

from price_manager.entities.entities import (
    Categoria,
    Proveedor,
    Almacen,
    Moneda,
    Precio,
    TipoCotizacion,
    CotizacionDolar,
    Producto,
    Stock
)


# =========================================
# CLASE BASE PARA REPOSITORIOS CSV
# =========================================
# Centraliza la lógica común de lectura y escritura.
class RepoCSVBase:
    def __init__(self, archivo: str, encabezado: list[str]):
        self.path = f"/content/price_manager/src/price_manager/migrations/csv/{archivo}"
        self.encabezado = encabezado

        # Se asegura que exista la carpeta donde se van a guardar los CSV
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        # Si el archivo no existe, se crea con su encabezado
        if not os.path.exists(self.path):
            self._guardar_todas_lineas([])

    def _leer_todas_lineas(self):
        lineas = []

        if not os.path.exists(self.path):
            return []

        with open(self.path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Se salta el encabezado
            next(reader, None)

            for row in reader:
                if row:
                    lineas.append(row)

        return lineas

    def _guardar_todas_lineas(self, lineas):
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.encabezado)
            writer.writerows(lineas)


# =========================================
# REPOSITORIO CATEGORIA
# =========================================
class RepositorioCategoria(RepoCSVBase):
    def __init__(self):
        super().__init__("categorias.csv", ["id", "nombre"])

    def crear(self, e: Categoria):
        lineas = self._leer_todas_lineas()
        if self.leer_por_id(e.id) is not None:
            raise ValueError("Ya existe una categoría con ese ID.")
        lineas.append([e.id, e.nombre])
        self._guardar_todas_lineas(lineas)
        return e

    def leer_todos(self):
        return [Categoria(int(l[0]), l[1]) for l in self._leer_todas_lineas()]

    def leer_por_id(self, id: int):
        return next((c for c in self.leer_todos() if c.id == id), None)

    def actualizar(self, e: Categoria):
        lineas = self._leer_todas_lineas()

        for i, l in enumerate(lineas):
            if int(l[0]) == e.id:
                lineas[i] = [e.id, e.nombre]
                self._guardar_todas_lineas(lineas)
                return e

        raise ValueError("No existe una categoría con ese ID.")

    def eliminar(self, id: int):
        lineas = self._leer_todas_lineas()
        nuevas = [l for l in lineas if int(l[0]) != id]

        if len(lineas) == len(nuevas):
            raise ValueError("No existe una categoría con ese ID.")

        self._guardar_todas_lineas(nuevas)
        return True


# =========================================
# REPOSITORIO PROVEEDOR
# =========================================
class RepositorioProveedor(RepoCSVBase):
    def __init__(self):
        super().__init__("proveedores.csv", ["id", "nombre", "contacto"])

    def crear(self, e: Proveedor):
        lineas = self._leer_todas_lineas()
        if self.leer_por_id(e.id) is not None:
            raise ValueError("Ya existe un proveedor con ese ID.")
        lineas.append([e.id, e.nombre, e.contacto])
        self._guardar_todas_lineas(lineas)
        return e

    def leer_todos(self):
        return [Proveedor(int(l[0]), l[1], l[2]) for l in self._leer_todas_lineas()]

    def leer_por_id(self, id: int):
        return next((p for p in self.leer_todos() if p.id == id), None)

    def actualizar(self, e: Proveedor):
        lineas = self._leer_todas_lineas()

        for i, l in enumerate(lineas):
            if int(l[0]) == e.id:
                lineas[i] = [e.id, e.nombre, e.contacto]
                self._guardar_todas_lineas(lineas)
                return e

        raise ValueError("No existe un proveedor con ese ID.")

    def eliminar(self, id: int):
        lineas = self._leer_todas_lineas()
        nuevas = [l for l in lineas if int(l[0]) != id]

        if len(lineas) == len(nuevas):
            raise ValueError("No existe un proveedor con ese ID.")

        self._guardar_todas_lineas(nuevas)
        return True


# =========================================
# REPOSITORIO ALMACEN
# =========================================
class RepositorioAlmacen(RepoCSVBase):
    def __init__(self):
        super().__init__("almacenes.csv", ["id", "nombre", "ubicacion"])

    def crear(self, e: Almacen):
        lineas = self._leer_todas_lineas()
        if self.leer_por_id(e.id) is not None:
            raise ValueError("Ya existe un almacén con ese ID.")
        lineas.append([e.id, e.nombre, e.ubicacion])
        self._guardar_todas_lineas(lineas)
        return e

    def leer_todos(self):
        return [Almacen(int(l[0]), l[1], l[2]) for l in self._leer_todas_lineas()]

    def leer_por_id(self, id: int):
        return next((a for a in self.leer_todos() if a.id == id), None)

    def actualizar(self, e: Almacen):
        lineas = self._leer_todas_lineas()

        for i, l in enumerate(lineas):
            if int(l[0]) == e.id:
                lineas[i] = [e.id, e.nombre, e.ubicacion]
                self._guardar_todas_lineas(lineas)
                return e

        raise ValueError("No existe un almacén con ese ID.")

    def eliminar(self, id: int):
        lineas = self._leer_todas_lineas()
        nuevas = [l for l in lineas if int(l[0]) != id]

        if len(lineas) == len(nuevas):
            raise ValueError("No existe un almacén con ese ID.")

        self._guardar_todas_lineas(nuevas)
        return True


# =========================================
# REPOSITORIO MONEDA
# =========================================
class RepositorioMoneda(RepoCSVBase):
    def __init__(self):
        super().__init__("monedas.csv", ["id", "nombre", "codigo"])

    def crear(self, e: Moneda):
        lineas = self._leer_todas_lineas()
        if self.leer_por_id(e.id) is not None:
            raise ValueError("Ya existe una moneda con ese ID.")
        lineas.append([e.id, e.nombre, e.codigo])
        self._guardar_todas_lineas(lineas)
        return e

    def leer_todos(self):
        return [Moneda(int(l[0]), l[1], l[2]) for l in self._leer_todas_lineas()]

    def leer_por_id(self, id: int):
        return next((m for m in self.leer_todos() if m.id == id), None)

    def actualizar(self, e: Moneda):
        lineas = self._leer_todas_lineas()

        for i, l in enumerate(lineas):
            if int(l[0]) == e.id:
                lineas[i] = [e.id, e.nombre, e.codigo]
                self._guardar_todas_lineas(lineas)
                return e

        raise ValueError("No existe una moneda con ese ID.")

    def eliminar(self, id: int):
        lineas = self._leer_todas_lineas()
        nuevas = [l for l in lineas if int(l[0]) != id]

        if len(lineas) == len(nuevas):
            raise ValueError("No existe una moneda con ese ID.")

        self._guardar_todas_lineas(nuevas)
        return True


# =========================================
# REPOSITORIO TIPO DE COTIZACION
# =========================================
class RepositorioTipoCotizacion(RepoCSVBase):
    def __init__(self):
        super().__init__("tipos_cotizacion.csv", ["id", "nombre"])

    def crear(self, e: TipoCotizacion):
        lineas = self._leer_todas_lineas()
        if self.leer_por_id(e.id) is not None:
            raise ValueError("Ya existe un tipo de cotización con ese ID.")
        lineas.append([e.id, e.nombre])
        self._guardar_todas_lineas(lineas)
        return e

    def leer_todos(self):
        return [TipoCotizacion(int(l[0]), l[1]) for l in self._leer_todas_lineas()]

    def leer_por_id(self, id: int):
        return next((t for t in self.leer_todos() if t.id == id), None)

    def actualizar(self, e: TipoCotizacion):
        lineas = self._leer_todas_lineas()

        for i, l in enumerate(lineas):
            if int(l[0]) == e.id:
                lineas[i] = [e.id, e.nombre]
                self._guardar_todas_lineas(lineas)
                return e

        raise ValueError("No existe un tipo de cotización con ese ID.")

    def eliminar(self, id: int):
        lineas = self._leer_todas_lineas()
        nuevas = [l for l in lineas if int(l[0]) != id]

        if len(lineas) == len(nuevas):
            raise ValueError("No existe un tipo de cotización con ese ID.")

        self._guardar_todas_lineas(nuevas)
        return True


# =========================================
# REPOSITORIO PRODUCTO
# =========================================
# Nota:
# Para reconstruir el objeto desde CSV se utilizan objetos simplificados
# para moneda, categoría y proveedor. Esto permite mantener el repositorio
# independiente y no acoplarlo innecesariamente a otros repositorios.
class RepositorioProducto(RepoCSVBase):
    def __init__(self):
        super().__init__(
            "productos.csv",
            ["id", "nombre", "descripcion", "precio", "moneda_id", "cat_id", "prov_id"]
        )

    def crear(self, p: Producto):
        lineas = self._leer_todas_lineas()

        if self.leer_por_id(p.id) is not None:
            raise ValueError("Ya existe un producto con ese ID.")

        lineas.append([
            p.id,
            p.nombre,
            p.descripcion,
            p.precio.valor,
            p.precio.moneda.id,
            p.categoria.id,
            p.proveedor.id
        ])
        self._guardar_todas_lineas(lineas)
        return p

    def leer_por_id(self, id: int):
        for l in self._leer_todas_lineas():
            if int(l[0]) == id:
                mon = Moneda(int(l[4]), "Moneda", "ARS")
                pre = Precio(float(l[3]), mon)

                return Producto(
                    int(l[0]),
                    l[1],
                    l[2],
                    pre,
                    Categoria(int(l[5]), "Categoria"),
                    Proveedor(int(l[6]), "Proveedor", "")
                )
        return None

    def leer_todos(self):
        res = []

        for l in self._leer_todas_lineas():
            try:
                mon = Moneda(int(l[4]), "Moneda", "ARS")
                pre = Precio(float(l[3]), mon)

                res.append(
                    Producto(
                        int(l[0]),
                        l[1],
                        l[2],
                        pre,
                        Categoria(int(l[5]), "Categoria"),
                        Proveedor(int(l[6]), "Proveedor", "")
                    )
                )
            except:
                # Si alguna fila está mal formada se ignora para no romper la carga completa
                continue

        return res

    def actualizar(self, p: Producto):
        lineas = self._leer_todas_lineas()

        for i, l in enumerate(lineas):
            if int(l[0]) == p.id:
                lineas[i] = [
                    p.id,
                    p.nombre,
                    p.descripcion,
                    p.precio.valor,
                    p.precio.moneda.id,
                    p.categoria.id,
                    p.proveedor.id
                ]
                self._guardar_todas_lineas(lineas)
                return p

        raise ValueError("No existe un producto con ese ID.")

    def eliminar(self, id: int):
        lineas = self._leer_todas_lineas()
        nuevas = [l for l in lineas if int(l[0]) != id]

        if len(lineas) == len(nuevas):
            raise ValueError("No existe un producto con ese ID.")

        self._guardar_todas_lineas(nuevas)
        return True


# =========================================
# REPOSITORIO STOCK
# =========================================
# En este caso la clave lógica está compuesta por producto + almacén.
class RepositorioStock(RepoCSVBase):
    def __init__(self):
        super().__init__("stock.csv", ["producto_id", "almacen_id", "cantidad"])

    def crear(self, s: Stock):
        lineas = self._leer_todas_lineas()

        for l in lineas:
            if int(l[0]) == s.producto.id and int(l[1]) == s.almacen.id:
                raise ValueError("Ya existe stock para ese producto en ese almacén.")

        lineas.append([s.producto.id, s.almacen.id, s.cantidad])
        self._guardar_todas_lineas(lineas)
        return s

    def leer_todos(self):
        res = []

        for l in self._leer_todas_lineas():
            try:
                producto = Producto(
                    int(l[0]),
                    "Producto",
                    "",
                    Precio(0, Moneda(0, "Moneda", "ARS")),
                    Categoria(0, "Categoria"),
                    Proveedor(0, "Proveedor", "")
                )

                almacen = Almacen(int(l[1]), "Almacen", "")
                cantidad = int(l[2])

                res.append(Stock(producto, almacen, cantidad))
            except:
                continue

        return res

    def leer_por_producto_y_almacen(self, producto_id: int, almacen_id: int):
        for l in self._leer_todas_lineas():
            try:
                if int(l[0]) == producto_id and int(l[1]) == almacen_id:
                    return int(l[2])
            except:
                continue
        return 0

    def actualizar(self, s: Stock):
        lineas = self._leer_todas_lineas()

        for i, l in enumerate(lineas):
            if int(l[0]) == s.producto.id and int(l[1]) == s.almacen.id:
                lineas[i] = [s.producto.id, s.almacen.id, s.cantidad]
                self._guardar_todas_lineas(lineas)
                return s

        raise ValueError("No existe stock para ese producto en ese almacén.")

    def eliminar(self, producto_id: int, almacen_id: int):
        lineas = self._leer_todas_lineas()
        nuevas = [
            l for l in lineas
            if not (int(l[0]) == producto_id and int(l[1]) == almacen_id)
        ]

        if len(lineas) == len(nuevas):
            raise ValueError("No existe stock para ese producto en ese almacén.")

        self._guardar_todas_lineas(nuevas)
        return True


# =========================================
# REPOSITORIO COTIZACION DOLAR
# =========================================
class RepositorioCotizacionDolar(RepoCSVBase):
    def __init__(self):
        super().__init__("cotizaciones.csv", ["id", "valor", "fecha", "tipo_id"])

    def crear(self, c: CotizacionDolar):
        lineas = self._leer_todas_lineas()

        if any(int(l[0]) == c.id for l in lineas):
            raise ValueError("Ya existe una cotización con ese ID.")

        lineas.append([c.id, c.valor, str(c.fecha), c.tipo.id])
        self._guardar_todas_lineas(lineas)
        return c

    def leer_todos(self):
        res = []

        for l in self._leer_todas_lineas():
            try:
                tipo = TipoCotizacion(int(l[3]), "Tipo")
                res.append(
                    CotizacionDolar(
                        valor=float(l[1]),
                        fecha=datetime.datetime.strptime(l[2], "%Y-%m-%d").date(),
                        tipo=tipo,
                        id=int(l[0])
                    )
                )
            except:
                continue

        return res

    def leer_por_id(self, id: int):
        return next((c for c in self.leer_todos() if c.id == id), None)

    def leer_historico_por_tipo(self, tipo_id: int):
        return [c for c in self.leer_todos() if c.tipo.id == tipo_id]

    def actualizar(self, c: CotizacionDolar):
        lineas = self._leer_todas_lineas()

        for i, l in enumerate(lineas):
            if int(l[0]) == c.id:
                lineas[i] = [c.id, c.valor, str(c.fecha), c.tipo.id]
                self._guardar_todas_lineas(lineas)
                return c

        raise ValueError("No existe una cotización con ese ID.")

    def eliminar(self, id: int):
        lineas = self._leer_todas_lineas()
        nuevas = [l for l in lineas if int(l[0]) != id]

        if len(lineas) == len(nuevas):
            raise ValueError("No existe una cotización con ese ID.")

        self._guardar_todas_lineas(nuevas)
        return True
