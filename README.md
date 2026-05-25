# Price Manager System - Sprint 2

## Información Académica

- **Grupo:** Grupo 2
- **Materia:** Seminario de Actualización
- **Profesores:** Gabriel Orlando Gosparo, Fabricio Pasinato
- **Universidad:** Universidad del Gran Rosario

---

## Objetivo

Ampliar el sistema Price Manager para que la información del proyecto
se persista en una base de datos relacional utilizando SQLAlchemy.

---

## Introducción y contexto

Este sprint continúa el desarrollo iniciado en Sprint 1. En la primera
entrega se trabajó sobre una estructura orientada a objetos, repositorios,
servicios, interfaz por consola y persistencia inicial mediante archivos CSV.

En Sprint 2 se incorporó una base de datos SQLite administrada mediante
SQLAlchemy, permitiendo migrar los datos cargados en archivos CSV hacia
tablas relacionales. Además, se agregó integración con una API externa para
obtener cotizaciones del dólar y nuevas opciones de menú para consultar y
exportar precios bimonetarios.

---

## Arquitectura del Sistema

El sistema mantiene una arquitectura organizada en capas:

``` Text
[ UI - Console ]
↓
[ Servicios ]
↓
[ Repositorios ]
↓
[ SQLite + SQLAlchemy ]
↑
[ Entidades / ORM ]
```

### Descripción de capas

- **Entidades**
  Representan el dominio principal del sistema.

- **Modelos ORM**
  Permiten mapear entidades hacia tablas relacionales.

- **Repositorios**
  Gestionan operaciones CRUD utilizando SQLAlchemy.

- **Servicios**
  Implementan lógica de negocio y validaciones.

- **UI**
  Interfaz por consola para operar el sistema.

---

## Principales funcionalidades

- Conexión a base de datos mediante SQLAlchemy.
- Manejo de sesiones y transacciones.
- Modelos ORM con relaciones entre tablas.
- Migración de datos desde CSV hacia SQLite.
- Generación de archivos SQL con sentencias INSERT.
- Repositorios adaptados para trabajar con base de datos.
- Integración con API externa de cotizaciones.
- Uso de archivo .env para configuración.
- Exportación de precios bimonetarios.
- Visualización de precios en múltiples monedas.

---

## Decisiones de diseño

- Se utilizó SQLite por simplicidad y portabilidad.
- Se mantuvo la separación por capas del Sprint 1.
- Se utilizó SQLAlchemy ORM para desacoplar persistencia.
- Se mantuvieron entidades separadas de modelos ORM.
- Se integró una API pública para obtener cotizaciones reales.

---

## Estructura principal

``` Text
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
```

---

## Cómo clonar el repositorio

git clone -b Sprint_2 https://github.com/adrianagata011/price_manager.git

---

## Cómo ejecutar el sistema

from price_manager.main import main

main(import_default_data=False)

---

## Sprint actual

Sprint 2.

Modificación realizada por Matias Diaz para revisión del Sprint 2.