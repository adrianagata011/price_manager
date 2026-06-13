from datetime import datetime
from functools import wraps

from price_manager.database.connection import ConexionDB
from price_manager.models.models import AuditoriaModel, Base


def _resumir_argumentos(args, kwargs) -> str:
  """Genera un resumen simple de los argumentos recibidos."""

  argumentos = []

  if len(args) > 1:
    argumentos.append(
        f"args={args[1:]}"
    )

  if kwargs:
    argumentos.append(
        f"kwargs={kwargs}"
    )

  resumen = " | ".join(argumentos)

  if len(resumen) > 250:
    resumen = resumen[:250] + "..."

  return resumen or "Sin argumentos adicionales"


def registrar_auditoria(accion: str, detalles: str) -> None:
  """Registra una operación en la tabla auditorias."""

  conexion = ConexionDB()

  Base.metadata.create_all(
      conexion.engine
  )

  with conexion.manejar_transaccion() as sesion:
    sesion.add(
        AuditoriaModel(
            accion=accion,
            fecha=datetime.now(),
            detalles=detalles[:500]
        )
    )


def auditar_operacion(accion: str):
  """Decorador para auditar operaciones del sistema."""

  def decorador(funcion):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
      resumen_argumentos = _resumir_argumentos(
          args,
          kwargs
      )

      try:
        resultado = funcion(
            *args,
            **kwargs
        )

        registrar_auditoria(
            accion=accion,
            detalles=(
                f"Operación ejecutada correctamente. "
                f"Función: {funcion.__name__}. "
                f"{resumen_argumentos}"
            )
        )

        return resultado

      except Exception as error:
        registrar_auditoria(
            accion=f"{accion}_ERROR",
            detalles=(
                f"Error al ejecutar la operación. "
                f"Función: {funcion.__name__}. "
                f"{resumen_argumentos}. "
                f"Error: {error}"
            )
        )

        raise

    return wrapper

  return decorador
