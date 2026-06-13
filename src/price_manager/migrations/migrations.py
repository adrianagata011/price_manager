import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import text

from price_manager.database.connection import ConexionDB
from price_manager.models.models import (
    AlmacenModel,
    Base,
    CategoriaModel,
    CotizacionModel,
    MonedaModel,
    ProductoModel,
    ProveedorModel,
    StockModel,
    TipoCotizacionModel
)
from price_manager.auditoria.auditoria import auditar_operacion


def _valor_sql(valor: Any) -> str:
  """Convierte un valor de Python a formato compatible con SQL."""

  if valor is None:
    return "NULL"

  if isinstance(valor, str):
    valor_limpio = valor.replace("'", "''")
    return f"'{valor_limpio}'"

  return str(valor)


def _generar_insert(
    tabla: str,
    fila: dict[str, str]
) -> str:
  """Genera una sentencia INSERT a partir de una fila CSV."""

  columnas = ", ".join(fila.keys())

  valores = ", ".join(
      _valor_sql(valor)
      for valor in fila.values()
  )

  return (
      f"INSERT INTO {tabla} "
      f"({columnas}) VALUES ({valores});"
  )


@auditar_operacion("MIGRAR_DATOS_CSV_SQL")
def migrar_datos(
    carpeta_csvs: str,
    carpeta_sqls: str
) -> None:
  """
  Migra datos desde CSV hacia la base relacional.

  También genera archivos .sql con las sentencias INSERT
  correspondientes a cada archivo procesado.

  Args:
    carpeta_csvs:
      Ruta donde se encuentran los archivos CSV.

    carpeta_sqls:
      Ruta donde se guardarán los archivos SQL generados.
  """

  conexion = ConexionDB()

  carpeta_csvs_path = Path(carpeta_csvs)
  carpeta_sqls_path = Path(carpeta_sqls)

  carpeta_sqls_path.mkdir(
      parents=True,
      exist_ok=True
  )

  Base.metadata.drop_all(
      conexion.engine
  )

  Base.metadata.create_all(
      conexion.engine
  )

  orden_migracion = [
      "categorias.csv",
      "proveedores.csv",
      "almacenes.csv",
      "monedas.csv",
      "tipos_cotizacion.csv",
      "productos.csv",
      "stock.csv",
      "cotizaciones.csv"
  ]

  with conexion.manejar_transaccion() as sesion:

    for nombre_archivo in orden_migracion:

      archivo_csv = carpeta_csvs_path / nombre_archivo

      if not archivo_csv.exists():
        print(f"No se encontró el archivo {nombre_archivo}.")
        continue

      tabla = archivo_csv.stem
      inserts_sql = []

      with open(
          archivo_csv,
          "r",
          encoding="utf-8"
      ) as csv_file:

        lector = csv.DictReader(csv_file)

        for fila in lector:

          inserts_sql.append(
              _generar_insert(
                  tabla,
                  fila
              )
          )

          if tabla == "categorias":
            sesion.add(
                CategoriaModel(
                    id=int(fila["id"]),
                    nombre=fila["nombre"]
                )
            )

          elif tabla == "proveedores":
            sesion.add(
                ProveedorModel(
                    id=int(fila["id"]),
                    nombre=fila["nombre"],
                    contacto=fila["contacto"]
                )
            )

          elif tabla == "almacenes":
            sesion.add(
                AlmacenModel(
                    id=int(fila["id"]),
                    nombre=fila["nombre"],
                    ubicacion=fila["ubicacion"]
                )
            )

          elif tabla == "monedas":
            sesion.add(
                MonedaModel(
                    id=int(fila["id"]),
                    nombre=fila["nombre"],
                    codigo=fila["codigo"]
                )
            )

          elif tabla == "tipos_cotizacion":
            sesion.add(
                TipoCotizacionModel(
                    id=int(fila["id"]),
                    nombre=fila["nombre"]
                )
            )

          elif tabla == "productos":
            sesion.add(
                ProductoModel(
                    id=int(fila["id"]),
                    nombre=fila["nombre"],
                    descripcion=fila["descripcion"],
                    precio=float(fila["precio"]),
                    moneda_id=int(fila["moneda_id"]),
                    cat_id=int(fila["cat_id"]),
                    prov_id=int(fila["prov_id"])
                )
            )

          elif tabla == "stock":
            sesion.add(
                StockModel(
                    producto_id=int(fila["producto_id"]),
                    almacen_id=int(fila["almacen_id"]),
                    cantidad=int(fila["cantidad"])
                )
            )

          elif tabla == "cotizaciones":
            sesion.add(
                CotizacionModel(
                    id=int(fila["id"]),
                    valor=float(fila["valor"]),
                    fecha=datetime.strptime(
                        fila["fecha"],
                        "%Y-%m-%d"
                    ),
                    tipo_id=int(fila["tipo_id"])
                )
            )

      archivo_sql = carpeta_sqls_path / f"{tabla}.sql"

      with open(
          archivo_sql,
          "w",
          encoding="utf-8"
      ) as sql_file:

        sql_file.write(
            "\n".join(inserts_sql)
        )

      print(f"Migración completada: {nombre_archivo}")


@auditar_operacion("CARGA_DATOS_SQL")
def cargar_datos_desde_sql(
    carpeta_sqls: str,
    reiniciar_base: bool = True
) -> None:
  """
  Carga los datos iniciales desde archivos SQL.

  Args:
    carpeta_sqls:
      Ruta donde están los archivos .sql.

    reiniciar_base:
      Indica si la base debe recrearse antes de cargar los datos.
  """

  conexion = ConexionDB()
  carpeta_sqls_path = Path(carpeta_sqls)

  if not carpeta_sqls_path.exists():
    raise FileNotFoundError(
        f"No se encontró la carpeta SQL: {carpeta_sqls_path}"
    )

  if reiniciar_base:
    Base.metadata.drop_all(
        conexion.engine
    )

    Base.metadata.create_all(
        conexion.engine
    )

  orden_sql = [
      "categorias.sql",
      "proveedores.sql",
      "almacenes.sql",
      "monedas.sql",
      "tipos_cotizacion.sql",
      "productos.sql",
      "stock.sql",
      "cotizaciones.sql"
  ]

  with conexion.manejar_transaccion() as sesion:

    for nombre_archivo in orden_sql:

      archivo_sql = carpeta_sqls_path / nombre_archivo

      if not archivo_sql.exists():
        print(f"No se encontró el archivo {nombre_archivo}.")
        continue

      contenido_sql = archivo_sql.read_text(
          encoding="utf-8"
      ).strip()

      if not contenido_sql:
        print(f"El archivo {nombre_archivo} está vacío.")
        continue

      sentencias = [
          sentencia.strip()
          for sentencia in contenido_sql.split(";")
          if sentencia.strip()
      ]

      for sentencia in sentencias:
        sesion.execute(
            text(sentencia)
        )

      print(f"Carga completada: {nombre_archivo}")
