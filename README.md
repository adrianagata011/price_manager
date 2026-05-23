# Price Manager System - Sprint 2

## Objetivo

Ampliar el sistema Price Manager para que la información del proyecto
se persista en una base de datos relacional utilizando SQLAlchemy.

## Introducción y contexto

Este sprint continúa el desarrollo iniciado en Sprint 1. En la primera
entrega se trabajó sobre una estructura orientada a objetos, repositorios,
servicios, interfaz por consola y persistencia inicial mediante archivos CSV.

En Sprint 2 se incorporó una base de datos SQLite administrada mediante
SQLAlchemy, permitiendo migrar los datos cargados en archivos CSV hacia
tablas relacionales. Además, se agregó integración con una API externa para
obtener cotizaciones del dólar y nuevas opciones de menú para consultar y
exportar precios bimonetarios.

## Funcionalidades principales

- Conexión a base de datos mediante SQLAlchemy.
- Manejo de sesiones y transacciones.
- Modelos ORM con relaciones entre tablas.
- Migración de datos desde CSV hacia SQLite.
- Generación de archivos SQL con sentencias INSERT.
- Repositorios adaptados para trabajar con base de datos.
- Integración con API externa de cotizaciones.
- Uso de archivo .env para configuración.
- Nuevas opciones de menú para cotizaciones y precios bimonetarios.

## Estructura principal

price_manager/
├── database/
├── entities/
├── models/
├── repositories/
├── services/
├── migrations/
│   ├── csv/
│   └── sql/
├── ui/
└── main.py

## Ejecución

from price_manager.main import main

main(import_default_data=False)

## Sprint actual

Sprint 2.