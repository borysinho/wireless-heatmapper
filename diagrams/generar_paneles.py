"""
generar_paneles.py
==================
Genera diagrams/Paneles-WHM.mdj con los 16 diagramas UML 2.5+
del proyecto Wireless HeatMapper, basados en docs/PANELES.

Uso:
    python diagrams/generar_paneles.py

Salida:
    diagrams/Paneles-WHM.mdj  (NO sobreescribe el archivo existente)
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

OUTPUT = Path(__file__).parent / "Paneles-WHM.mdj"

# ── Paleta institucional ────────────────────────────────────────────────────
FILL   = "#EBF5FB"
BORDER = "#2980B9"
NOTE   = "#FFFDE7"
TEXT   = "#000000"

# ─────────────────────────── IDs deterministas ─────────────────────────────
def sid(key: str) -> str:
    """ID estable de 32 hex a partir de clave semántica (MD5)."""
    return hashlib.md5(key.encode("utf-8")).hexdigest()


def ref(k: str) -> dict:
    return {"$ref": sid(k)}


# ─────────────────────────── Edge label views ──────────────────────────────
def _elv(vk: str, pk: str, mk: str, vis: bool = False,
         ep: int = 1, a: float = 0.0, d: float = 15.0) -> dict:
    return {
        "_type": "EdgeLabelView",
        "_id": sid(vk), "_parent": ref(pk), "model": ref(mk),
        "visible": vis, "edgePosition": ep, "alpha": a,
        "distance": d, "hostEdge": ref(pk),
    }


def _assoc_labs(vk: str, mk: str) -> tuple[list, dict]:
    ovs = [
        _elv(f"{vk}_nl",  vk, mk, vis=True),
        _elv(f"{vk}_sl",  vk, mk),
        _elv(f"{vk}_pl",  vk, mk, ep=2),
        _elv(f"{vk}_hml", vk, mk, a=0.5236,  d=25.0, ep=2),
        _elv(f"{vk}_tml", vk, mk, a=-0.5236, d=25.0),
        _elv(f"{vk}_hql", vk, mk, a=-0.5236, d=15.0, ep=2),
        _elv(f"{vk}_tql", vk, mk, a=0.5236,  d=15.0),
    ]
    refs = {
        "nameLabel":              ref(f"{vk}_nl"),
        "stereotypeLabel":        ref(f"{vk}_sl"),
        "propertyLabel":          ref(f"{vk}_pl"),
        "headMultiplicityLabel":  ref(f"{vk}_hml"),
        "tailMultiplicityLabel":  ref(f"{vk}_tml"),
        "headQualifierCompartment": ref(f"{vk}_hql"),
        "tailQualifierCompartment": ref(f"{vk}_tql"),
    }
    return ovs, refs


def _simple_labs(vk: str, mk: str) -> tuple[list, dict]:
    ovs = [
        _elv(f"{vk}_nl", vk, mk, vis=True),
        _elv(f"{vk}_sl", vk, mk),
        _elv(f"{vk}_pl", vk, mk, ep=2),
    ]
    refs = {
        "nameLabel":       ref(f"{vk}_nl"),
        "stereotypeLabel": ref(f"{vk}_sl"),
        "propertyLabel":   ref(f"{vk}_pl"),
    }
    return ovs, refs


# ─────────────────────────── Model builders ────────────────────────────────
def M(tp: str, k: str, pk: str, name: str = "", **kw) -> dict:
    e: dict = {"_type": tp, "_id": sid(k), "_parent": ref(pk), "name": name}
    e.update(kw)
    return e


def M_class(k: str, pk: str, name: str,
            attrs: list[tuple] | None = None,
            abstract: bool = False) -> dict:
    e = M("UMLClass", k, pk, name, visibility="public", isAbstract=abstract)
    if attrs:
        e["ownedElements"] = [
            {"_type": "UMLAttribute", "_id": sid(f"{k}_a{i}"),
             "_parent": ref(k), "name": a[0],
             "type": a[1] if len(a) > 1 else "", "visibility": "public"}
            for i, a in enumerate(attrs)
        ]
    return e


def M_assoc(k: str, pk: str, e1k: str, e2k: str,
            name: str = "", m1: str = "", m2: str = "") -> dict:
    e1 = {"_type": "UMLAssociationEnd", "_id": sid(f"{k}_e1"),
          "_parent": ref(k), "reference": ref(e1k),
          "navigable": True, "multiplicity": m1, "aggregation": "none"}
    e2 = {"_type": "UMLAssociationEnd", "_id": sid(f"{k}_e2"),
          "_parent": ref(k), "reference": ref(e2k),
          "navigable": True, "multiplicity": m2, "aggregation": "none"}
    return {"_type": "UMLAssociation", "_id": sid(k), "_parent": ref(pk),
            "name": name, "end1": e1, "end2": e2}


# ─────────────────────────── View builders ─────────────────────────────────
def _Vb(tp: str, vk: str, dk: str, mk: str, x: int, y: int, w: int, h: int,
        fill: str = FILL, border: str = BORDER,
        inner: list | None = None) -> dict:
    v: dict = {
        "_type": tp, "_id": sid(vk), "_parent": ref(dk), "model": ref(mk),
        "x": x, "y": y, "width": w, "height": h,
        "fillColor": fill, "lineColor": border, "fontColor": TEXT,
        "visible": True, "enabled": True,
    }
    if inner is not None:
        v["ownedViews"] = inner
    return v


def V_nc(vk: str, pvk: str, mk: str) -> dict:
    return {"_type": "UMLNameCompartmentView",
            "_id": sid(vk), "_parent": ref(pvk), "model": ref(mk), "visible": True}


def V_ac(vk: str, pvk: str, mk: str) -> dict:
    return {"_type": "UMLAttributeCompartmentView",
            "_id": sid(vk), "_parent": ref(pvk), "model": ref(mk), "visible": True}


def V_oc(vk: str, pvk: str, mk: str) -> dict:
    return {"_type": "UMLOperationCompartmentView",
            "_id": sid(vk), "_parent": ref(pvk), "model": ref(mk), "visible": True}


def V_lp(vk: str, pvk: str, mk: str) -> dict:
    return {"_type": "UMLLinePartView",
            "_id": sid(vk), "_parent": ref(pvk), "model": ref(mk), "visible": True}


def actor_v(vk: str, dk: str, mk: str, x: int, y: int) -> dict:
    return _Vb("UMLActorView", vk, dk, mk, x, y, 40, 65, inner=[])


def uc_v(vk: str, dk: str, mk: str, x: int, y: int,
         w: int = 150, h: int = 40) -> dict:
    return _Vb("UMLUseCaseView", vk, dk, mk, x, y, w, h)


def class_v(vk: str, dk: str, mk: str, x: int, y: int,
            w: int = 165, h: int = 110) -> dict:
    return _Vb("UMLClassView", vk, dk, mk, x, y, w, h, inner=[
        V_nc(f"{vk}_nc", vk, mk), V_ac(f"{vk}_ac", vk, mk), V_oc(f"{vk}_oc", vk, mk),
    ])


def pkg_v(vk: str, dk: str, mk: str, x: int, y: int,
          w: int = 210, h: int = 120) -> dict:
    return _Vb("UMLPackageView", vk, dk, mk, x, y, w, h,
               inner=[V_nc(f"{vk}_nc", vk, mk)])


def node_v(vk: str, dk: str, mk: str, x: int, y: int,
           w: int = 190, h: int = 80) -> dict:
    return _Vb("UMLNodeView", vk, dk, mk, x, y, w, h,
               inner=[V_nc(f"{vk}_nc", vk, mk)])


def artifact_v(vk: str, dk: str, mk: str, x: int, y: int,
               w: int = 150, h: int = 38) -> dict:
    return _Vb("UMLArtifactView", vk, dk, mk, x, y, w, h,
               inner=[V_nc(f"{vk}_nc", vk, mk)])


def lifeline_v(vk: str, dk: str, mk: str, x: int,
               y: int = 32, w: int = 110, h: int = 40) -> dict:
    return _Vb("UMLSeqLifelineView", vk, dk, mk, x, y, w, h, inner=[
        V_nc(f"{vk}_nc", vk, mk), V_lp(f"{vk}_lp", vk, mk),
    ])


def state_v(vk: str, dk: str, mk: str, x: int, y: int,
            w: int = 130, h: int = 40) -> dict:
    return _Vb("UMLStateView", vk, dk, mk, x, y, w, h,
               inner=[V_nc(f"{vk}_nc", vk, mk)])


def pseudo_v(vk: str, dk: str, mk: str, x: int, y: int) -> dict:
    return _Vb("UMLPseudostateView", vk, dk, mk, x, y, 20, 20,
               fill=BORDER, border=BORDER, inner=[])


def final_v(vk: str, dk: str, mk: str, x: int, y: int) -> dict:
    return _Vb("UMLFinalStateView", vk, dk, mk, x, y, 25, 25,
               fill=BORDER, border=BORDER, inner=[])


def edge_v(tp: str, vk: str, dk: str, mk: str,
           tail_vk: str, head_vk: str) -> dict:
    is_assoc = tp == "UMLAssociationView"
    ovs, refs = _assoc_labs(vk, mk) if is_assoc else _simple_labs(vk, mk)
    v: dict = {
        "_type": tp, "_id": sid(vk), "_parent": ref(dk), "model": ref(mk),
        "tail": ref(tail_vk), "head": ref(head_vk),
        "lineColor": BORDER, "visible": True, "enabled": True,
        "ownedViews": ovs,
    }
    v.update(refs)
    return v


def seq_msg_v(vk: str, dk: str, mk: str,
              tail_vk: str, head_vk: str,
              x1: int, y1: int, x2: int, y2: int) -> dict:
    nl = _elv(f"{vk}_nl", vk, mk, vis=True)
    return {
        "_type": "UMLSeqMessageView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "tail": ref(tail_vk), "head": ref(head_vk),
        "points": f"{x1}:{y1};{x2}:{y2}",
        "lineColor": BORDER, "visible": True, "enabled": True,
        "ownedViews": [nl], "nameLabel": ref(f"{vk}_nl"),
    }


def diag(tp: str, dk: str, pk: str, name: str, views: list) -> dict:
    return {
        "_type": tp, "_id": sid(dk), "_parent": ref(pk),
        "name": name, "visible": True, "defaultDiagram": False,
        "ownedViews": views,
    }


# ═══════════════════════════════════════════════════════════════════════════
# SPRINT 0
# ═══════════════════════════════════════════════════════════════════════════

def build_sprint0(proj_k: str) -> list[dict]:
    M0 = "m_s0"

    # ── S0.1 Contexto — Diagrama de Casos de Uso ─────────────────────────
    D = "diag_s0_ctx"
    ctx_elems: list[dict] = [
        M("UMLActor",   "a_s0_adm", M0, "Administrador"),
        M("UMLActor",   "a_s0_tec", M0, "Técnico (App Móvil)"),
        M("UMLActor",   "a_s0_cli", M0, "Cliente"),
        M("UMLActor",   "a_s0_ia",  M0, "Sistema IA (Backend)"),
        M("UMLUseCase", "uc_s0_01", M0, "UC01 Gestionar usuarios"),
        M("UMLUseCase", "uc_s0_02", M0, "UC02 Autenticarse"),
        M("UMLUseCase", "uc_s0_09", M0, "UC09 Gestionar clientes"),
        M("UMLUseCase", "uc_s0_13", M0, "UC13 Gestionar proyectos"),
        M("UMLUseCase", "uc_s0_18", M0, "UC18 Ver listado de proyectos"),
        M("UMLUseCase", "uc_s0_19", M0, "UC19 Autenticarse en app móvil"),
        M("UMLUseCase", "uc_s0_03", M0, "UC03 Seleccionar proyecto"),
        M("UMLUseCase", "uc_s0_04", M0, "UC04 Realizar levantamiento Wi-Fi"),
        M("UMLUseCase", "uc_s0_05", M0, "UC05 Generar mapa de calor"),
        M("UMLUseCase", "uc_s0_06", M0, "UC06 Analizar cobertura con IA"),
        M("UMLUseCase", "uc_s0_07", M0, "UC07 Ver heatmap en panel web"),
        M("UMLUseCase", "uc_s0_08", M0, "UC08 Exportar reportes"),
        M("UMLUseCase", "uc_s0_10", M0, "UC10 Ver proyectos propios"),
        M_assoc("as_s0_a1", M0, "a_s0_adm", "uc_s0_01"),
        M_assoc("as_s0_a2", M0, "a_s0_adm", "uc_s0_02"),
        M_assoc("as_s0_a9", M0, "a_s0_adm", "uc_s0_09"),
        M_assoc("as_s0_a13", M0, "a_s0_adm", "uc_s0_13"),
        M_assoc("as_s0_a18", M0, "a_s0_adm", "uc_s0_18"),
        M_assoc("as_s0_a7",  M0, "a_s0_adm", "uc_s0_07"),
        M_assoc("as_s0_a8",  M0, "a_s0_adm", "uc_s0_08"),
        M_assoc("as_s0_t19", M0, "a_s0_tec", "uc_s0_19"),
        M_assoc("as_s0_t3",  M0, "a_s0_tec", "uc_s0_03"),
        M_assoc("as_s0_t4",  M0, "a_s0_tec", "uc_s0_04"),
        M_assoc("as_s0_c10", M0, "a_s0_cli", "uc_s0_10"),
        M_assoc("as_s0_c2",  M0, "a_s0_cli", "uc_s0_02"),
        M("UMLInclude", "inc_s0_0405", M0, "",
          client=ref("uc_s0_04"), supplier=ref("uc_s0_05")),
        M("UMLInclude", "inc_s0_0506", M0, "",
          client=ref("uc_s0_05"), supplier=ref("uc_s0_06")),
        M_assoc("as_s0_ia6", M0, "uc_s0_06", "a_s0_ia"),
    ]
    ctx_views: list[dict] = [
        actor_v("va_s0_adm", D, "a_s0_adm", 40, 60),
        actor_v("va_s0_tec", D, "a_s0_tec", 40, 290),
        actor_v("va_s0_cli", D, "a_s0_cli", 40, 490),
        actor_v("va_s0_ia",  D, "a_s0_ia",  710, 380),
        uc_v("vuc_s0_01", D, "uc_s0_01", 200,  30, 165, 40),
        uc_v("vuc_s0_02", D, "uc_s0_02", 200,  90, 155, 40),
        uc_v("vuc_s0_09", D, "uc_s0_09", 200, 150, 165, 40),
        uc_v("vuc_s0_13", D, "uc_s0_13", 440,  30, 175, 40),
        uc_v("vuc_s0_18", D, "uc_s0_18", 440,  90, 205, 40),
        uc_v("vuc_s0_07", D, "uc_s0_07", 440, 150, 210, 40),
        uc_v("vuc_s0_08", D, "uc_s0_08", 440, 210, 175, 40),
        uc_v("vuc_s0_19", D, "uc_s0_19", 200, 270, 210, 40),
        uc_v("vuc_s0_03", D, "uc_s0_03", 200, 330, 185, 40),
        uc_v("vuc_s0_04", D, "uc_s0_04", 440, 270, 225, 40),
        uc_v("vuc_s0_05", D, "uc_s0_05", 440, 330, 200, 40),
        uc_v("vuc_s0_06", D, "uc_s0_06", 440, 390, 210, 40),
        uc_v("vuc_s0_10", D, "uc_s0_10", 200, 490, 200, 40),
        edge_v("UMLAssociationView", "ve_s0_a1",  D, "as_s0_a1",  "va_s0_adm", "vuc_s0_01"),
        edge_v("UMLAssociationView", "ve_s0_a2",  D, "as_s0_a2",  "va_s0_adm", "vuc_s0_02"),
        edge_v("UMLAssociationView", "ve_s0_a9",  D, "as_s0_a9",  "va_s0_adm", "vuc_s0_09"),
        edge_v("UMLAssociationView", "ve_s0_a13", D, "as_s0_a13", "va_s0_adm", "vuc_s0_13"),
        edge_v("UMLAssociationView", "ve_s0_a18", D, "as_s0_a18", "va_s0_adm", "vuc_s0_18"),
        edge_v("UMLAssociationView", "ve_s0_a7",  D, "as_s0_a7",  "va_s0_adm", "vuc_s0_07"),
        edge_v("UMLAssociationView", "ve_s0_a8",  D, "as_s0_a8",  "va_s0_adm", "vuc_s0_08"),
        edge_v("UMLAssociationView", "ve_s0_t19", D, "as_s0_t19", "va_s0_tec", "vuc_s0_19"),
        edge_v("UMLAssociationView", "ve_s0_t3",  D, "as_s0_t3",  "va_s0_tec", "vuc_s0_03"),
        edge_v("UMLAssociationView", "ve_s0_t4",  D, "as_s0_t4",  "va_s0_tec", "vuc_s0_04"),
        edge_v("UMLAssociationView", "ve_s0_c10", D, "as_s0_c10", "va_s0_cli", "vuc_s0_10"),
        edge_v("UMLAssociationView", "ve_s0_c2",  D, "as_s0_c2",  "va_s0_cli", "vuc_s0_02"),
        edge_v("UMLIncludeView",     "ve_s0_i45", D, "inc_s0_0405", "vuc_s0_04", "vuc_s0_05"),
        edge_v("UMLIncludeView",     "ve_s0_i56", D, "inc_s0_0506", "vuc_s0_05", "vuc_s0_06"),
        edge_v("UMLAssociationView", "ve_s0_ia6", D, "as_s0_ia6", "vuc_s0_06", "va_s0_ia"),
    ]
    ctx_diag = diag("UMLUseCaseDiagram", D, M0, "Modelo_Contexto_Sprint0", ctx_views)

    # ── S0.2 Arquitectura de Paquetes ────────────────────────────────────
    D = "diag_s0_pkg"
    pkg_elems: list[dict] = [
        M("UMLPackage", "pkg_s0_mob", M0, "App Móvil (Flutter/Dart)"),
        M("UMLPackage", "pkg_s0_bk",  M0, "Backend (FastAPI/Python)"),
        M("UMLPackage", "pkg_s0_web", M0, "Web Admin (React/TypeScript)"),
        M("UMLPackage", "pkg_s0_db",  M0, "Base de Datos (PostgreSQL 15)"),
        M("UMLDependency", "dep_s0_mb", M0, "REST/HTTPS",
          client=ref("pkg_s0_mob"), supplier=ref("pkg_s0_bk")),
        M("UMLDependency", "dep_s0_wb", M0, "REST/HTTPS",
          client=ref("pkg_s0_web"), supplier=ref("pkg_s0_bk")),
        M("UMLDependency", "dep_s0_bd", M0, "SQLAlchemy/ORM",
          client=ref("pkg_s0_bk"), supplier=ref("pkg_s0_db")),
    ]
    pkg_views: list[dict] = [
        pkg_v("vp_s0_mob", D, "pkg_s0_mob",  40,  40, 220, 130),
        pkg_v("vp_s0_bk",  D, "pkg_s0_bk",  320,  40, 220, 130),
        pkg_v("vp_s0_web", D, "pkg_s0_web",  600,  40, 230, 130),
        pkg_v("vp_s0_db",  D, "pkg_s0_db",  320, 230, 220,  90),
        edge_v("UMLDependencyView", "ve_s0_mb", D, "dep_s0_mb", "vp_s0_mob", "vp_s0_bk"),
        edge_v("UMLDependencyView", "ve_s0_wb", D, "dep_s0_wb", "vp_s0_web", "vp_s0_bk"),
        edge_v("UMLDependencyView", "ve_s0_bd", D, "dep_s0_bd", "vp_s0_bk",  "vp_s0_db"),
    ]
    pkg_diag = diag("UMLPackageDiagram", D, M0, "Arquitectura_Paquetes_Sprint0", pkg_views)

    # ── S0.3 Despliegue ──────────────────────────────────────────────────
    D = "diag_s0_dep"
    dep_elems: list[dict] = [
        M("UMLNode",     "nd_s0_and",  M0, "Dispositivo Android (Técnico)"),
        M("UMLNode",     "nd_s0_srv",  M0, "Servidor de Producción (VPS/Docker)"),
        M("UMLNode",     "nd_s0_ngx",  M0, "Nginx (Reverse Proxy)"),
        M("UMLNode",     "nd_s0_api",  M0, "FastAPI (Backend REST + IA)"),
        M("UMLNode",     "nd_s0_app",  M0, "React App (Panel Web)"),
        M("UMLNode",     "nd_s0_pdb",  M0, "PostgreSQL (Base de Datos)"),
        M("UMLArtifact", "art_s0_apk", M0, "App Flutter (APK)"),
        M("UMLDependency", "dep_s0_an",  M0, "HTTPS / REST",
          client=ref("nd_s0_and"), supplier=ref("nd_s0_ngx")),
        M("UMLDependency", "dep_s0_na",  M0, "/api/*",
          client=ref("nd_s0_ngx"), supplier=ref("nd_s0_api")),
        M("UMLDependency", "dep_s0_nw",  M0, "/*",
          client=ref("nd_s0_ngx"), supplier=ref("nd_s0_app")),
        M("UMLDependency", "dep_s0_ad",  M0, "TCP 5432",
          client=ref("nd_s0_api"), supplier=ref("nd_s0_pdb")),
    ]
    dep_views: list[dict] = [
        node_v("vn_s0_and",  D, "nd_s0_and",  40,  60, 190, 80),
        artifact_v("vart_s0_apk", D, "art_s0_apk", 55, 100, 160, 38),
        node_v("vn_s0_srv",  D, "nd_s0_srv",  290,  20, 500, 330),
        node_v("vn_s0_ngx",  D, "nd_s0_ngx",  310,  60, 200, 70),
        node_v("vn_s0_api",  D, "nd_s0_api",  310, 160, 200, 70),
        node_v("vn_s0_app",  D, "nd_s0_app",  540,  60, 220, 70),
        node_v("vn_s0_pdb",  D, "nd_s0_pdb",  540, 160, 220, 70),
        edge_v("UMLDependencyView", "ve_s0_an", D, "dep_s0_an", "vn_s0_and", "vn_s0_ngx"),
        edge_v("UMLDependencyView", "ve_s0_na", D, "dep_s0_na", "vn_s0_ngx", "vn_s0_api"),
        edge_v("UMLDependencyView", "ve_s0_nw", D, "dep_s0_nw", "vn_s0_ngx", "vn_s0_app"),
        edge_v("UMLDependencyView", "ve_s0_ad", D, "dep_s0_ad", "vn_s0_api", "vn_s0_pdb"),
    ]
    dep_diag = diag("UMLDeploymentDiagram", D, M0, "Despliegue_Sprint0", dep_views)

    # ── S0.4 Modelo Conceptual de Datos ─────────────────────────────────
    D = "diag_s0_cls"
    cls_elems: list[dict] = [
        M_class("cls_s0_usr",  M0, "Usuario",
                [("nombre",""), ("apellido",""), ("correo",""), ("contrasena",""), ("rol",""), ("activo","")]),
        M_class("cls_s0_org",  M0, "Organizacion",
                [("nombre",""), ("direccion",""), ("contacto",""), ("activo","")]),
        M_class("cls_s0_pry",  M0, "Proyecto",
                [("nombre",""), ("descripcion",""), ("estado",""), ("fechaInicio",""), ("fechaFin","")]),
        M_class("cls_s0_ins",  M0, "Instalacion",
                [("nombre",""), ("descripcion","")]),
        M_class("cls_s0_pla",  M0, "PlanoDePlanta",
                [("archivo",""), ("escala",""), ("anchoMetros",""), ("altoMetros","")]),
        M_class("cls_s0_med",  M0, "Medicion",
                [("rssi_dBm",""), ("ssid",""), ("bssid",""), ("frecuencia_GHz",""), ("canal",""),
                 ("coordenadaX",""), ("coordenadaY",""), ("fechaHora","")]),
        M_class("cls_s0_mpa",  M0, "MapaDeCalor",
                [("imagenGenerada",""), ("algoritmo",""), ("fechaGeneracion","")]),
        M_class("cls_s0_rpt",  M0, "ReporteIA",
                [("recomendaciones",""), ("puntajeCobertura",""), ("fechaEmision","")]),
        M_assoc("ac_s0_up", M0, "cls_s0_usr", "cls_s0_pry",  "gestiona", "1",    "0..*"),
        M_assoc("ac_s0_op", M0, "cls_s0_org", "cls_s0_pry",  "solicita", "1",    "1..*"),
        M_assoc("ac_s0_pi", M0, "cls_s0_pry", "cls_s0_ins",  "abarca",   "1",    "1..*"),
        M_assoc("ac_s0_ip", M0, "cls_s0_ins", "cls_s0_pla",  "tiene",    "1",    "1"),
        M_assoc("ac_s0_pm", M0, "cls_s0_pry", "cls_s0_med",  "contiene", "1",    "0..*"),
        M_assoc("ac_s0_mm", M0, "cls_s0_med", "cls_s0_mpa",  "origina",  "0..*", "1"),
        M_assoc("ac_s0_mr", M0, "cls_s0_mpa", "cls_s0_rpt",  "genera",   "1",    "0..1"),
    ]
    cls_views: list[dict] = [
        class_v("vc_s0_usr", D, "cls_s0_usr",  40,  40, 165, 130),
        class_v("vc_s0_org", D, "cls_s0_org",  240,  40, 165, 110),
        class_v("vc_s0_pry", D, "cls_s0_pry",  440,  40, 165, 110),
        class_v("vc_s0_ins", D, "cls_s0_ins",  640,  40, 165,  85),
        class_v("vc_s0_pla", D, "cls_s0_pla",  640, 200, 165, 110),
        class_v("vc_s0_med", D, "cls_s0_med",  440, 200, 165, 165),
        class_v("vc_s0_mpa", D, "cls_s0_mpa",  240, 200, 165, 100),
        class_v("vc_s0_rpt", D, "cls_s0_rpt",  40,  200, 165, 100),
        edge_v("UMLAssociationView", "ve_s0_up", D, "ac_s0_up", "vc_s0_usr", "vc_s0_pry"),
        edge_v("UMLAssociationView", "ve_s0_op", D, "ac_s0_op", "vc_s0_org", "vc_s0_pry"),
        edge_v("UMLAssociationView", "ve_s0_pi", D, "ac_s0_pi", "vc_s0_pry", "vc_s0_ins"),
        edge_v("UMLAssociationView", "ve_s0_ip", D, "ac_s0_ip", "vc_s0_ins", "vc_s0_pla"),
        edge_v("UMLAssociationView", "ve_s0_pm", D, "ac_s0_pm", "vc_s0_pry", "vc_s0_med"),
        edge_v("UMLAssociationView", "ve_s0_mm", D, "ac_s0_mm", "vc_s0_med", "vc_s0_mpa"),
        edge_v("UMLAssociationView", "ve_s0_mr", D, "ac_s0_mr", "vc_s0_mpa", "vc_s0_rpt"),
    ]
    cls_diag = diag("UMLClassDiagram", D, M0, "Modelo_Datos_Conceptual_Sprint0", cls_views)

    all_elems = (ctx_elems + pkg_elems + dep_elems + cls_elems +
                 [ctx_diag, pkg_diag, dep_diag, cls_diag])
    return [{"_type": "UMLModel", "_id": sid(M0), "_parent": ref(proj_k),
             "name": "Sprint 0 — Modelos Iniciales", "visibility": "public",
             "ownedElements": all_elems}]


# ═══════════════════════════════════════════════════════════════════════════
# SPRINT 1
# ═══════════════════════════════════════════════════════════════════════════

def build_sprint1(proj_k: str) -> list[dict]:
    M1 = "m_s1"

    # ── S1.1 Contexto ────────────────────────────────────────────────────
    D = "diag_s1_ctx"
    ctx_elems: list[dict] = [
        M("UMLActor",   "a_s1_adm", M1, "Administrador"),
        M("UMLActor",   "a_s1_tec", M1, "Técnico (App Móvil)"),
        M("UMLUseCase", "uc_s1_10", M1, "PB-10 Autenticarse en panel web"),
        M("UMLUseCase", "uc_s1_01", M1, "PB-01 Gestionar usuarios"),
        M("UMLUseCase", "uc_s1_09", M1, "PB-09 Gestionar clientes"),
        M("UMLUseCase", "uc_s1_13", M1, "PB-13 Gestionar proyectos"),
        M("UMLUseCase", "uc_s1_18", M1, "PB-18 Ver proyectos por cliente"),
        M("UMLUseCase", "uc_s1_19", M1, "PB-19 Autenticarse en app móvil"),
        M_assoc("as_s1_a10", M1, "a_s1_adm", "uc_s1_10"),
        M_assoc("as_s1_a01", M1, "a_s1_adm", "uc_s1_01"),
        M_assoc("as_s1_a09", M1, "a_s1_adm", "uc_s1_09"),
        M_assoc("as_s1_a13", M1, "a_s1_adm", "uc_s1_13"),
        M_assoc("as_s1_a18", M1, "a_s1_adm", "uc_s1_18"),
        M_assoc("as_s1_t19", M1, "a_s1_tec", "uc_s1_19"),
    ]
    ctx_views: list[dict] = [
        actor_v("va_s1_adm", D, "a_s1_adm", 40, 160),
        actor_v("va_s1_tec", D, "a_s1_tec", 40, 370),
        uc_v("vuc_s1_10", D, "uc_s1_10", 200,  40, 210, 40),
        uc_v("vuc_s1_01", D, "uc_s1_01", 200, 100, 185, 40),
        uc_v("vuc_s1_09", D, "uc_s1_09", 200, 160, 185, 40),
        uc_v("vuc_s1_13", D, "uc_s1_13", 200, 220, 200, 40),
        uc_v("vuc_s1_18", D, "uc_s1_18", 200, 280, 205, 40),
        uc_v("vuc_s1_19", D, "uc_s1_19", 200, 360, 215, 40),
        edge_v("UMLAssociationView", "ve_s1_a10", D, "as_s1_a10", "va_s1_adm", "vuc_s1_10"),
        edge_v("UMLAssociationView", "ve_s1_a01", D, "as_s1_a01", "va_s1_adm", "vuc_s1_01"),
        edge_v("UMLAssociationView", "ve_s1_a09", D, "as_s1_a09", "va_s1_adm", "vuc_s1_09"),
        edge_v("UMLAssociationView", "ve_s1_a13", D, "as_s1_a13", "va_s1_adm", "vuc_s1_13"),
        edge_v("UMLAssociationView", "ve_s1_a18", D, "as_s1_a18", "va_s1_adm", "vuc_s1_18"),
        edge_v("UMLAssociationView", "ve_s1_t19", D, "as_s1_t19", "va_s1_tec", "vuc_s1_19"),
    ]
    ctx_diag = diag("UMLUseCaseDiagram", D, M1, "Contexto_Sprint1", ctx_views)

    # ── S1.2 Paquetes ────────────────────────────────────────────────────
    D = "diag_s1_pkg"
    pkg_elems: list[dict] = [
        M("UMLPackage", "pkg_s1_mob", M1, "App Móvil (Flutter)"),
        M("UMLPackage", "pkg_s1_bk",  M1, "Backend (FastAPI)"),
        M("UMLPackage", "pkg_s1_web", M1, "Web Admin (React)"),
        M("UMLPackage", "pkg_s1_db",  M1, "Base de Datos (PostgreSQL)"),
        M("UMLDependency", "dep_s1_mb", M1, "JWT / REST",
          client=ref("pkg_s1_mob"), supplier=ref("pkg_s1_bk")),
        M("UMLDependency", "dep_s1_wb", M1, "JWT / REST",
          client=ref("pkg_s1_web"), supplier=ref("pkg_s1_bk")),
        M("UMLDependency", "dep_s1_bd", M1, "SQLAlchemy",
          client=ref("pkg_s1_bk"), supplier=ref("pkg_s1_db")),
    ]
    pkg_views: list[dict] = [
        pkg_v("vp_s1_mob", D, "pkg_s1_mob",  40,  40, 220, 130),
        pkg_v("vp_s1_bk",  D, "pkg_s1_bk",  320,  40, 220, 130),
        pkg_v("vp_s1_web", D, "pkg_s1_web",  600,  40, 230, 130),
        pkg_v("vp_s1_db",  D, "pkg_s1_db",  320, 230, 220,  90),
        edge_v("UMLDependencyView", "ve_s1_mb", D, "dep_s1_mb", "vp_s1_mob", "vp_s1_bk"),
        edge_v("UMLDependencyView", "ve_s1_wb", D, "dep_s1_wb", "vp_s1_web", "vp_s1_bk"),
        edge_v("UMLDependencyView", "ve_s1_bd", D, "dep_s1_bd", "vp_s1_bk",  "vp_s1_db"),
    ]
    pkg_diag = diag("UMLPackageDiagram", D, M1, "Paquetes_Sprint1", pkg_views)

    # ── S1.3 Despliegue ──────────────────────────────────────────────────
    D = "diag_s1_dep"
    dep_elems: list[dict] = [
        M("UMLNode", "nd_s1_and",  M1, "Dispositivo Android"),
        M("UMLNode", "nd_s1_brw",  M1, "PC / Navegador Web"),
        M("UMLNode", "nd_s1_srv",  M1, "Servidor (Docker Compose)"),
        M("UMLNode", "nd_s1_ngx",  M1, "nginx:alpine"),
        M("UMLNode", "nd_s1_api",  M1, "backend:python"),
        M("UMLNode", "nd_s1_pdb",  M1, "db:postgres15"),
        M("UMLArtifact", "art_s1_apk",   M1, "App Flutter"),
        M("UMLArtifact", "art_s1_react", M1, "Panel Admin React"),
        M("UMLDependency", "dep_s1_an",  M1, "HTTPS :443 /api",
          client=ref("nd_s1_and"), supplier=ref("nd_s1_ngx")),
        M("UMLDependency", "dep_s1_bn",  M1, "HTTPS :443",
          client=ref("nd_s1_brw"), supplier=ref("nd_s1_ngx")),
        M("UMLDependency", "dep_s1_na",  M1, ":8000 /api/v1",
          client=ref("nd_s1_ngx"), supplier=ref("nd_s1_api")),
        M("UMLDependency", "dep_s1_ad",  M1, ":5432",
          client=ref("nd_s1_api"), supplier=ref("nd_s1_pdb")),
    ]
    dep_views: list[dict] = [
        node_v("vn_s1_and",  D, "nd_s1_and",  40,  60, 180, 80),
        artifact_v("vart_s1_apk", D, "art_s1_apk", 50, 100, 160, 38),
        node_v("vn_s1_brw",  D, "nd_s1_brw",  40, 200, 180, 80),
        artifact_v("vart_s1_rct", D, "art_s1_react", 50, 240, 160, 38),
        node_v("vn_s1_srv",  D, "nd_s1_srv",  280,  20, 500, 330),
        node_v("vn_s1_ngx",  D, "nd_s1_ngx",  300,  60, 200, 70),
        node_v("vn_s1_api",  D, "nd_s1_api",  300, 160, 200, 70),
        node_v("vn_s1_pdb",  D, "nd_s1_pdb",  300, 260, 200, 70),
        edge_v("UMLDependencyView", "ve_s1_an", D, "dep_s1_an", "vn_s1_and", "vn_s1_ngx"),
        edge_v("UMLDependencyView", "ve_s1_bn", D, "dep_s1_bn", "vn_s1_brw", "vn_s1_ngx"),
        edge_v("UMLDependencyView", "ve_s1_na", D, "dep_s1_na", "vn_s1_ngx", "vn_s1_api"),
        edge_v("UMLDependencyView", "ve_s1_ad", D, "dep_s1_ad", "vn_s1_api", "vn_s1_pdb"),
    ]
    dep_diag = diag("UMLDeploymentDiagram", D, M1, "Despliegue_Sprint1", dep_views)

    # ── S1.4 Modelo Conceptual ───────────────────────────────────────────
    D = "diag_s1_cls"
    cls_elems: list[dict] = [
        M_class("cls_s1_usr", M1, "Usuario",
                [("nombre", "string"), ("apellido", "string"), ("correo", "string"),
                 ("contrasena_hash", "string"), ("rol", "enum"), ("activo", "bool"),
                 ("fecha_creacion", "datetime")]),
        M_class("cls_s1_org", M1, "Organizacion",
                [("nombre", "string"), ("direccion", "string"), ("contacto", "string"),
                 ("activo", "bool"), ("fecha_creacion", "datetime")]),
        M_class("cls_s1_pry", M1, "Proyecto",
                [("nombre", "string"), ("descripcion", "string"), ("estado", "enum"),
                 ("fecha_inicio", "date"), ("fecha_fin", "date"), ("fecha_creacion", "datetime")]),
        M_assoc("ac_s1_up", M1, "cls_s1_usr", "cls_s1_pry", "gestiona", "1",    "0..*"),
        M_assoc("ac_s1_op", M1, "cls_s1_org", "cls_s1_pry", "tiene",    "1",    "0..*"),
    ]
    cls_views: list[dict] = [
        class_v("vc_s1_usr", D, "cls_s1_usr",  40,  40, 185, 165),
        class_v("vc_s1_org", D, "cls_s1_org",  290,  40, 185, 130),
        class_v("vc_s1_pry", D, "cls_s1_pry",  540,  40, 185, 145),
        edge_v("UMLAssociationView", "ve_s1_up", D, "ac_s1_up", "vc_s1_usr", "vc_s1_pry"),
        edge_v("UMLAssociationView", "ve_s1_op", D, "ac_s1_op", "vc_s1_org", "vc_s1_pry"),
    ]
    cls_diag = diag("UMLClassDiagram", D, M1, "Datos_Conceptual_Sprint1", cls_views)

    all_m1 = (ctx_elems + pkg_elems + dep_elems + cls_elems +
              [ctx_diag, pkg_diag, dep_diag, cls_diag])
    model_s1 = {"_type": "UMLModel", "_id": sid(M1), "_parent": ref(proj_k),
                "name": "Sprint 1 — Fundación CRUD", "visibility": "public",
                "ownedElements": all_m1}

    # ── S1.5 Secuencia Autenticación ─────────────────────────────────────
    COL1 = "col_s1_auth"
    INT1 = "int_s1_auth"
    D = "diag_s1_seq"

    # Participants / lifelines (model)
    ll_keys = ["ll_s1_usr", "ll_s1_fe", "ll_s1_api", "ll_s1_svc", "ll_s1_db"]
    ll_names = ["Usuario", "Frontend\n(Web o App)", "FastAPI\n/auth/login",
                "AuthService", "PostgreSQL\nusuarios"]
    ll_models = [M("UMLLifeline", k, INT1, n) for k, n in zip(ll_keys, ll_names)]

    # Messages (model) — happy path only
    msg_data = [
        ("msg_s1_01", "ll_s1_usr", "ll_s1_fe",  "Ingresa correo + contraseña"),
        ("msg_s1_02", "ll_s1_fe",  "ll_s1_api", "POST /api/v1/auth/login"),
        ("msg_s1_03", "ll_s1_api", "ll_s1_svc", "autenticar(email, password)"),
        ("msg_s1_04", "ll_s1_svc", "ll_s1_db",  "SELECT * FROM usuarios WHERE correo = email"),
        ("msg_s1_05", "ll_s1_db",  "ll_s1_svc", "registro del usuario", "reply"),
        ("msg_s1_06", "ll_s1_svc", "ll_s1_svc", "verificar bcrypt(password, hash)"),
        ("msg_s1_07", "ll_s1_svc", "ll_s1_api", "usuario autenticado", "reply"),
        ("msg_s1_08", "ll_s1_api", "ll_s1_fe",  "200 OK {access_token}", "reply"),
        ("msg_s1_09", "ll_s1_fe",  "ll_s1_usr", "Redirige al dashboard", "reply"),
    ]
    msg_models = [
        M("UMLMessage", d[0], INT1, d[3],
          messageSort=d[4] if len(d) > 4 else "synchCall",
          source=ref(d[1]), target=ref(d[2]))
        for d in msg_data
    ]

    # Sequence diagram views — lifelines across top, messages down
    LX = [80, 230, 380, 530, 680]   # lifeline x positions
    LCX = [cx + 55 for cx in LX]    # center-x of each lifeline (w=110)
    LL_IDX = {k: i for i, k in enumerate(ll_keys)}

    def _lx(k: str) -> int:
        return LCX[LL_IDX[k]]

    ll_views = [lifeline_v(f"vll_s1_{i}", D, ll_keys[i], LX[i]) for i in range(5)]

    msg_y_start = 120
    msg_step = 55
    msg_views = []
    for j, d in enumerate(msg_data):
        y = msg_y_start + j * msg_step
        x1 = _lx(d[1])
        x2 = _lx(d[2])
        mv = seq_msg_v(
            f"vmsg_s1_{j:02d}", D, d[0],
            f"vll_s1_{LL_IDX[d[1]]}", f"vll_s1_{LL_IDX[d[2]]}",
            x1, y, x2, y,
        )
        msg_views.append(mv)

    seq_diag_view = diag("UMLSequenceDiagram", D, INT1, "Secuencia_Autenticacion_Sprint1",
                         ll_views + msg_views)

    collab_s1 = {
        "_type": "UMLCollaboration",
        "_id": sid(COL1), "_parent": ref(proj_k),
        "name": "Secuencia_Autenticacion_Sprint1",
        "ownedElements": [{
            "_type": "UMLInteraction",
            "_id": sid(INT1), "_parent": ref(COL1),
            "name": "Secuencia_Autenticacion_Sprint1",
            "ownedElements": ll_models + msg_models + [seq_diag_view],
        }],
    }

    return [model_s1, collab_s1]


# ═══════════════════════════════════════════════════════════════════════════
# SPRINT 2
# ═══════════════════════════════════════════════════════════════════════════

def build_sprint2(proj_k: str) -> list[dict]:
    M2 = "m_s2"

    # ── S2.1 Casos de Uso ────────────────────────────────────────────────
    D = "diag_s2_ctx"
    ctx_elems: list[dict] = [
        M("UMLActor",   "a_s2_tec", M2, "Técnico"),
        M("UMLUseCase", "uc_s2_02", M2, "PB-02 Importar plano"),
        M("UMLUseCase", "uc_s2_11", M2, "PB-11 Calibrar escala"),
        M("UMLUseCase", "uc_s2_01", M2, "PB-01 Gestionar proyecto"),
        M_assoc("as_s2_t2",  M2, "a_s2_tec", "uc_s2_02"),
        M_assoc("as_s2_t11", M2, "a_s2_tec", "uc_s2_11"),
        M_assoc("as_s2_t1",  M2, "a_s2_tec", "uc_s2_01"),
        M("UMLDependency", "dep_s2_112", M2, "<<requires>>",
          client=ref("uc_s2_11"), supplier=ref("uc_s2_02")),
    ]
    ctx_views: list[dict] = [
        actor_v("va_s2_tec", D, "a_s2_tec", 40, 200),
        uc_v("vuc_s2_02", D, "uc_s2_02", 220,  60, 175, 40),
        uc_v("vuc_s2_11", D, "uc_s2_11", 220, 160, 175, 40),
        uc_v("vuc_s2_01", D, "uc_s2_01", 220, 310, 195, 40),
        edge_v("UMLAssociationView", "ve_s2_t2",  D, "as_s2_t2",  "va_s2_tec", "vuc_s2_02"),
        edge_v("UMLAssociationView", "ve_s2_t11", D, "as_s2_t11", "va_s2_tec", "vuc_s2_11"),
        edge_v("UMLAssociationView", "ve_s2_t1",  D, "as_s2_t1",  "va_s2_tec", "vuc_s2_01"),
        edge_v("UMLDependencyView",  "ve_s2_d11", D, "dep_s2_112", "vuc_s2_11", "vuc_s2_02"),
    ]
    ctx_diag = diag("UMLUseCaseDiagram", D, M2, "Sprint2_CasosUso", ctx_views)

    # ── S2.2 Clases ──────────────────────────────────────────────────────
    D = "diag_s2_cls"
    cls_elems: list[dict] = [
        M_class("cls_s2_pry", M2, "Proyecto",
                [("id", "entero"), ("nombre", "texto"), ("cliente", "texto"), ("estado", "texto")]),
        M_class("cls_s2_pla", M2, "Plano",
                [("id", "entero"), ("nombre_archivo", "texto"), ("formato", "texto"),
                 ("ancho_px", "entero"), ("alto_px", "entero"), ("escala_m_por_px", "decimal")]),
        M_assoc("ac_s2_pp", M2, "cls_s2_pry", "cls_s2_pla", "contiene", "1", "0..*"),
    ]
    cls_views: list[dict] = [
        class_v("vc_s2_pry", D, "cls_s2_pry",  80,  80, 175, 110),
        class_v("vc_s2_pla", D, "cls_s2_pla", 360,  80, 185, 145),
        edge_v("UMLAssociationView", "ve_s2_pp", D, "ac_s2_pp", "vc_s2_pry", "vc_s2_pla"),
    ]
    cls_diag = diag("UMLClassDiagram", D, M2, "Sprint2_Clases", cls_views)

    all_m2 = ctx_elems + cls_elems + [ctx_diag, cls_diag]
    model_s2 = {"_type": "UMLModel", "_id": sid(M2), "_parent": ref(proj_k),
                "name": "Sprint 2 — Planos y Calibración", "visibility": "public",
                "ownedElements": all_m2}

    # ── S2.3 Secuencia Subida de Plano ───────────────────────────────────
    COL2a = "col_s2_sub"
    INT2a = "int_s2_sub"
    Da = "diag_s2_seq_sub"

    ll2a_keys  = ["ll_s2_tec", "ll_s2_app", "ll_s2_api", "ll_s2_bk", "ll_s2_stor", "ll_s2_db"]
    ll2a_names = ["Tecnico", "PlanoEditorPage", "ApiClient",
                  "Backend /proyectos/{id}/planos", "StorageService", "PostgreSQL"]
    ll2a_models = [M("UMLLifeline", k, INT2a, n) for k, n in zip(ll2a_keys, ll2a_names)]

    msg2a_data = [
        ("msg_s2a_01", "ll_s2_tec",  "ll_s2_app",  "seleccionar archivo"),
        ("msg_s2a_02", "ll_s2_app",  "ll_s2_api",  "POST multipart/form-data"),
        ("msg_s2a_03", "ll_s2_api",  "ll_s2_bk",   "solicitud autenticada"),
        ("msg_s2a_04", "ll_s2_bk",   "ll_s2_stor", "guardar archivo renderizado"),
        ("msg_s2a_05", "ll_s2_bk",   "ll_s2_db",   "insertar metadatos del plano"),
        ("msg_s2a_06", "ll_s2_db",   "ll_s2_bk",   "id y dimensiones", "reply"),
        ("msg_s2a_07", "ll_s2_bk",   "ll_s2_app",  "201 + URL firmada", "reply"),
        ("msg_s2a_08", "ll_s2_app",  "ll_s2_tec",  "renderizar plano", "reply"),
    ]
    msg2a_models = [
        M("UMLMessage", d[0], INT2a, d[3],
          messageSort=d[4] if len(d) > 4 else "synchCall",
          source=ref(d[1]), target=ref(d[2]))
        for d in msg2a_data
    ]

    LX2a = [60, 210, 360, 510, 660, 810]
    LCX2a = [x + 55 for x in LX2a]
    LL2a_IDX = {k: i for i, k in enumerate(ll2a_keys)}

    ll2a_views = [lifeline_v(f"vll_s2a_{i}", Da, ll2a_keys[i], LX2a[i]) for i in range(6)]
    msg2a_views = []
    for j, d in enumerate(msg2a_data):
        y = 120 + j * 55
        mv = seq_msg_v(
            f"vmsg_s2a_{j:02d}", Da, d[0],
            f"vll_s2a_{LL2a_IDX[d[1]]}", f"vll_s2a_{LL2a_IDX[d[2]]}",
            LCX2a[LL2a_IDX[d[1]]], y, LCX2a[LL2a_IDX[d[2]]], y,
        )
        msg2a_views.append(mv)

    seq2a_diag = diag("UMLSequenceDiagram", Da, INT2a,
                      "Sprint2_Secuencia_Subida", ll2a_views + msg2a_views)

    collab_s2a = {
        "_type": "UMLCollaboration", "_id": sid(COL2a), "_parent": ref(proj_k),
        "name": "Sprint2_Secuencia_Subida",
        "ownedElements": [{
            "_type": "UMLInteraction", "_id": sid(INT2a), "_parent": ref(COL2a),
            "name": "Sprint2_Secuencia_Subida",
            "ownedElements": ll2a_models + msg2a_models + [seq2a_diag],
        }],
    }

    # ── S2.4 Secuencia Calibración ───────────────────────────────────────
    COL2b = "col_s2_cal"
    INT2b = "int_s2_cal"
    Db = "diag_s2_seq_cal"

    ll2b_keys  = ["ll_s2b_tec", "ll_s2b_app", "ll_s2b_cub", "ll_s2b_bk", "ll_s2b_db"]
    ll2b_names = ["Tecnico", "PlanoEditorPage", "PlanosCubit",
                  "Backend /planos/{id}/calibracion", "PostgreSQL"]
    ll2b_models = [M("UMLLifeline", k, INT2b, n) for k, n in zip(ll2b_keys, ll2b_names)]

    msg2b_data = [
        ("msg_s2b_01", "ll_s2b_tec", "ll_s2b_app", "tocar dos puntos"),
        ("msg_s2b_02", "ll_s2b_app", "ll_s2b_tec", "solicitar distancia real", "reply"),
        ("msg_s2b_03", "ll_s2b_tec", "ll_s2b_app", "ingresar metros"),
        ("msg_s2b_04", "ll_s2b_app", "ll_s2b_cub", "confirmar calibración"),
        ("msg_s2b_05", "ll_s2b_cub", "ll_s2b_bk",  "PATCH calibracion"),
        ("msg_s2b_06", "ll_s2b_bk",  "ll_s2b_db",  "actualizar escala y puntos referencia"),
        ("msg_s2b_07", "ll_s2b_db",  "ll_s2b_bk",  "calibración persistida", "reply"),
        ("msg_s2b_08", "ll_s2b_bk",  "ll_s2b_cub", "plano calibrado", "reply"),
        ("msg_s2b_09", "ll_s2b_cub", "ll_s2b_app", "estado exitoso", "reply"),
        ("msg_s2b_10", "ll_s2b_app", "ll_s2b_tec", "mostrar factor y regla", "reply"),
    ]
    msg2b_models = [
        M("UMLMessage", d[0], INT2b, d[3],
          messageSort=d[4] if len(d) > 4 else "synchCall",
          source=ref(d[1]), target=ref(d[2]))
        for d in msg2b_data
    ]

    LX2b = [60, 210, 380, 550, 730]
    LCX2b = [x + 55 for x in LX2b]
    LL2b_IDX = {k: i for i, k in enumerate(ll2b_keys)}

    ll2b_views = [lifeline_v(f"vll_s2b_{i}", Db, ll2b_keys[i], LX2b[i]) for i in range(5)]
    msg2b_views = []
    for j, d in enumerate(msg2b_data):
        y = 120 + j * 55
        mv = seq_msg_v(
            f"vmsg_s2b_{j:02d}", Db, d[0],
            f"vll_s2b_{LL2b_IDX[d[1]]}", f"vll_s2b_{LL2b_IDX[d[2]]}",
            LCX2b[LL2b_IDX[d[1]]], y, LCX2b[LL2b_IDX[d[2]]], y,
        )
        msg2b_views.append(mv)

    seq2b_diag = diag("UMLSequenceDiagram", Db, INT2b,
                      "Sprint2_Secuencia_Calibracion", ll2b_views + msg2b_views)

    collab_s2b = {
        "_type": "UMLCollaboration", "_id": sid(COL2b), "_parent": ref(proj_k),
        "name": "Sprint2_Secuencia_Calibracion",
        "ownedElements": [{
            "_type": "UMLInteraction", "_id": sid(INT2b), "_parent": ref(COL2b),
            "name": "Sprint2_Secuencia_Calibracion",
            "ownedElements": ll2b_models + msg2b_models + [seq2b_diag],
        }],
    }

    return [model_s2, collab_s2a, collab_s2b]


# ═══════════════════════════════════════════════════════════════════════════
# SPRINT 3
# ═══════════════════════════════════════════════════════════════════════════

def build_sprint3(proj_k: str) -> list[dict]:
    M3 = "m_s3"

    # ── S3.1 Casos de Uso ────────────────────────────────────────────────
    D = "diag_s3_ctx"
    ctx_elems: list[dict] = [
        M("UMLActor",   "a_s3_tec", M3, "Técnico"),
        M("UMLUseCase", "uc_s3_03", M3, "PB-03 Capturar señales WiFi"),
        M("UMLUseCase", "uc_s3_04", M3, "PB-04 Marcar puntos de medición"),
        M("UMLUseCase", "uc_s3_11", M3, "PB-11 Plano calibrado"),
        M_assoc("as_s3_t3",  M3, "a_s3_tec", "uc_s3_03"),
        M_assoc("as_s3_t4",  M3, "a_s3_tec", "uc_s3_04"),
        M("UMLDependency", "dep_s3_311", M3, "<<requires>>",
          client=ref("uc_s3_03"), supplier=ref("uc_s3_11")),
        M("UMLInclude", "inc_s3_43", M3, "",
          client=ref("uc_s3_04"), supplier=ref("uc_s3_03")),
    ]
    ctx_views: list[dict] = [
        actor_v("va_s3_tec", D, "a_s3_tec", 40, 200),
        uc_v("vuc_s3_03", D, "uc_s3_03", 220,  60, 200, 40),
        uc_v("vuc_s3_04", D, "uc_s3_04", 220, 160, 220, 40),
        uc_v("vuc_s3_11", D, "uc_s3_11", 220, 310, 190, 40),
        edge_v("UMLAssociationView", "ve_s3_t3",  D, "as_s3_t3",  "va_s3_tec", "vuc_s3_03"),
        edge_v("UMLAssociationView", "ve_s3_t4",  D, "as_s3_t4",  "va_s3_tec", "vuc_s3_04"),
        edge_v("UMLDependencyView",  "ve_s3_d31", D, "dep_s3_311", "vuc_s3_03", "vuc_s3_11"),
        edge_v("UMLIncludeView",     "ve_s3_i43", D, "inc_s3_43",  "vuc_s3_04", "vuc_s3_03"),
    ]
    ctx_diag = diag("UMLUseCaseDiagram", D, M3, "Sprint3_CasosUso", ctx_views)

    all_m3 = ctx_elems + [ctx_diag]
    model_s3 = {"_type": "UMLModel", "_id": sid(M3), "_parent": ref(proj_k),
                "name": "Sprint 3 — Captura WiFi en Línea", "visibility": "public",
                "ownedElements": all_m3}

    # ── S3.2 Secuencia Captura WiFi ──────────────────────────────────────
    COL3 = "col_s3_cap"
    INT3 = "int_s3_cap"
    D3 = "diag_s3_seq"

    ll3_keys  = ["ll_s3_tec", "ll_s3_app", "ll_s3_scan", "ll_s3_cub", "ll_s3_bk", "ll_s3_db"]
    ll3_names = ["Tecnico", "CapturaPage", "WifiScanner",
                 "CapturaCubit", "Backend /mediciones", "PostgreSQL"]
    ll3_models = [M("UMLLifeline", k, INT3, n) for k, n in zip(ll3_keys, ll3_names)]

    msg3_data = [
        ("msg_s3_01", "ll_s3_tec",  "ll_s3_app",  "tocar punto en plano"),
        ("msg_s3_02", "ll_s3_app",  "ll_s3_scan", "iniciar escaneo"),
        ("msg_s3_03", "ll_s3_scan", "ll_s3_app",  "resultados WiFi", "reply"),
        ("msg_s3_04", "ll_s3_app",  "ll_s3_cub",  "enviar lote"),
        ("msg_s3_05", "ll_s3_cub",  "ll_s3_bk",   "POST /api/mediciones"),
        ("msg_s3_06", "ll_s3_bk",   "ll_s3_db",   "insertar punto y mediciones"),
        ("msg_s3_07", "ll_s3_db",   "ll_s3_bk",   "ids y nivel", "reply"),
        ("msg_s3_08", "ll_s3_bk",   "ll_s3_cub",  "201 Created", "reply"),
        ("msg_s3_09", "ll_s3_cub",  "ll_s3_app",  "actualizar plano", "reply"),
        ("msg_s3_10", "ll_s3_app",  "ll_s3_tec",  "mostrar badge por nivel", "reply"),
    ]
    msg3_models = [
        M("UMLMessage", d[0], INT3, d[3],
          messageSort=d[4] if len(d) > 4 else "synchCall",
          source=ref(d[1]), target=ref(d[2]))
        for d in msg3_data
    ]

    LX3 = [50, 200, 360, 520, 680, 840]
    LCX3 = [x + 55 for x in LX3]
    LL3_IDX = {k: i for i, k in enumerate(ll3_keys)}

    ll3_views = [lifeline_v(f"vll_s3_{i}", D3, ll3_keys[i], LX3[i]) for i in range(6)]
    msg3_views = []
    for j, d in enumerate(msg3_data):
        y = 120 + j * 55
        mv = seq_msg_v(
            f"vmsg_s3_{j:02d}", D3, d[0],
            f"vll_s3_{LL3_IDX[d[1]]}", f"vll_s3_{LL3_IDX[d[2]]}",
            LCX3[LL3_IDX[d[1]]], y, LCX3[LL3_IDX[d[2]]], y,
        )
        msg3_views.append(mv)

    seq3_diag = diag("UMLSequenceDiagram", D3, INT3,
                     "Sprint3_Secuencia_Captura", ll3_views + msg3_views)

    collab_s3 = {
        "_type": "UMLCollaboration", "_id": sid(COL3), "_parent": ref(proj_k),
        "name": "Sprint3_Secuencia_Captura",
        "ownedElements": [{
            "_type": "UMLInteraction", "_id": sid(INT3), "_parent": ref(COL3),
            "name": "Sprint3_Secuencia_Captura",
            "ownedElements": ll3_models + msg3_models + [seq3_diag],
        }],
    }

    # ── S3.3 Diagrama de Estados ─────────────────────────────────────────
    SM = "sm_s3_estados"
    D_st = "diag_s3_st"

    state_keys = [
        "st_s3_ini", "st_s3_inac", "st_s3_load", "st_s3_act",
        "st_s3_env", "st_s3_thro", "st_s3_pau", "st_s3_det",
        "st_s3_err", "st_s3_fin",
    ]
    state_names = [
        None,          # pseudostate initial
        "Inactiva", "Loading", "Activa",
        "Enviando", "Throttling", "Pausada", "PuntoDetalle",
        "Error", None,  # final state
    ]

    state_models: list[dict] = []
    # Initial pseudostate
    state_models.append(M("UMLPseudostate", "st_s3_ini", SM, "", kind="initial"))
    # Named states
    for k, n in zip(state_keys[1:-1], state_names[1:-1]):
        state_models.append(M("UMLState", k, SM, n))
    # Final state
    state_models.append(M("UMLFinalState", "st_s3_fin", SM, ""))

    trans_data = [
        ("tr_s3_01", "st_s3_ini",  "st_s3_inac", ""),
        ("tr_s3_02", "st_s3_inac", "st_s3_load", "iniciarSesion"),
        ("tr_s3_03", "st_s3_load", "st_s3_act",  "puntos cargados"),
        ("tr_s3_04", "st_s3_act",  "st_s3_env",  "marcarPunto"),
        ("tr_s3_05", "st_s3_env",  "st_s3_act",  "lote persistido"),
        ("tr_s3_06", "st_s3_act",  "st_s3_thro", "limite alcanzado"),
        ("tr_s3_07", "st_s3_thro", "st_s3_act",  "tiempo liberado"),
        ("tr_s3_08", "st_s3_act",  "st_s3_pau",  "sin conectividad"),
        ("tr_s3_09", "st_s3_pau",  "st_s3_act",  "reanudar"),
        ("tr_s3_10", "st_s3_act",  "st_s3_det",  "abrirDetallePunto"),
        ("tr_s3_11", "st_s3_det",  "st_s3_act",  "cerrarDetalle"),
        ("tr_s3_12", "st_s3_env",  "st_s3_err",  "fallo de envio"),
        ("tr_s3_13", "st_s3_err",  "st_s3_act",  "reintentar"),
        ("tr_s3_14", "st_s3_act",  "st_s3_inac", "detenerSesion"),
    ]
    trans_models = [
        M("UMLTransition", d[0], SM, d[3], source=ref(d[1]), target=ref(d[2]))
        for d in trans_data
    ]

    # State diagram views (arranged in a flow)
    # Layout: 2-column arrangement
    #   Col A (x=60):  ini, Inactiva, Loading, Activa, Inactiva(loop back)
    #   Col B (x=300): Enviando, Throttling, Pausada, PuntoDetalle, Error, Final
    ST_POS = {
        "st_s3_ini":  (180,  20),
        "st_s3_inac": (130,  80),
        "st_s3_load": (130, 160),
        "st_s3_act":  (130, 240),
        "st_s3_env":  (350, 160),
        "st_s3_thro": (350, 240),
        "st_s3_pau":  (550, 160),
        "st_s3_det":  (550, 240),
        "st_s3_err":  (350, 340),
        "st_s3_fin":  (130, 440),
    }

    state_views: list[dict] = []
    # Initial pseudostate
    px, py = ST_POS["st_s3_ini"]
    state_views.append(pseudo_v("vst_s3_ini", D_st, "st_s3_ini", px, py))
    # Named states
    for k, n in zip(state_keys[1:-1], state_names[1:-1]):
        sx, sy = ST_POS[k]
        state_views.append(state_v(f"vst_{k}", D_st, k, sx, sy, 130, 40))
    # Final state
    fx, fy = ST_POS["st_s3_fin"]
    state_views.append(final_v("vst_s3_fin", D_st, "st_s3_fin", fx, fy))

    # Transition views
    VIEW_KEY = {k: (f"vst_s3_ini" if k == "st_s3_ini" else
                    f"vst_s3_fin" if k == "st_s3_fin" else
                    f"vst_{k}")
                for k in state_keys}

    trans_views: list[dict] = []
    for d in trans_data:
        ovs, refs_ = _simple_labs(f"vtr_{d[0]}", d[0])
        v: dict = {
            "_type": "UMLTransitionView",
            "_id": sid(f"vtr_{d[0]}"), "_parent": ref(D_st), "model": ref(d[0]),
            "tail": ref(VIEW_KEY[d[1]]), "head": ref(VIEW_KEY[d[2]]),
            "lineColor": BORDER, "visible": True, "enabled": True,
            "ownedViews": ovs,
        }
        v.update(refs_)
        trans_views.append(v)

    st_diag = diag("UMLStatechartDiagram", D_st, SM, "Sprint3_Estados",
                   state_views + trans_views)

    statemachine_s3 = {
        "_type": "UMLStateMachine",
        "_id": sid(SM), "_parent": ref(proj_k),
        "name": "Sprint3_Estados",
        "ownedElements": state_models + trans_models + [st_diag],
    }

    return [model_s3, collab_s3, statemachine_s3]


# ═══════════════════════════════════════════════════════════════════════════
# ENSAMBLADO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def build_project() -> dict:
    PROJ = "proj_paneles_whm"
    owned: list[dict] = []
    owned.extend(build_sprint0(PROJ))
    owned.extend(build_sprint1(PROJ))
    owned.extend(build_sprint2(PROJ))
    owned.extend(build_sprint3(PROJ))

    return {
        "_type": "Project",
        "_id": sid(PROJ),
        "name": "Paneles-WHM",
        "ownedElements": owned,
    }


def main() -> None:
    if OUTPUT.exists():
        print(f"[AVISO] El archivo ya existe: {OUTPUT}")
        resp = input("  ¿Sobreescribir? (s/N): ").strip().lower()
        if resp != "s":
            print("Cancelado.")
            return

    project = build_project()
    OUTPUT.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"[OK] Generado: {OUTPUT}  ({size_kb:.1f} KB)")

    # Conteo de diagramas
    diagram_types = {
        "UMLUseCaseDiagram", "UMLClassDiagram", "UMLPackageDiagram",
        "UMLDeploymentDiagram", "UMLSequenceDiagram", "UMLStatechartDiagram",
    }
    raw = json.dumps(project)
    for t in sorted(diagram_types):
        count = raw.count(f'"_type": "{t}"')
        if count:
            print(f"  {t}: {count}")


if __name__ == "__main__":
    main()
