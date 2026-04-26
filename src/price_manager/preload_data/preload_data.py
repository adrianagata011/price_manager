
# =========================================
# PRECARGA DE DATOS INICIALES
# =========================================
# Este módulo se utiliza para garantizar una carga mínima de datos
# en las entidades maestras del sistema, tal como solicita la consigna.

from price_manager.entities.entities import (
    Categoria,
    Proveedor,
    Moneda,
    TipoCotizacion,
    Almacen
)


def cargar_datos_iniciales(srv_cat, srv_prov, srv_mon, srv_tipo, srv_alm):
    """
    Garantiza la precarga de 10 registros por entidad maestra.

    La idea de esta función es dejar disponibles datos iniciales
    para poder probar el sistema sin tener que cargar todo manualmente
    desde la interfaz.
    """

    # =========================================
    # 1. CATEGORÍAS
    # =========================================
    categorias = [
        "Procesadores",
        "Memorias RAM",
        "Almacenamiento",
        "Placas de Video",
        "Fuentes",
        "Gabinetes",
        "Monitores",
        "Teclados",
        "Mouses",
        "Audio"
    ]

    for i, nombre in enumerate(categorias, 1):
        if not srv_cat.obtener(i):
            srv_cat.crear(Categoria(i, nombre))

    # =========================================
    # 2. PROVEEDORES
    # =========================================
    proveedores = [
        "TechDistribuidora",
        "GlobalHardware",
        "StarImport",
        "MegaComponentes",
        "PCParts",
        "LogiWholesale",
        "SiliconValleySA",
        "DataSupply",
        "NanoTech",
        "HardWorld"
    ]

    for i, nombre in enumerate(proveedores, 1):
        if not srv_prov.obtener(i):
            srv_prov.crear(
                Proveedor(i, nombre, f"contacto_{i}@distribuidora.com")
            )

    # =========================================
    # 3. MONEDAS
    # =========================================
    # Aunque en un sistema real probablemente no harían falta tantas,
    # se cargan 10 registros para cumplir explícitamente con la consigna.
    monedas = [
        ("Peso Argentino", "ARS"),
        ("Dólar Estadounidense", "USD"),
        ("Euro", "EUR"),
        ("Real Brasileño", "BRL"),
        ("Peso Chileno", "CLP"),
        ("Peso Uruguayo", "UYU"),
        ("Guaraní", "PYG"),
        ("Boliviano", "BOB"),
        ("Sol Peruano", "PEN"),
        ("Peso Mexicano", "MXN")
    ]

    for i, (nombre, codigo) in enumerate(monedas, 1):
        if not srv_mon.obtener(i):
            srv_mon.crear(Moneda(i, nombre, codigo))

    # =========================================
    # 4. TIPOS DE COTIZACIÓN
    # =========================================
    tipos_cotizacion = [
        "Oficial",
        "Blue",
        "Tarjeta",
        "MEP",
        "CCL",
        "Cripto",
        "Mayorista",
        "Lujo",
        "Turista",
        "Ahorro"
    ]

    for i, nombre in enumerate(tipos_cotizacion, 1):
        if not srv_tipo.obtener(i):
            srv_tipo.crear(TipoCotizacion(i, nombre))

    # =========================================
    # 5. ALMACENES
    # =========================================
    # Se agregan 10 almacenes para cubrir el modelo Producto-Stock-Almacén.
    for i in range(1, 11):
        if not srv_alm.obtener(i):
            srv_alm.crear(
                Almacen(
                    i,
                    f"Depósito Central {i}",
                    f"Zona Industrial Sector {i}"
                )
            )

    print("Precarga completada: se verificaron y cargaron 10 registros por cada entidad maestra.")
