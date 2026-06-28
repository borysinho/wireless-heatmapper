"""Endpoints de enlaces públicos para cliente.

Sprint 6 — PB-15/PB-16/PB-17.
"""

from __future__ import annotations

import hashlib
import hmac
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.v1.heatmaps import _conjunto_out, _generar_heatmap_core, _mapa_out
from app.api.v1.planos import _firmar as _firmar_plano
from app.core.config import settings
from app.core.database import get_db
from app.core.security import require_admin
from app.models.cliente import Cliente
from app.models.heatmap import ConjuntoAP, MapaCalor
from app.models.plano import Plano
from app.models.proyecto import Proyecto
from app.models.share import TokenEnlaceCliente
from app.models.usuario import Usuario
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.heatmap import GenerarHeatmapConjuntoIn, MapaCalorOut
from app.schemas.plano import PlanoOut
from app.schemas.share import (
    ContenidoEnlaceIn,
    EnlaceClienteActualizarIn,
    EnlaceClienteCrearIn,
    EnlaceClienteEnviarCorreoIn,
    EnlaceClienteEnviarCorreoOut,
    EnlaceClienteOut,
    PortalClienteOut,
    ProyectoPortalOut,
)
from app.services.email_service import EmailDeliveryError, EmailService

router = APIRouter(prefix="/share", tags=["portal-cliente"])


def _generar_token() -> str:
    base = str(uuid.uuid4())
    firma = hmac.new(
        settings.storage_url_secret.encode("utf-8"),
        base.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{base}.{firma}"


def _token_valido_formato(token: str) -> bool:
    partes = token.split(".")
    if len(partes) != 2:
        return False
    base, firma = partes
    esperada = hmac.new(
        settings.storage_url_secret.encode("utf-8"),
        base.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(esperada, firma)


def _url_publica(token: str) -> str:
    return f"/portal/{token}"


def _origen_publico(request: Request) -> str:
    if settings.public_web_url:
        return settings.public_web_url.rstrip("/")
    proto = request.headers.get("x-forwarded-proto") or request.url.scheme
    host = request.headers.get("host") or request.url.netloc
    return f"{proto}://{host}".rstrip("/")


def _url_publica_absoluta(token: str, request: Request) -> str:
    return f"{_origen_publico(request)}{_url_publica(token)}"


def _contenido_dict(contenido: ContenidoEnlaceIn) -> dict:
    return {
        "conjunto_ids": list(dict.fromkeys(contenido.conjunto_ids)),
        "mapa_ids": list(dict.fromkeys(contenido.mapa_ids)),
    }


def _contenido_from_model(enlace: TokenEnlaceCliente) -> ContenidoEnlaceIn:
    return ContenidoEnlaceIn(**(enlace.contenido or {}))


def _asegurar_utc(valor: datetime) -> datetime:
    if valor.tzinfo is None:
        return valor.replace(tzinfo=UTC)
    return valor.astimezone(UTC)


def _enlace_out(enlace: TokenEnlaceCliente) -> EnlaceClienteOut:
    return EnlaceClienteOut(
        id=enlace.id,
        proyecto_id=enlace.proyecto_id,
        url_publica=_url_publica(enlace.token),
        expira_en=enlace.expira_en,
        revocado=enlace.revocado,
        accesos=enlace.accesos,
        ultimo_acceso=enlace.ultimo_acceso,
        ip_ultimo_acceso=enlace.ip_ultimo_acceso,
        contenido=_contenido_from_model(enlace),
        created_at=enlace.created_at,
    )


def _cliente_destino_correo(*, cliente_id: int, db: Session) -> Cliente:
    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id, Cliente.activo.is_(True))
        .first()
    )
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )
    if not cliente.email_referencia:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El cliente seleccionado no tiene correo de referencia registrado.",
        )
    return cliente


def _asegurar_correo_configurado(email_service: EmailService) -> None:
    if not email_service.habilitado:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El correo transaccional no está configurado.",
        )


def _enviar_correo_enlace_cliente(
    *,
    enlace: TokenEnlaceCliente,
    proyecto: Proyecto,
    cliente: Cliente,
    request: Request,
    email_service: EmailService,
) -> EnlaceClienteEnviarCorreoOut:
    _asegurar_correo_configurado(email_service)
    try:
        enviado = email_service.enviar_enlace_cliente(
            destinatario=cliente.email_referencia,
            nombre_proyecto=proyecto.nombre,
            cliente=cliente.nombre,
            url_publica=_url_publica_absoluta(enlace.token, request),
            expira_en=enlace.expira_en,
        )
    except EmailDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo enviar el correo.",
        ) from exc
    if not enviado:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El correo transaccional no está configurado.",
        )
    return EnlaceClienteEnviarCorreoOut(
        enlace_id=enlace.id,
        destinatario=cliente.email_referencia,
        enviado=True,
    )


def _proyecto_admin(
    *, proyecto_id: int, current_user: Usuario, db: Session
) -> Proyecto:
    proyecto = ProyectoRepository(db).obtener_por_id_admin(proyecto_id=proyecto_id)
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return proyecto


def _validar_contenido(
    *, proyecto: Proyecto, contenido: ContenidoEnlaceIn, db: Session
) -> ContenidoEnlaceIn:
    plano_ids = {plano.id for plano in proyecto.planos}
    mapa_ids = set(contenido.mapa_ids)
    conjunto_ids = set(contenido.conjunto_ids)

    contenido = ContenidoEnlaceIn(
        conjunto_ids=sorted(conjunto_ids),
        mapa_ids=sorted(mapa_ids),
    )

    conjuntos = (
        db.query(ConjuntoAP).filter(ConjuntoAP.id.in_(contenido.conjunto_ids)).all()
        if contenido.conjunto_ids
        else []
    )
    if {item.id for item in conjuntos} != set(contenido.conjunto_ids) or any(
        item.plano_id not in plano_ids for item in conjuntos
    ):
        raise HTTPException(
            status_code=422,
            detail="Conjunto no pertenece al proyecto.",
        )
    mapas = (
        db.query(MapaCalor).filter(MapaCalor.id.in_(contenido.mapa_ids)).all()
        if contenido.mapa_ids
        else []
    )
    if {item.id for item in mapas} != set(contenido.mapa_ids) or any(
        item.plano_id not in plano_ids for item in mapas
    ):
        raise HTTPException(status_code=422, detail="Mapa no pertenece al proyecto.")

    return ContenidoEnlaceIn(**_contenido_dict(contenido))


def _obtener_enlace_publico(
    *, token: str, db: Session, request: Request | None = None
) -> TokenEnlaceCliente:
    if not _token_valido_formato(token):
        raise HTTPException(status_code=404, detail="Enlace no válido o expirado.")
    enlace = (
        db.query(TokenEnlaceCliente).filter(TokenEnlaceCliente.token == token).first()
    )
    ahora = datetime.now(UTC)
    if enlace is None or enlace.revocado or _asegurar_utc(enlace.expira_en) < ahora:
        raise HTTPException(status_code=404, detail="Enlace no válido o expirado.")
    if request is not None:
        enlace.accesos += 1
        enlace.ultimo_acceso = ahora
        enlace.ip_ultimo_acceso = request.client.host if request.client else None
        db.commit()
        db.refresh(enlace)
    return enlace


@router.post(
    "/proyectos/{proyecto_id}/enlaces",
    response_model=EnlaceClienteOut,
    status_code=status.HTTP_201_CREATED,
)
def crear_enlace_cliente(
    proyecto_id: int,
    body: EnlaceClienteCrearIn,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
) -> EnlaceClienteOut:
    proyecto = _proyecto_admin(
        proyecto_id=proyecto_id,
        current_user=current_user,
        db=db,
    )
    contenido = _validar_contenido(
        proyecto=proyecto,
        contenido=body.contenido,
        db=db,
    )
    cliente_destino: Cliente | None = None
    email_service = EmailService()
    if body.cliente_id is not None:
        cliente_destino = _cliente_destino_correo(
            cliente_id=body.cliente_id,
            db=db,
        )
        _asegurar_correo_configurado(email_service)
    enlace = TokenEnlaceCliente(
        proyecto_id=proyecto.id,
        token=_generar_token(),
        contenido=_contenido_dict(contenido),
        expira_en=datetime.now(UTC) + timedelta(days=body.expira_en_dias),
        creado_por_id=current_user.id,
    )
    db.add(enlace)
    db.commit()
    db.refresh(enlace)
    if cliente_destino is not None:
        _enviar_correo_enlace_cliente(
            enlace=enlace,
            proyecto=proyecto,
            cliente=cliente_destino,
            request=request,
            email_service=email_service,
        )
    return _enlace_out(enlace)


@router.get("/proyectos/{proyecto_id}/enlaces", response_model=list[EnlaceClienteOut])
def listar_enlaces_cliente(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
) -> list[EnlaceClienteOut]:
    proyecto = _proyecto_admin(
        proyecto_id=proyecto_id,
        current_user=current_user,
        db=db,
    )
    enlaces = (
        db.query(TokenEnlaceCliente)
        .filter(TokenEnlaceCliente.proyecto_id == proyecto.id)
        .order_by(TokenEnlaceCliente.created_at.desc(), TokenEnlaceCliente.id.desc())
        .all()
    )
    return [_enlace_out(enlace) for enlace in enlaces]


@router.patch("/enlaces/{enlace_id}", response_model=EnlaceClienteOut)
def actualizar_enlace_cliente(
    enlace_id: int,
    body: EnlaceClienteActualizarIn,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
) -> EnlaceClienteOut:
    enlace = (
        db.query(TokenEnlaceCliente).filter(TokenEnlaceCliente.id == enlace_id).first()
    )
    if enlace is None:
        raise HTTPException(status_code=404, detail="Enlace no encontrado.")
    _proyecto_admin(proyecto_id=enlace.proyecto_id, current_user=current_user, db=db)
    enlace.revocado = body.revocado
    db.commit()
    db.refresh(enlace)
    return _enlace_out(enlace)


@router.post(
    "/enlaces/{enlace_id}/correo",
    response_model=EnlaceClienteEnviarCorreoOut,
    summary="Enviar enlace existente por correo",
)
def enviar_correo_enlace_cliente(
    enlace_id: int,
    body: EnlaceClienteEnviarCorreoIn,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
) -> EnlaceClienteEnviarCorreoOut:
    enlace = (
        db.query(TokenEnlaceCliente).filter(TokenEnlaceCliente.id == enlace_id).first()
    )
    if enlace is None:
        raise HTTPException(status_code=404, detail="Enlace no encontrado.")
    proyecto = _proyecto_admin(
        proyecto_id=enlace.proyecto_id,
        current_user=current_user,
        db=db,
    )
    ahora = datetime.now(UTC)
    if enlace.revocado:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede enviar un enlace revocado.",
        )
    if _asegurar_utc(enlace.expira_en) < ahora:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede enviar un enlace expirado.",
        )
    cliente = _cliente_destino_correo(cliente_id=body.cliente_id, db=db)
    return _enviar_correo_enlace_cliente(
        enlace=enlace,
        proyecto=proyecto,
        cliente=cliente,
        request=request,
        email_service=EmailService(),
    )


@router.get("/{token}", response_model=PortalClienteOut)
def obtener_portal_cliente(
    token: str,
    request: Request,
    db: Session = Depends(get_db),
) -> PortalClienteOut:
    enlace = _obtener_enlace_publico(token=token, db=db, request=request)
    contenido = _contenido_from_model(enlace)
    proyecto = enlace.proyecto
    plano_ids = {plano.id for plano in proyecto.planos}
    conjuntos = (
        db.query(ConjuntoAP)
        .filter(
            ConjuntoAP.id.in_(contenido.conjunto_ids),
            ConjuntoAP.plano_id.in_(plano_ids),
        )
        .all()
        if contenido.conjunto_ids
        else []
    )
    mapas = (
        db.query(MapaCalor)
        .filter(MapaCalor.id.in_(contenido.mapa_ids), MapaCalor.plano_id.in_(plano_ids))
        .order_by(MapaCalor.created_at.desc(), MapaCalor.id.desc())
        .all()
        if contenido.mapa_ids
        else []
    )
    planos_mapa = {mapa.plano_id for mapa in mapas}
    planos_visibles = planos_mapa | {conjunto.plano_id for conjunto in conjuntos}
    planos = (
        db.query(Plano)
        .filter(Plano.id.in_(planos_visibles))
        .order_by(Plano.created_at.desc(), Plano.id.desc())
        .all()
        if planos_visibles
        else []
    )
    return PortalClienteOut(
        proyecto=ProyectoPortalOut(
            id=proyecto.id,
            nombre=proyecto.nombre,
            cliente=proyecto.cliente.nombre if proyecto.cliente else None,
            descripcion=proyecto.descripcion,
        ),
        planos=[
            PlanoOut.from_plano(
                plano,
                url_firmada=_firmar_plano(plano.ruta_storage, request),
            )
            for plano in planos
        ],
        conjuntos=[_conjunto_out(conjunto) for conjunto in conjuntos],
        heatmaps=[_mapa_out(mapa, request) for mapa in mapas],
    )


@router.post(
    "/{token}/conjuntos/{conjunto_id}/heatmaps",
    response_model=MapaCalorOut,
)
def generar_heatmap_portal(
    token: str,
    conjunto_id: int,
    body: GenerarHeatmapConjuntoIn,
    request: Request,
    db: Session = Depends(get_db),
) -> MapaCalorOut:
    enlace = _obtener_enlace_publico(token=token, db=db)
    contenido = _contenido_from_model(enlace)
    if conjunto_id not in contenido.conjunto_ids:
        raise HTTPException(status_code=404, detail="Conjunto no disponible.")

    proyecto = enlace.proyecto
    plano_ids = {plano.id for plano in proyecto.planos}
    conjunto = (
        db.query(ConjuntoAP)
        .filter(
            ConjuntoAP.id == conjunto_id,
            ConjuntoAP.plano_id.in_(plano_ids),
        )
        .first()
    )
    if conjunto is None:
        raise HTTPException(status_code=404, detail="Conjunto no disponible.")

    bssids_conjunto = [item.bssid.lower() for item in conjunto.items]
    bssids_solicitados = [bssid.strip().lower() for bssid in (body.bssids or [])]
    if body.modo == "CONJUNTO_COMPLETO":
        bssids_generacion = bssids_conjunto
    elif body.modo == "INDIVIDUAL":
        if len(bssids_solicitados) != 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El modo INDIVIDUAL requiere exactamente un AP del conjunto.",
            )
        bssids_generacion = bssids_solicitados
    else:
        if not bssids_solicitados:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El modo SUBCONJUNTO requiere al menos un AP del conjunto.",
            )
        bssids_generacion = bssids_solicitados

    fuera_del_conjunto = [
        bssid for bssid in bssids_generacion if bssid not in bssids_conjunto
    ]
    if fuera_del_conjunto:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Uno o más APs seleccionados no pertenecen al conjunto.",
        )

    items_por_bssid = {item.bssid.lower(): item for item in conjunto.items}
    ap_pos_x = [
        items_por_bssid[bssid].pos_x
        for bssid in bssids_generacion
        if items_por_bssid[bssid].pos_x is not None
    ]
    ap_pos_y = [
        items_por_bssid[bssid].pos_y
        for bssid in bssids_generacion
        if items_por_bssid[bssid].pos_y is not None
    ]
    posiciones_completas = len(ap_pos_x) == len(bssids_generacion) and len(
        ap_pos_y
    ) == len(bssids_generacion)
    tecnico = db.query(Usuario).filter(Usuario.id == proyecto.tecnico_id).first()
    if tecnico is None:
        raise HTTPException(status_code=404, detail="Proyecto no disponible.")

    return _generar_heatmap_core(
        plano_id=conjunto.plano_id,
        request=request,
        bssid=bssids_generacion,
        ap_pos_x=ap_pos_x if posiciones_completas else None,
        ap_pos_y=ap_pos_y if posiciones_completas else None,
        algoritmo=body.algoritmo,
        resolucion=body.resolucion,
        db=db,
        current_user=tecnico,
        conjunto_ap_id=conjunto.id,
        modo_generacion=body.modo,
    )
