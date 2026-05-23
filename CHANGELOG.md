# CHANGELOG

## [2026-05-19 23:46] - Inicio Sprint_2

### Configuración inicial
- Se configuró el entorno de trabajo en Google Colab.
- Se agregó autenticación segura mediante token GitHub.
- Se configuró el repositorio remoto del proyecto.
- Se clonó el repositorio price_manager.
- Se creó y verificó la rama Sprint_2.
- Se configuró el entorno PYTHONPATH del proyecto.

## [2026-05-20 21:20] - Ejercicio 01

### Estructura inicial Sprint_2
- Se crearon los directorios database y models.
- Se creó la estructura de migrations/csv y migrations/sql.
- Se agregaron archivos __init__.py para modularización.
- Se verificó la estructura inicial del proyecto.

## [2026-05-21 09:55] - Ejercicios 02 al 05

### Configuración de base de datos
- Se implementó la clase ConexionDB utilizando SQLAlchemy.
- Se configuró el engine SQLite del proyecto.
- Se implementó la creación y manejo de sesiones.

### Manejo de transacciones
- Se agregó un context manager para administración segura de transacciones.
- Se implementó commit, rollback y cierre automático de sesiones.

### Modelos ORM
- Se crearon los modelos ORM del sistema.
- Se configuraron relaciones entre tablas mediante foreign keys.
- Se verificó la creación automática de tablas relacionales.

### Migración de datos
- Se implementó la función migrar_datos().
- Se realizó la lectura de archivos CSV del Sprint_1.
- Se generaron sentencias SQL de inserción.
- Se almacenaron archivos .sql dentro de migrations/sql.
- Se verificó la migración de datos hacia SQLite.


## [2026-05-21 23:27] - Ejercicio 06

### Integración de repositorios con SQLite
- Se refactorizaron los repositorios del sistema para utilizar SQLite mediante SQLAlchemy.
- Se implementaron operaciones CRUD utilizando modelos ORM.
- Se incorporó manejo transaccional mediante ConexionDB.
- Se agregaron conversiones entre modelos ORM y entidades del dominio.
- Se verificó la lectura de datos persistidos desde la base relacional.


## [2026-05-23 00:18] - Ejercicio 07

### API del dólar y dotenv
- Se creó el archivo .env para configuración externa de la API.
- Se incorporó soporte para python-dotenv.
- Se integró la API pública de cotizaciones del dólar.
- Se implementó el método obtener_cotizaciones().
- Se registraron cotizaciones automáticamente en SQLite.
- Se verificó la descarga y persistencia de cotizaciones.
