"""seed_dev.py — Inserta usuarios, clientes y proyectos de prueba para desarrollo local.

Solo debe ejecutarse en entornos de desarrollo (DEBUG=true).
Idempotente: no duplica registros si ya existen.

Usuarios creados:
  admin@bulldogtech.bo   / Admin2026!    rol: admin
  tecnico@bulldogtech.bo / Tecnico2026!  rol: tecnico

Clientes de prueba:
  Bulldog Tech.
  Cliente Beta S.A.

Proyectos de prueba:
  3 proyectos asignados al técnico demo (Sprint 1 — PB-18, PB-19 seed data)
  1 proyecto real adaptado desde producción: Campo Villamontes / Multinacional S.A.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Guardia: solo corre en modo debug / desarrollo
if os.getenv("DEBUG", "false").lower() != "true":
    print("[seed_dev] No estoy en modo DEBUG — omitiendo seed.")
    sys.exit(0)

import bcrypt

from app.core.config import settings  # noqa: E402
from app.core.database import SessionLocal  # noqa: E402
from app.models.cliente import Cliente  # noqa: E402
from app.models.medicion import (  # noqa: E402
    MedicionWifi,
    PuntoMedicion,
    clasificar_nivel,
)
from app.models.plano import Plano  # noqa: E402
from app.models.proyecto import Proyecto  # noqa: E402
from app.models.usuario import Usuario  # noqa: E402
from app.storage import LocalFilesystemStorage  # noqa: E402

USUARIOS_PRUEBA = [
    {
        "nombre": "Administrador",
        "email": "admin@bulldogtech.bo",
        "password": "Admin2026!",
        "rol": "admin",
    },
    {
        "nombre": "Técnico Demo",
        "email": "tecnico@bulldogtech.bo",
        "password": "Tecnico2026!",
        "rol": "tecnico",
    },
]

CLIENTES_PRUEBA = [
    "Bulldog Tech.",
    "Cliente Beta S.A.",
]

PROYECTOS_PRUEBA = [
    {
        "nombre": "Oficinas Central Bulldog Tech.",
        "cliente": "Bulldog Tech.",
        "estado": "en_progreso",
    },
    {"nombre": "Sucursal Norte", "cliente": "Bulldog Tech.", "estado": "completado"},
    {
        "nombre": "Almacén Logístico",
        "cliente": "Cliente Beta S.A.",
        "estado": "en_progreso",
    },
]

SEED_ASSETS_DIR = Path(__file__).resolve().parent / "seed_assets"
CAMPO_VILLAMONTES_JSON = (
    SEED_ASSETS_DIR
    / "campo_villamontes"
    / "campo_villamontes_seed.json"
)


def _parse_fecha(valor: str | None) -> datetime | None:
    if not valor:
        return None
    return datetime.fromisoformat(valor.replace("Z", "+00:00"))


def _peor_nivel(mediciones: list[dict]) -> str:
    orden = {"verde": 0, "amarillo": 1, "naranja": 2, "rojo": 3, "negro": 4}
    niveles = [
        item.get("nivel") or clasificar_nivel(int(item["rssi"]))
        for item in mediciones
    ]
    return max(niveles, key=lambda nivel: orden[nivel])


def _normalizar_estado_proyecto(estado: str, cantidad_puntos: int) -> str:
    if estado == "nuevo" and cantidad_puntos > 0:
        return "en_progreso"
    return estado


def _seed_campo_villamontes(db, tecnico: Usuario) -> None:
    """Carga datos reales de Campo Villamontes adaptados al modelo vigente."""
    if not CAMPO_VILLAMONTES_JSON.exists():
        print("[seed_dev] Seed Campo Villamontes no encontrado — omitido.")
        return

    data = json.loads(CAMPO_VILLAMONTES_JSON.read_text(encoding="utf-8"))
    cliente_data = data["cliente"]
    proyecto_data = data["proyecto"]
    planos_data = data["planos"]
    cantidad_puntos = sum(len(plano["puntos"]) for plano in planos_data)

    cliente = db.query(Cliente).filter_by(nombre=cliente_data["nombre"]).first()
    if not cliente:
        cliente = Cliente(
            nombre=cliente_data["nombre"],
            email_referencia=cliente_data.get("email_referencia"),
            activo=True,
        )
        db.add(cliente)
        db.flush()
        print(f"[seed_dev] Cliente real creado: {cliente.nombre}")
    else:
        cliente.email_referencia = cliente_data.get("email_referencia")
        cliente.activo = True

    proyecto = (
        db.query(Proyecto)
        .filter_by(nombre=proyecto_data["nombre"], cliente_id=cliente.id)
        .first()
    )
    estado = _normalizar_estado_proyecto(
        proyecto_data.get("estado", "en_progreso"),
        cantidad_puntos,
    )
    if not proyecto:
        proyecto = Proyecto(
            nombre=proyecto_data["nombre"],
            descripcion=(
                proyecto_data.get("descripcion")
                or "Proyecto real de desarrollo con plano y lecturas WiFi de campo."
            ),
            cliente_id=cliente.id,
            estado=estado,
            tecnico_id=tecnico.id,
            cantidad_puntos=cantidad_puntos,
        )
        db.add(proyecto)
        db.flush()
        print(f"[seed_dev] Proyecto real creado: {proyecto.nombre}")
    else:
        proyecto.descripcion = (
            proyecto_data.get("descripcion")
            or "Proyecto real de desarrollo con plano y lecturas WiFi de campo."
        )
        proyecto.cliente_id = cliente.id
        proyecto.estado = estado
        proyecto.tecnico_id = tecnico.id
        proyecto.cantidad_puntos = cantidad_puntos
        print(f"[seed_dev] Proyecto real actualizado: {proyecto.nombre}")

    storage = LocalFilesystemStorage(root=settings.storage_root)

    for plano_data in planos_data:
        archivo_seed = (
            CAMPO_VILLAMONTES_JSON.parent / plano_data["archivo_seed"]
        )
        if not archivo_seed.exists():
            print(
                "[seed_dev] Imagen de Campo Villamontes no encontrada "
                f"({archivo_seed.name}) — plano omitido."
            )
            continue

        ruta_storage = f"seed/campo_villamontes/{archivo_seed.name}"
        storage.save(archivo_seed.read_bytes(), ruta_storage)

        plano = (
            db.query(Plano)
            .filter_by(proyecto_id=proyecto.id, nombre=plano_data["nombre"])
            .first()
        )
        if not plano:
            plano = Plano(proyecto_id=proyecto.id, nombre=plano_data["nombre"])
            db.add(plano)
            print(f"[seed_dev] Plano real creado: {plano.nombre}")
        else:
            for punto in list(plano.puntos_medicion):
                db.delete(punto)
            print(f"[seed_dev] Plano real actualizado: {plano.nombre}")

        plano.descripcion = plano_data.get("descripcion")
        plano.formato = plano_data["formato"]
        plano.ruta_storage = ruta_storage
        plano.ancho_px = plano_data["ancho_px"]
        plano.alto_px = plano_data["alto_px"]
        plano.tamano_bytes = archivo_seed.stat().st_size
        plano.calibracion_x1 = plano_data.get("calibracion_x1")
        plano.calibracion_y1 = plano_data.get("calibracion_y1")
        plano.calibracion_x2 = plano_data.get("calibracion_x2")
        plano.calibracion_y2 = plano_data.get("calibracion_y2")
        plano.distancia_real_m = plano_data.get("distancia_real_m")
        plano.escala_m_por_px = plano_data.get("escala_m_por_px")
        plano.poligono_interes = plano_data.get("poligono_interes")
        db.flush()

        for punto_data in plano_data["puntos"]:
            mediciones = punto_data["mediciones"]
            punto = PuntoMedicion(
                plano_id=plano.id,
                pos_x=punto_data["pos_x"],
                pos_y=punto_data["pos_y"],
                nivel=punto_data.get("nivel") or _peor_nivel(mediciones),
                created_at=_parse_fecha(punto_data.get("created_at")),
            )
            db.add(punto)
            db.flush()
            for medicion_data in mediciones:
                db.add(
                    MedicionWifi(
                        punto_id=punto.id,
                        ssid=medicion_data["ssid"],
                        bssid=medicion_data["bssid"].lower(),
                        rssi=medicion_data["rssi"],
                        canal=medicion_data.get("canal"),
                        frecuencia_mhz=medicion_data.get("frecuencia_mhz"),
                        nivel=(
                            medicion_data.get("nivel")
                            or clasificar_nivel(int(medicion_data["rssi"]))
                        ),
                        numero_lectura=medicion_data.get("numero_lectura", 1),
                        created_at=_parse_fecha(medicion_data.get("created_at")),
                    )
                )

    db.commit()
    print(
        "[seed_dev] Campo Villamontes cargado: "
        f"{len(planos_data)} plano(s), {cantidad_puntos} punto(s)."
    )


def seed() -> None:
    with SessionLocal() as db:
        # Usuarios
        for datos in USUARIOS_PRUEBA:
            existe = db.query(Usuario).filter_by(email=datos["email"]).first()
            if existe:
                print(f"[seed_dev] Ya existe: {datos['email']} — omitido.")
                continue
            usuario = Usuario(
                nombre=datos["nombre"],
                email=datos["email"],
                password_hash=bcrypt.hashpw(
                    datos["password"].encode(), bcrypt.gensalt()
                ).decode(),
                rol=datos["rol"],
                activo=True,
            )
            db.add(usuario)
            print(f"[seed_dev] Creado: {datos['email']} (rol={datos['rol']})")
        db.commit()

        # Clientes (PB-19)
        clientes_map: dict[str, int] = {}
        for nombre in CLIENTES_PRUEBA:
            cliente = db.query(Cliente).filter_by(nombre=nombre).first()
            if not cliente:
                cliente = Cliente(nombre=nombre)
                db.add(cliente)
                db.flush()
                print(f"[seed_dev] Cliente creado: {nombre}")
            else:
                print(f"[seed_dev] Ya existe cliente: {nombre} — omitido.")
            clientes_map[nombre] = cliente.id
        db.commit()

        # Proyectos (asignados al técnico demo)
        tecnico = db.query(Usuario).filter_by(email="tecnico@bulldogtech.bo").first()
        if tecnico:
            proyectos_existentes = (
                db.query(Proyecto).filter_by(tecnico_id=tecnico.id).count()
            )
            if proyectos_existentes == 0:
                for datos in PROYECTOS_PRUEBA:
                    proyecto = Proyecto(
                        nombre=datos["nombre"],
                        cliente_id=clientes_map.get(datos["cliente"]),
                        estado=datos["estado"],
                        tecnico_id=tecnico.id,
                    )
                    db.add(proyecto)
                    print(f"[seed_dev] Proyecto creado: {datos['nombre']}")
                db.commit()

            _seed_campo_villamontes(db, tecnico)


    print("[seed_dev] Seed completado.")


if __name__ == "__main__":
    seed()
