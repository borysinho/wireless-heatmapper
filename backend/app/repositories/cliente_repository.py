"""Repositorio de acceso a datos para la entidad Cliente.

Sprint 1 — PB-19 (Sp1-31): CRUD básico de clientes para el admin.
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def listar_activos(self) -> list[Cliente]:
        """Retorna todos los clientes con activo=True, ordenados por nombre."""
        return (
            self._db.query(Cliente)
            .filter(Cliente.activo.is_(True))
            .order_by(Cliente.nombre)
            .all()
        )

    def listar_todos(self) -> list[Cliente]:
        """Retorna todos los clientes (incluye inactivos). Uso exclusivo del admin."""
        return self._db.query(Cliente).order_by(Cliente.nombre).all()

    def obtener_por_id(self, cliente_id: int) -> Cliente | None:
        return self._db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def crear(self, nombre: str, email_referencia: str | None = None) -> Cliente:
        """Crea un cliente nuevo. Lanza IntegrityError si el nombre ya existe."""
        cliente = Cliente(
            nombre=nombre.strip(),
            email_referencia=email_referencia.strip() if email_referencia else None,
        )
        self._db.add(cliente)
        self._db.flush()
        self._db.refresh(cliente)
        return cliente

    def actualizar(
        self,
        cliente: Cliente,
        *,
        nombre: str | None = None,
        email_referencia: str | None = None,
        actualizar_email_referencia: bool = False,
        activo: bool | None = None,
    ) -> Cliente:
        if nombre is not None:
            cliente.nombre = nombre.strip()
        if actualizar_email_referencia:
            cliente.email_referencia = (
                email_referencia.strip() if email_referencia else None
            )
        if activo is not None:
            cliente.activo = activo
        self._db.flush()
        self._db.refresh(cliente)
        return cliente
