from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class ConexionDB:
  """Administra la conexión y las transacciones de base de datos."""

  def __init__(
      self,
      database_url: Optional[str] = None
  ) -> None:
    """
    Inicializa la conexión SQLite del sistema.

    Args:
      database_url:
        URL opcional de conexión.
    """

    base_path = Path(__file__).resolve().parents[2]
    db_path = base_path / "price_manager.db"

    self._database_url = (
        database_url
        or f"sqlite:///{db_path}"
    )

    self._engine: Engine = create_engine(
        self._database_url,
        echo=False,
        future=True
    )

    self._session_factory = sessionmaker(
        bind=self._engine,
        autoflush=False,
        autocommit=False,
        future=True
    )

  @property
  def database_url(self) -> str:
    """Devuelve la URL de conexión."""

    return self._database_url

  @property
  def engine(self) -> Engine:
    """Devuelve el engine de SQLAlchemy."""

    return self._engine

  def crear_sesion(self) -> Session:
    """Crea una nueva sesión de base de datos."""

    return self._session_factory()

  @contextmanager
  def manejar_transaccion(self) -> Iterator[Session]:
    """
    Administra una transacción de base de datos.

    Si las operaciones finalizan correctamente, confirma los cambios.
    Si ocurre un error, revierte la transacción y propaga la excepción.
    Al finalizar, cierra siempre la sesión.
    """

    sesion = self.crear_sesion()

    try:
      yield sesion
      sesion.commit()

    except Exception:
      sesion.rollback()
      raise

    finally:
      sesion.close()
