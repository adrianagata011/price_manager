# Price Manager System - Sprint 1

## Información Académica
- **Alumnos:** Adrián Agata, 
- **Materia:** Seminario de Actualización
- **Profesores:** Gabriel Orlando Gosparo, Fabricio Pasinato
- **Universidad:** Universidad del Gran Rosario
- **Fecha:** 25/04/2026

---

## Descripción del Proyecto
**Price Manager** es un sistema orientado a la gestión de productos, precios y stock, desarrollado bajo un enfoque modular.

El objetivo principal fue implementar una solución funcional que permita operar las entidades del sistema mediante un CRUD completo, incorporando validaciones de negocio y persistencia de datos.

---

## Objetivos del Sprint 1
En esta etapa se trabajó sobre la base del sistema:

- Definición del modelo de dominio
- Implementación de persistencia en archivos CSV
- Desarrollo de lógica de negocio mediante servicios
- Construcción de una interfaz de usuario por consola
- Implementación de operaciones CRUD sobre todas las entidades
- Manejo de stock con validaciones
- Registro de cotizaciones con histórico

---

## Arquitectura del Sistema

El sistema se organiza en capas para separar responsabilidades:

```
[ UI - Console ]
↓
[ Servicios ]
↓
[ Repositorios ]
↓
[ Archivos CSV ]
↑
[ Entidades ]
```

### Descripción de capas

- **Entidades**
  Representan el modelo del dominio y contienen validaciones básicas.

- **Repositorios**
  Gestionan la persistencia en archivos CSV.

- **Servicios**
  Implementan la lógica de negocio y validaciones más complejas.

- **UI (Consola)**
  Permite interactuar con el sistema y ejecutar operaciones CRUD.

---

## Estructura del Proyecto

```
price_manager/
│
├── src/price_manager/
│ ├── entities/ # Modelo de dominio
│ ├── repositories/ # Persistencia CSV
│ ├── services/ # Lógica de negocio
│ ├── ui/ # Interfaz por consola
│ ├── preload_data/ # Precarga de datos
│ └── migrations/csv/ # Archivos CSV
│
└── main.py # Punto de entrada
```

---

## Principales Funcionalidades

- Gestión de productos (alta, modificación, baja, consulta)
- Gestión de categorías y proveedores
- Manejo de stock por producto y almacén
- Registro de movimientos de stock (ingresos/egresos)
- Gestión de monedas
- Registro y consulta de cotizaciones
- Consulta de histórico de cotizaciones

---

## Decisiones de Diseño

---

## Cómo ejecutar el sistema

