
# =========================================
# INTERFAZ DE USUARIO POR CONSOLA
# =========================================
# Permite operar todos los CRUD del sistema mediante consola.
# Se utiliza este enfoque para simplificar la interacción sin
# necesidad de una interfaz gráfica compleja.

from price_manager.entities.entities import (
    Categoria, Proveedor, Almacen, Moneda,
    TipoCotizacion, CotizacionDolar, Producto, Precio
)
import csv
import datetime
from pathlib import Path
import json
import os
import re
import subprocess
from sqlalchemy import text
from price_manager.database.connection import ConexionDB
from price_manager.auditoria.auditoria import registrar_auditoria


class ConsoleUI:

    def __init__(self, srv_prod, srv_cat, srv_prov, srv_stock,
                 srv_alm, srv_mon, srv_tipo, srv_cot):
        self.srv_prod = srv_prod
        self.srv_cat = srv_cat
        self.srv_prov = srv_prov
        self.srv_stock = srv_stock
        self.srv_alm = srv_alm
        self.srv_mon = srv_mon
        self.srv_tipo = srv_tipo
        self.srv_cot = srv_cot

    # =========================================
    # MENÚ PRINCIPAL
    # =========================================
    def mostrar_menu(self):
        print("\n=== PRICE MANAGER ===")
        print("1.  Listar productos")
        print("2.  Crear producto")
        print("3.  Modificar producto")
        print("4.  Eliminar producto")
        print("5.  Ver stock")
        print("6.  Movimiento de stock")
        print("7.  Listar categorías")
        print("8.  Crear categoría")
        print("9.  Modificar categoría")
        print("10. Eliminar categoría")
        print("11. Listar proveedores")
        print("12. Crear proveedor")
        print("13. Modificar proveedor")
        print("14. Eliminar proveedor")
        print("15. Listar almacenes")
        print("16. Crear almacén")
        print("17. Modificar almacén")
        print("18. Eliminar almacén")
        print("19. Listar monedas")
        print("20. Crear moneda")
        print("21. Modificar moneda")
        print("22. Eliminar moneda")
        print("23. Listar tipos cotización")
        print("24. Crear tipo cotización")
        print("25. Modificar tipo cotización")
        print("26. Eliminar tipo cotización")
        print("27. Registrar cotización")
        print("28. Modificar cotización")
        print("29. Eliminar cotización")
        print("30. Ver histórico cotizaciones")
        print("31. Obtener cotizaciones por API")
        print("32. Ver lista de precios bimonetaria")
        print("33. Exportar precios bimonetarios a CSV")
        print("34. Ejecutar scraping")
        print("35. Generar reporte")
        print("36. Ver historial de auditoría")
        print("0. Salir")

        return input("Seleccione una opción: ")

    # =========================================
    # LOOP PRINCIPAL
    # =========================================
    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu()

            try:
                if opcion == "1": self.listar_productos()
                elif opcion == "2": self.crear_producto()
                elif opcion == "3": self.modificar_producto()
                elif opcion == "4": self.eliminar_producto()
                elif opcion == "5": self.ver_stock()
                elif opcion == "6": self.movimiento_stock()
                elif opcion == "7": self.listar_categorias()
                elif opcion == "8": self.crear_categoria()
                elif opcion == "9": self.modificar_categoria()
                elif opcion == "10": self.eliminar_categoria()
                elif opcion == "11": self.listar_proveedores()
                elif opcion == "12": self.crear_proveedor()
                elif opcion == "13": self.modificar_proveedor()
                elif opcion == "14": self.eliminar_proveedor()
                elif opcion == "15": self.listar_almacenes()
                elif opcion == "16": self.crear_almacen()
                elif opcion == "17": self.modificar_almacen()
                elif opcion == "18": self.eliminar_almacen()
                elif opcion == "19": self.listar_monedas()
                elif opcion == "20": self.crear_moneda()
                elif opcion == "21": self.modificar_moneda()
                elif opcion == "22": self.eliminar_moneda()
                elif opcion == "23": self.listar_tipos()
                elif opcion == "24": self.crear_tipo()
                elif opcion == "25": self.modificar_tipo()
                elif opcion == "26": self.eliminar_tipo()
                elif opcion == "27": self.registrar_cotizacion()
                elif opcion == "28": self.modificar_cotizacion()
                elif opcion == "29": self.eliminar_cotizacion()
                elif opcion == "30": self.historico_cotizaciones()
                elif opcion == "31": self.obtener_cotizaciones_api()
                elif opcion == "32": self.ver_lista_precios_bimonetaria()
                elif opcion == "33": self.exportar_precios_bimonetarios_csv()
                elif opcion == "34": self.ejecutar_scraping()
                elif opcion == "35": self.generar_reporte()
                elif opcion == "36": self.ver_historial_auditoria()
                elif opcion == "0":
                    print("Saliendo...")
                    break
                else:
                    print("Opción inválida.")

            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

    # =========================================
    # PRODUCTOS
    # =========================================
    def listar_productos(self):
        for p in self.srv_prod.listar_todos():
            print(f"{p.id} - {p.nombre} - {p.precio.valor}")

    def crear_producto(self):
        id_p = int(input("ID: "))
        nombre = input("Nombre: ")
        desc = input("Descripción: ")
        precio_val = float(input("Precio: "))

        moneda = self.srv_mon.obtener(1)
        precio = Precio(precio_val, moneda)

        cat = self.srv_cat.obtener(int(input("ID categoría: ")))
        prov = self.srv_prov.obtener(int(input("ID proveedor: ")))

        self.srv_prod.crear(Producto(id_p, nombre, desc, precio, cat, prov))
        print("Producto creado.")

    def modificar_producto(self):
        p = self.srv_prod.obtener(int(input("ID: ")))
        p.nombre = input("Nuevo nombre: ") or p.nombre
        self.srv_prod.actualizar(p)

    def eliminar_producto(self):
        self.srv_prod.eliminar(int(input("ID: ")))

    # =========================================
    # STOCK
    # =========================================
    def ver_stock(self):
        print(self.srv_stock.obtener_stock(int(input("ID producto: ")), 1))

    def movimiento_stock(self):
        self.srv_stock.registrar_movimiento(
            int(input("ID producto: ")),
            int(input("Cantidad (+/-): ")),
            1
        )

    # =========================================
    # CATEGORÍAS
    # =========================================
    def listar_categorias(self):
        for c in self.srv_cat.listar_todos():
            print(c.id, c.nombre)

    def crear_categoria(self):
        self.srv_cat.crear(Categoria(int(input("ID: ")), input("Nombre: ")))

    def modificar_categoria(self):
        c = self.srv_cat.obtener(int(input("ID: ")))
        c.nombre = input("Nuevo nombre: ") or c.nombre
        self.srv_cat.actualizar(c)

    def eliminar_categoria(self):
        self.srv_cat.eliminar(int(input("ID: ")))

    # =========================================
    # PROVEEDORES
    # =========================================
    def listar_proveedores(self):
        for p in self.srv_prov.listar_todos():
            print(p.id, p.nombre)

    def crear_proveedor(self):
        self.srv_prov.crear(Proveedor(
            int(input("ID: ")),
            input("Nombre: "),
            input("Contacto: ")
        ))

    def modificar_proveedor(self):
        p = self.srv_prov.obtener(int(input("ID: ")))
        p.nombre = input("Nuevo nombre: ") or p.nombre
        self.srv_prov.actualizar(p)

    def eliminar_proveedor(self):
        self.srv_prov.eliminar(int(input("ID: ")))

    # =========================================
    # ALMACENES
    # =========================================
    def listar_almacenes(self):
        for a in self.srv_alm.listar_todos():
            print(a.id, a.nombre)

    def crear_almacen(self):
        self.srv_alm.crear(Almacen(
            int(input("ID: ")),
            input("Nombre: "),
            input("Ubicación: ")
        ))

    def modificar_almacen(self):
        a = self.srv_alm.obtener(int(input("ID: ")))
        a.nombre = input("Nuevo nombre: ") or a.nombre
        self.srv_alm.actualizar(a)

    def eliminar_almacen(self):
        self.srv_alm.eliminar(int(input("ID: ")))

    # =========================================
    # MONEDAS
    # =========================================
    def listar_monedas(self):
        for m in self.srv_mon.listar_todos():
            print(m.id, m.nombre)

    def crear_moneda(self):
        self.srv_mon.crear(Moneda(
            int(input("ID: ")),
            input("Nombre: "),
            input("Código: ")
        ))

    def modificar_moneda(self):
        m = self.srv_mon.obtener(int(input("ID: ")))
        m.nombre = input("Nuevo nombre: ") or m.nombre
        self.srv_mon.actualizar(m)

    def eliminar_moneda(self):
        self.srv_mon.eliminar(int(input("ID: ")))

    # =========================================
    # TIPOS DE COTIZACIÓN
    # =========================================
    def listar_tipos(self):
        for t in self.srv_tipo.listar_todos():
            print(t.id, t.nombre)

    def crear_tipo(self):
        self.srv_tipo.crear(TipoCotizacion(
            int(input("ID: ")),
            input("Nombre: ")
        ))
        print("Tipo de cotización creado.")

    def modificar_tipo(self):
        t = self.srv_tipo.obtener(int(input("ID: ")))
        t.nombre = input("Nuevo nombre: ") or t.nombre
        self.srv_tipo.actualizar(t)
        print("Tipo de cotización actualizado.")

    def eliminar_tipo(self):
        self.srv_tipo.eliminar(int(input("ID: ")))
        print("Tipo de cotización eliminado.")

    # =========================================
    # COTIZACIONES
    # =========================================
    def registrar_cotizacion(self):
        id_cot = int(input("ID cotización: "))
        tipo = self.srv_tipo.obtener(int(input("ID tipo: ")))
        valor = float(input("Valor: "))
        fecha = datetime.date.today()

        self.srv_cot.crear(CotizacionDolar(valor, fecha, tipo, id=id_cot))
        print("Cotización registrada.")

    def modificar_cotizacion(self):
        cot = self.srv_cot.obtener(int(input("ID cotización: ")))

        nuevo_valor = input(f"Nuevo valor [{cot.valor}]: ")
        if nuevo_valor:
            cot.valor = float(nuevo_valor)

        print("Tipos disponibles:")
        self.listar_tipos()
        nuevo_tipo = input(f"Nuevo ID tipo [{cot.tipo.id}]: ")
        if nuevo_tipo:
            tipo = self.srv_tipo.obtener(int(nuevo_tipo))
            cot.tipo = tipo

        nueva_fecha = input(f"Nueva fecha [{cot.fecha}] (YYYY-MM-DD): ")
        if nueva_fecha:
            cot.fecha = datetime.datetime.strptime(nueva_fecha, "%Y-%m-%d").date()

        self.srv_cot.actualizar(cot)
        print("Cotización actualizada.")

    def eliminar_cotizacion(self):
        self.srv_cot.eliminar(int(input("ID cotización: ")))
        print("Cotización eliminada.")

    def historico_cotizaciones(self):
        for c in self.srv_cot.obtener_historico(int(input("ID tipo: "))):
            print(c.id, c.valor, c.fecha)

    def obtener_cotizaciones_api(self):
        """Obtiene cotizaciones desde la API y las registra."""

        cotizaciones = self.srv_cot.obtener_cotizaciones()

        print(
            f"Cotizaciones registradas desde API: {len(cotizaciones)}"
        )

    def ver_lista_precios_bimonetaria(self):
        """Muestra precios en pesos y en otra moneda seleccionada."""

        productos = self.srv_prod.listar_todos()
        monedas = self.srv_mon.listar_todos()

        print("Monedas disponibles:")

        for moneda in monedas:
            print(moneda.id, moneda.nombre, moneda.codigo)

        moneda_id = int(
            input("Seleccione ID de moneda destino: ")
        )

        moneda_destino = self.srv_mon.obtener(
            moneda_id
        )

        cotizaciones = self.srv_cot.listar_todos()

        cotizacion = next(
            (
                c for c in reversed(cotizaciones)
                if c.tipo.nombre.lower()
                == moneda_destino.nombre.lower()
            ),
            None
        )

        if not cotizacion:
            raise ValueError(
                "No existe cotización disponible para la moneda seleccionada."
            )

        print("\n=== LISTA DE PRECIOS BIMONETARIA ===")

        for producto in productos:

            precio_pesos = producto.precio.valor
            precio_convertido = precio_pesos / cotizacion.valor

            print(
                f"{producto.id} - {producto.nombre} | "
                f"ARS {precio_pesos:.2f} | "
                f"{moneda_destino.codigo} {precio_convertido:.2f}"
            )

    def exportar_precios_bimonetarios_csv(self):
        """Exporta precios en pesos y otras monedas a un archivo CSV."""

        productos = self.srv_prod.listar_todos()
        cotizaciones = self.srv_cot.listar_todos()

        ruta_salida = Path(
            "/content/price_manager/src/"
            "price_manager/migrations/csv/precios_bimonetarios.csv"
        )

        monedas = self.srv_mon.listar_todos()

        with open(
            ruta_salida,
            "w",
            encoding="utf-8",
            newline=""
        ) as archivo_csv:

            columnas = [
                "producto_id",
                "producto",
                "precio_pesos",
                "moneda",
                "precio_convertido"
            ]

            escritor = csv.DictWriter(
                archivo_csv,
                fieldnames=columnas
            )

            escritor.writeheader()

            for producto in productos:

                for moneda in monedas:

                    if moneda.codigo.upper() == "ARS":
                        continue

                    cotizacion = next(
                        (
                            c for c in reversed(cotizaciones)
                            if c.tipo.nombre.lower()
                            == moneda.nombre.lower()
                        ),
                        None
                    )

                    if not cotizacion:
                        continue

                    escritor.writerow(
                        {
                            "producto_id": producto.id,
                            "producto": producto.nombre,
                            "precio_pesos": producto.precio.valor,
                            "moneda": moneda.codigo,
                            "precio_convertido": (
                                producto.precio.valor
                                / cotizacion.valor
                            )
                        }
                    )

        print(
            f"Archivo exportado correctamente: {ruta_salida}"
        )


    # =========================================
    # FUNCIONALIDADES SPRINT 3
    # =========================================
    def _ruta_repositorio(self):
        """Obtiene la ruta raíz del repositorio."""

        return Path(__file__).resolve().parents[3]

    def _convertir_precio_web(self, precio_texto):
        """Convierte un precio web en formato texto a número."""

        precio_limpio = re.sub(
            r"[^0-9,\.]",
            "",
            str(precio_texto or "")
        )

        if not precio_limpio:
            return None

        precio_limpio = precio_limpio.replace(".", "")
        precio_limpio = precio_limpio.replace(",", ".")

        return float(precio_limpio)


    def ejecutar_scraping(self):
        """Ejecuta el scraper de Star Computación."""

        ruta_repo = self._ruta_repositorio()
        ruta_src = ruta_repo / "src"

        ruta_spider = (
            ruta_src
            / "price_manager"
            / "scraper"
            / "spiders"
            / "star_computacion_spider.py"
        )

        ruta_productos = (
            ruta_src
            / "price_manager"
            / "scraper"
            / "productos_busqueda.json"
        )

        if not ruta_spider.exists():
            raise FileNotFoundError(
                f"No se encontró el spider: {ruta_spider}"
            )

        if not ruta_productos.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo de productos: {ruta_productos}"
            )

        env = os.environ.copy()
        env["PYTHONPATH"] = str(ruta_src)

        comando = [
            "scrapy",
            "runspider",
            str(ruta_spider),
            "-a",
            f"productos_path={ruta_productos}"
        ]

        resultado = subprocess.run(
            comando,
            cwd=str(ruta_repo),
            env=env,
            capture_output=True,
            text=True,
            check=False
        )

        if resultado.returncode != 0:
            registrar_auditoria(
                "MENU_EJECUTAR_SCRAPING_ERROR",
                (resultado.stderr or "Error al ejecutar scraping.")[-500:]
            )

            raise RuntimeError(
                "No se pudo ejecutar el scraper."
            )

        registrar_auditoria(
            "MENU_EJECUTAR_SCRAPING",
            "Scraping ejecutado desde el menú de consola."
        )

        print("Scraping ejecutado correctamente.")
        print(
            "Archivo generado:",
            ruta_repo / "reports" / "star_computacion_resultados.json"
        )


    def generar_reporte(self):
        """Genera el reporte Excel de comparación de precios."""

        from openpyxl import Workbook

        ruta_repo = self._ruta_repositorio()

        ruta_resultados = (
            ruta_repo
            / "reports"
            / "star_computacion_resultados.json"
        )

        ruta_reporte = (
            ruta_repo
            / "reports"
            / "reporte_precios.xlsx"
        )

        if not ruta_resultados.exists():
            raise FileNotFoundError(
                "No se encontró el archivo de resultados del scraper."
            )

        resultados_web = json.loads(
            ruta_resultados.read_text(encoding="utf-8")
        )

        conexion = ConexionDB()

        with conexion.manejar_transaccion() as sesion:
            productos_db = sesion.execute(
                text(
                    """
                    SELECT nombre, precio
                    FROM productos
                    ORDER BY id
                    """
                )
            ).fetchall()

        productos_internos = {
            producto.nombre: float(producto.precio)
            for producto in productos_db
        }

        fecha_extraccion = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        filas = []

        for resultado in resultados_web:
            producto_buscado = resultado.get("producto_buscado")

            if producto_buscado not in productos_internos:
                continue

            precio_interno = productos_internos[producto_buscado]

            precio_web = self._convertir_precio_web(
                resultado.get("precio")
            )

            if precio_web is None:
                continue

            filas.append(
                [
                    producto_buscado,
                    resultado.get("nombre"),
                    precio_interno,
                    precio_web,
                    precio_web - precio_interno,
                    fecha_extraccion
                ]
            )

        ruta_reporte.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        workbook = Workbook()
        hoja = workbook.active
        hoja.title = "Reporte precios"

        hoja.append(
            [
                "Producto",
                "Producto web encontrado",
                "Precio interno",
                "Precio web",
                "Diferencia",
                "Fecha de extracción"
            ]
        )

        for fila in filas:
            hoja.append(fila)

        workbook.save(
            ruta_reporte
        )

        registrar_auditoria(
            "MENU_GENERAR_REPORTE",
            f"Reporte generado desde menú. Filas: {len(filas)}."
        )

        print("Reporte generado correctamente.")
        print("Archivo:", ruta_reporte)


    def ver_historial_auditoria(self):
        """Muestra los últimos registros de auditoría."""

        conexion = ConexionDB()

        with conexion.manejar_transaccion() as sesion:
            registros = sesion.execute(
                text(
                    """
                    SELECT id, accion, fecha, detalles
                    FROM auditorias
                    ORDER BY id DESC
                    LIMIT 20
                    """
                )
            ).fetchall()

        if not registros:
            print("No hay registros de auditoría.")
            return

        print("\n=== HISTORIAL DE AUDITORÍA ===")

        for registro in registros:
            print("-" * 80)
            print("ID:", registro.id)
            print("Acción:", registro.accion)
            print("Fecha:", registro.fecha)
            print("Detalles:", registro.detalles)

        registrar_auditoria(
            "MENU_VER_HISTORIAL_AUDITORIA",
            "Historial de auditoría consultado desde menú."
        )

