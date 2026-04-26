
# =========================================
# ARCHIVO PRINCIPAL DEL SISTEMA
# =========================================
# Este archivo actúa como punto de entrada del proyecto.
# Se encarga de instanciar repositorios, servicios, realizar la
# precarga opcional de datos y lanzar la interfaz de usuario.

from price_manager.repositories.repositories import (
    RepositorioCategoria,
    RepositorioProveedor,
    RepositorioAlmacen,
    RepositorioMoneda,
    RepositorioTipoCotizacion,
    RepositorioProducto,
    RepositorioStock,
    RepositorioCotizacionDolar
)

from price_manager.services.services import (
    ServicioCategoria,
    ServicioProveedor,
    ServicioAlmacen,
    ServicioMoneda,
    ServicioTipoCotizacion,
    ServicioProducto,
    ServicioStock,
    ServicioCotizacionDolar
)

from price_manager.preload_data.preload_data import cargar_datos_iniciales
from price_manager.ui.console import ConsoleUI


def main(import_default_data: bool = False):
    """
    Punto de entrada principal del sistema.

    Se realiza la inyección de dependencias entre repositorios y servicios,
    y luego se lanza la interfaz de usuario.
    """

    # =========================================
    # 1. INSTANCIACIÓN DE REPOSITORIOS
    # =========================================
    repo_cat = RepositorioCategoria()
    repo_prov = RepositorioProveedor()
    repo_alm = RepositorioAlmacen()
    repo_mon = RepositorioMoneda()
    repo_tipo_cot = RepositorioTipoCotizacion()
    repo_prod = RepositorioProducto()
    repo_stock = RepositorioStock()
    repo_cot = RepositorioCotizacionDolar()

    # =========================================
    # 2. INSTANCIACIÓN DE SERVICIOS
    # =========================================
    srv_cat = ServicioCategoria(repo_cat)
    srv_prov = ServicioProveedor(repo_prov)
    srv_alm = ServicioAlmacen(repo_alm)
    srv_mon = ServicioMoneda(repo_mon)
    srv_tipo_cot = ServicioTipoCotizacion(repo_tipo_cot)
    srv_prod = ServicioProducto(repo_prod, srv_cat, srv_prov)
    srv_stock = ServicioStock(repo_stock, srv_prod, srv_alm)
    srv_cot = ServicioCotizacionDolar(repo_cot, srv_tipo_cot)

    # =========================================
    # 3. PRECARGA DE DATOS
    # =========================================
    # Si se solicita, se cargan datos iniciales para facilitar
    # las pruebas del sistema y cumplir con la consigna.
    if import_default_data:
        try:
            cargar_datos_iniciales(
                srv_cat,
                srv_prov,
                srv_mon,
                srv_tipo_cot,
                srv_alm
            )
        except Exception as e:
            print(f"Aviso: no se pudieron cargar los datos iniciales: {e}")

    # =========================================
    # 4. LANZAMIENTO DE LA INTERFAZ
    # =========================================
    ui = ConsoleUI(
        srv_prod,
        srv_cat,
        srv_prov,
        srv_stock,
        srv_alm,
        srv_mon,
        srv_tipo_cot,
        srv_cot
    )
    ui.ejecutar()


if __name__ == "__main__":
    # En ejecución directa no se fuerza la importación automática
    # de datos, aunque puede activarse cambiando el parámetro.
    main()
