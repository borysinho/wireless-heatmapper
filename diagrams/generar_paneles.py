"""
generar_paneles.py
==================
Genera diagrams/Paneles-WHM.mdj con los 16 diagramas UML 2.5+
del proyecto Wireless HeatMapper, basados en docs/PANELES.

Uso:
    python diagrams/generar_paneles.py

Salida:
    diagrams/Paneles-WHM.mdj  (NO sobreescribe sin confirmación)

Correcciones aplicadas frente a la versión anterior:
  - Posición: "left"/"top" (NO "x"/"y")
  - Vistas anidadas en vistas: "subViews" (NO "ownedViews")
  - Diagrama → sus hijos directos: "ownedViews"
  - Compartimentos (nameCompartment etc.) como $ref + en subViews
  - Edge labels con campo "hostEdge" en subViews
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

OUTPUT = Path(__file__).parent / "Paneles-WHM.mdj"

FILL   = "#EBF5FB"
BORDER = "#2980B9"

# ─────────────────────────── IDs deterministas ─────────────────────────────
def sid(key: str) -> str:
    return hashlib.md5(key.encode("utf-8")).hexdigest()

def ref(k: str) -> dict:
    return {"$ref": sid(k)}

# ─────────────────────────── Helpers de modelos ────────────────────────────
def M(tp: str, k: str, pk: str, name: str = "", **kw) -> dict:
    e: dict = {"_type": tp, "_id": sid(k), "_parent": ref(pk), "name": name}
    e.update(kw)
    return e

def M_class(k: str, pk: str, name: str,
            attrs: list[tuple] | None = None) -> dict:
    e = M("UMLClass", k, pk, name, visibility="public")
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

# ─────────────────────────── Compartimentos ocultos ────────────────────────
def _hid(tp: str, sub_id: str, pvk: str, mk: str) -> dict:
    return {"_type": tp, "_id": sub_id, "_parent": ref(pvk), "model": ref(mk),
            "parentStyle": True, "visible": False,
            "left": -232, "top": -48, "width": 10, "height": 10}

def _nc(nc_id: str, pvk: str, mk: str, lx: int, ly: int, w: int, h: int = 25) -> dict:
    return {"_type": "UMLNameCompartmentView", "_id": nc_id,
            "_parent": ref(pvk), "model": ref(mk),
            "parentStyle": True, "left": lx, "top": ly, "width": w, "height": h}

def _ac(ac_id: str, pvk: str, mk: str, lx: int, ly: int, w: int, h: int,
        visible: bool = True) -> dict:
    return {"_type": "UMLAttributeCompartmentView", "_id": ac_id,
            "_parent": ref(pvk), "model": ref(mk),
            "parentStyle": True, "visible": visible,
            "left": lx, "top": ly, "width": w, "height": h}

# ─────────────────────────── Vistas de nodos ───────────────────────────────
def actor_v(vk: str, dk: str, mk: str, x: int, y: int) -> dict:
    w, h = 40, 65
    return {
        "_type": "UMLActorView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "fillColor": FILL, "lineColor": BORDER,
        "parentStyle": False, "containerChangeable": True,
        "left": x, "top": y, "width": w, "height": h,
        "suppressAttributes": True, "suppressOperations": True,
        "nameCompartment": ref(f"{vk}_nc"),
        "attributeCompartment": ref(f"{vk}_ac"),
        "operationCompartment": ref(f"{vk}_oc"),
        "receptionCompartment": ref(f"{vk}_rc"),
        "templateParameterCompartment": ref(f"{vk}_tc"),
        "subViews": [
            _nc(sid(f"{vk}_nc"), vk, mk, x, y, w, 25),
            _hid("UMLAttributeCompartmentView",  sid(f"{vk}_ac"), vk, mk),
            _hid("UMLOperationCompartmentView",  sid(f"{vk}_oc"), vk, mk),
            _hid("UMLReceptionCompartmentView",  sid(f"{vk}_rc"), vk, mk),
            _hid("UMLTemplateParameterCompartmentView", sid(f"{vk}_tc"), vk, mk),
        ],
    }

def uc_v(vk: str, dk: str, mk: str, x: int, y: int,
         w: int = 150, h: int = 44) -> dict:
    return {
        "_type": "UMLUseCaseView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "fillColor": FILL, "lineColor": BORDER,
        "parentStyle": False, "containerChangeable": True,
        "left": x, "top": y, "width": w, "height": h,
        "wordWrap": True,
        "suppressAttributes": True, "suppressOperations": True,
        "nameCompartment": ref(f"{vk}_nc"),
        "attributeCompartment": ref(f"{vk}_ac"),
        "operationCompartment": ref(f"{vk}_oc"),
        "receptionCompartment": ref(f"{vk}_rc"),
        "templateParameterCompartment": ref(f"{vk}_tc"),
        "extensionPointCompartment": ref(f"{vk}_ep"),
        "subViews": [
            _nc(sid(f"{vk}_nc"), vk, mk, x, y, w, min(h, 38)),
            _hid("UMLAttributeCompartmentView",      sid(f"{vk}_ac"), vk, mk),
            _hid("UMLOperationCompartmentView",      sid(f"{vk}_oc"), vk, mk),
            _hid("UMLReceptionCompartmentView",      sid(f"{vk}_rc"), vk, mk),
            _hid("UMLTemplateParameterCompartmentView", sid(f"{vk}_tc"), vk, mk),
            _hid("UMLExtensionPointCompartmentView", sid(f"{vk}_ep"), vk, mk),
        ],
    }

def class_v(vk: str, dk: str, mk: str, x: int, y: int,
            w: int = 165, h: int = 110) -> dict:
    NC_H = 25
    ac_h = max(10, h - NC_H)
    return {
        "_type": "UMLClassView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "fillColor": FILL, "lineColor": BORDER,
        "parentStyle": False, "containerChangeable": True,
        "left": x, "top": y, "width": w, "height": h,
        "nameCompartment": ref(f"{vk}_nc"),
        "attributeCompartment": ref(f"{vk}_ac"),
        "operationCompartment": ref(f"{vk}_oc"),
        "receptionCompartment": ref(f"{vk}_rc"),
        "templateParameterCompartment": ref(f"{vk}_tc"),
        "subViews": [
            _nc(sid(f"{vk}_nc"), vk, mk, x, y, w, NC_H),
            _ac(sid(f"{vk}_ac"), vk, mk, x, y + NC_H, w, ac_h),
            {"_type": "UMLOperationCompartmentView", "_id": sid(f"{vk}_oc"),
             "_parent": ref(vk), "model": ref(mk),
             "parentStyle": True, "visible": False,
             "left": x, "top": y + h, "width": w, "height": 10},
            _hid("UMLReceptionCompartmentView",  sid(f"{vk}_rc"), vk, mk),
            _hid("UMLTemplateParameterCompartmentView", sid(f"{vk}_tc"), vk, mk),
        ],
    }

def pkg_v(vk: str, dk: str, mk: str, x: int, y: int,
          w: int = 210, h: int = 120) -> dict:
    return {
        "_type": "UMLPackageView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "fillColor": FILL, "lineColor": BORDER,
        "parentStyle": False, "containerChangeable": True,
        "left": x, "top": y, "width": w, "height": h,
        "nameCompartment": ref(f"{vk}_nc"),
        "subViews": [_nc(sid(f"{vk}_nc"), vk, mk, x, y, w, 25)],
    }

def node_v(vk: str, dk: str, mk: str, x: int, y: int,
           w: int = 190, h: int = 80) -> dict:
    return {
        "_type": "UMLNodeView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "fillColor": FILL, "lineColor": BORDER,
        "parentStyle": False, "containerChangeable": True,
        "left": x, "top": y, "width": w, "height": h,
        "suppressAttributes": True, "suppressOperations": True,
        "nameCompartment": ref(f"{vk}_nc"),
        "attributeCompartment": ref(f"{vk}_ac"),
        "operationCompartment": ref(f"{vk}_oc"),
        "receptionCompartment": ref(f"{vk}_rc"),
        "templateParameterCompartment": ref(f"{vk}_tc"),
        "subViews": [
            _nc(sid(f"{vk}_nc"), vk, mk, x, y, w, 25),
            _hid("UMLAttributeCompartmentView",  sid(f"{vk}_ac"), vk, mk),
            _hid("UMLOperationCompartmentView",  sid(f"{vk}_oc"), vk, mk),
            _hid("UMLReceptionCompartmentView",  sid(f"{vk}_rc"), vk, mk),
            _hid("UMLTemplateParameterCompartmentView", sid(f"{vk}_tc"), vk, mk),
        ],
    }

def artifact_v(vk: str, dk: str, mk: str, x: int, y: int,
               w: int = 150, h: int = 38) -> dict:
    return {
        "_type": "UMLArtifactView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "fillColor": FILL, "lineColor": BORDER,
        "parentStyle": False, "left": x, "top": y, "width": w, "height": h,
        "nameCompartment": ref(f"{vk}_nc"),
        "subViews": [_nc(sid(f"{vk}_nc"), vk, mk, x, y, w, 25)],
    }

def lifeline_v(vk: str, dk: str, mk: str, x: int,
               y: int = 32, w: int = 120, ll_h: int = 500) -> dict:
    BOX_H = 40
    nc_id = sid(f"{vk}_nc")
    lp_id = sid(f"{vk}_lp")
    return {
        "_type": "UMLSeqLifelineView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "fillColor": FILL, "lineColor": BORDER,
        "parentStyle": False,
        "left": x, "top": y, "width": w, "height": ll_h,
        "stereotypeDisplay": "icon",
        "nameCompartment": {"$ref": nc_id},
        "linePart": {"$ref": lp_id},
        "subViews": [
            {"_type": "UMLNameCompartmentView", "_id": nc_id,
             "_parent": ref(vk), "model": ref(mk),
             "parentStyle": True,
             "left": x, "top": y, "width": w, "height": BOX_H},
            {"_type": "UMLLinePartView", "_id": lp_id,
             "_parent": ref(vk), "model": ref(mk),
             "parentStyle": False,
             "left": x + w // 2, "top": y + BOX_H,
             "width": 1, "height": ll_h - BOX_H},
        ],
    }

def state_v(vk: str, dk: str, mk: str, x: int, y: int,
            w: int = 140, h: int = 44) -> dict:
    return {
        "_type": "UMLStateView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "fillColor": FILL, "lineColor": BORDER,
        "parentStyle": False,
        "left": x, "top": y, "width": w, "height": h,
        "nameCompartment": ref(f"{vk}_nc"),
        "subViews": [_nc(sid(f"{vk}_nc"), vk, mk, x, y, w, h)],
    }

def pseudo_v(vk: str, dk: str, mk: str, x: int, y: int) -> dict:
    return {"_type": "UMLPseudostateView", "_id": sid(vk),
            "_parent": ref(dk), "model": ref(mk),
            "fillColor": BORDER, "lineColor": BORDER,
            "parentStyle": False, "left": x, "top": y, "width": 20, "height": 20}

def final_v(vk: str, dk: str, mk: str, x: int, y: int) -> dict:
    return {"_type": "UMLFinalStateView", "_id": sid(vk),
            "_parent": ref(dk), "model": ref(mk),
            "fillColor": BORDER, "lineColor": BORDER,
            "parentStyle": False, "left": x, "top": y, "width": 25, "height": 25}

# ─────────────────────────── Vistas de aristas ─────────────────────────────
def _elv_sub(vk: str, edge_vk: str, mk: str,
             lx: int = 0, ly: int = 0,
             visible: bool = False, ep: int = 1,
             a: float = 1.5708, d: float = 15.0) -> dict:
    return {
        "_type": "EdgeLabelView", "_id": sid(vk),
        "_parent": ref(edge_vk), "model": ref(mk),
        "visible": visible, "parentStyle": False,
        "left": lx, "top": ly, "height": 13,
        "alpha": a, "distance": d,
        "hostEdge": ref(edge_vk), "edgePosition": ep,
    }

def edge_v(tp: str, vk: str, dk: str, mk: str,
           tail_vk: str, head_vk: str) -> dict:
    nl = _elv_sub(f"{vk}_nl", vk, mk, visible=True, ep=1)
    sl = _elv_sub(f"{vk}_sl", vk, mk, visible=False, ep=1, a=1.5708, d=30)
    pl = _elv_sub(f"{vk}_pl", vk, mk, visible=False, ep=2, a=-1.5708, d=15)
    sub = [nl, sl, pl]
    v: dict = {
        "_type": tp, "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "lineColor": BORDER, "parentStyle": False,
        "head": ref(head_vk), "tail": ref(tail_vk),
        "nameLabel":       {"$ref": sid(f"{vk}_nl")},
        "stereotypeLabel": {"$ref": sid(f"{vk}_sl")},
        "propertyLabel":   {"$ref": sid(f"{vk}_pl")},
        "subViews": sub,
    }
    if tp == "UMLAssociationView":
        extra_keys = [
            (f"{vk}_hml", 2, 0.5236, 25),
            (f"{vk}_tml", 0, -0.5236, 25),
            (f"{vk}_hql", 2, -0.5236, 15),
            (f"{vk}_tql", 0, 0.5236, 15),
            (f"{vk}_hrn", 2, 0.5236, 15),
            (f"{vk}_trn", 0, -0.5236, 15),
            (f"{vk}_hpp", 2, -0.5236, 25),
            (f"{vk}_tpp", 0, 0.5236, 25),
        ]
        for ek, ep, a, d in extra_keys:
            sub.append(_elv_sub(ek, vk, mk, ep=ep, a=a, d=d))
        v["headMultiplicityLabel"]      = {"$ref": sid(f"{vk}_hml")}
        v["tailMultiplicityLabel"]      = {"$ref": sid(f"{vk}_tml")}
        v["headQualifiersCompartment"]  = {"$ref": sid(f"{vk}_hql")}
        v["tailQualifiersCompartment"]  = {"$ref": sid(f"{vk}_tql")}
        v["headRoleNameLabel"]          = {"$ref": sid(f"{vk}_hrn")}
        v["tailRoleNameLabel"]          = {"$ref": sid(f"{vk}_trn")}
        v["headPropertyLabel"]          = {"$ref": sid(f"{vk}_hpp")}
        v["tailPropertyLabel"]          = {"$ref": sid(f"{vk}_tpp")}
        v["showVisibility"] = True
        v["lineStyle"] = 3
        v["showEndOrder"] = "hide"
    else:
        v["showVisibility"] = True
        v["lineStyle"] = 1
    return v

def seq_msg_v(vk: str, dk: str, mk: str,
              tail_vk: str, head_vk: str,
              x1: int, y1: int, x2: int, y2: int) -> dict:
    mid_x = (x1 + x2) // 2
    nl_id  = sid(f"{vk}_nl")
    sl_id  = sid(f"{vk}_sl")
    pl_id  = sid(f"{vk}_pl")
    act_id = sid(f"{vk}_act")
    return {
        "_type": "UMLSeqMessageView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "lineColor": BORDER, "parentStyle": False,
        "head": ref(head_vk), "tail": ref(tail_vk),
        "points": f"{x1}:{y1};{x2}:{y2}",
        "nameLabel":       {"$ref": nl_id},
        "stereotypeLabel": {"$ref": sl_id},
        "propertyLabel":   {"$ref": pl_id},
        "activation":      {"$ref": act_id},
        "subViews": [
            {"_type": "EdgeLabelView", "_id": nl_id,
             "_parent": ref(vk), "model": ref(mk),
             "visible": True, "parentStyle": False,
             "left": mid_x, "top": y1 - 12, "height": 13,
             "alpha": 1.5708, "distance": 15,
             "hostEdge": ref(vk), "edgePosition": 1},
            {"_type": "EdgeLabelView", "_id": sl_id,
             "_parent": ref(vk), "model": ref(mk),
             "visible": False, "parentStyle": False,
             "left": mid_x, "top": y1, "height": 13,
             "alpha": 1.5708, "distance": 30,
             "hostEdge": ref(vk), "edgePosition": 1},
            {"_type": "EdgeLabelView", "_id": pl_id,
             "_parent": ref(vk), "model": ref(mk),
             "visible": False, "parentStyle": False,
             "left": mid_x, "top": y1 + 12, "height": 13,
             "alpha": -1.5708, "distance": 15,
             "hostEdge": ref(vk), "edgePosition": 2},
            {"_type": "UMLActivationView", "_id": act_id,
             "_parent": ref(vk), "model": ref(mk),
             "visible": False, "parentStyle": False,
             "left": x2, "top": y2, "width": 10, "height": 20},
        ],
    }

def trans_v(vk: str, dk: str, mk: str,
            tail_vk: str, head_vk: str) -> dict:
    nl = _elv_sub(f"{vk}_nl", vk, mk, visible=True, ep=1)
    sl = _elv_sub(f"{vk}_sl", vk, mk, visible=False, ep=1, a=1.5708, d=30)
    pl = _elv_sub(f"{vk}_pl", vk, mk, visible=False, ep=2, a=-1.5708, d=15)
    return {
        "_type": "UMLTransitionView", "_id": sid(vk),
        "_parent": ref(dk), "model": ref(mk),
        "lineColor": BORDER, "parentStyle": False,
        "head": ref(head_vk), "tail": ref(tail_vk),
        "lineStyle": 1,
        "nameLabel":       {"$ref": sid(f"{vk}_nl")},
        "stereotypeLabel": {"$ref": sid(f"{vk}_sl")},
        "propertyLabel":   {"$ref": sid(f"{vk}_pl")},
        "subViews": [nl, sl, pl],
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

    # S0.1 Contexto
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
        M_assoc("as_s0_a1",  M0, "a_s0_adm", "uc_s0_01"),
        M_assoc("as_s0_a2",  M0, "a_s0_adm", "uc_s0_02"),
        M_assoc("as_s0_a9",  M0, "a_s0_adm", "uc_s0_09"),
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
        actor_v("va_s0_adm", D, "a_s0_adm",  30,  50),
        actor_v("va_s0_tec", D, "a_s0_tec",  30, 310),
        actor_v("va_s0_cli", D, "a_s0_cli",  30, 495),
        actor_v("va_s0_ia",  D, "a_s0_ia",  730, 385),
        uc_v("vuc_s0_01", D, "uc_s0_01", 190,  30, 165, 44),
        uc_v("vuc_s0_02", D, "uc_s0_02", 190,  90, 155, 44),
        uc_v("vuc_s0_09", D, "uc_s0_09", 190, 150, 165, 44),
        uc_v("vuc_s0_13", D, "uc_s0_13", 450,  30, 175, 44),
        uc_v("vuc_s0_18", D, "uc_s0_18", 450,  90, 205, 44),
        uc_v("vuc_s0_07", D, "uc_s0_07", 450, 150, 210, 44),
        uc_v("vuc_s0_08", D, "uc_s0_08", 450, 215, 175, 44),
        uc_v("vuc_s0_19", D, "uc_s0_19", 190, 275, 215, 44),
        uc_v("vuc_s0_03", D, "uc_s0_03", 190, 340, 185, 44),
        uc_v("vuc_s0_04", D, "uc_s0_04", 450, 275, 225, 44),
        uc_v("vuc_s0_05", D, "uc_s0_05", 450, 340, 200, 44),
        uc_v("vuc_s0_06", D, "uc_s0_06", 450, 410, 210, 44),
        uc_v("vuc_s0_10", D, "uc_s0_10", 190, 495, 200, 44),
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

    # S0.2 Paquetes
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
        pkg_v("vp_s0_mob", D, "pkg_s0_mob",  40,  40, 210, 120),
        pkg_v("vp_s0_bk",  D, "pkg_s0_bk",  310,  40, 210, 120),
        pkg_v("vp_s0_web", D, "pkg_s0_web",  580,  40, 220, 120),
        pkg_v("vp_s0_db",  D, "pkg_s0_db",  310, 220, 210,  90),
        edge_v("UMLDependencyView", "ve_s0_mb", D, "dep_s0_mb", "vp_s0_mob", "vp_s0_bk"),
        edge_v("UMLDependencyView", "ve_s0_wb", D, "dep_s0_wb", "vp_s0_web", "vp_s0_bk"),
        edge_v("UMLDependencyView", "ve_s0_bd", D, "dep_s0_bd", "vp_s0_bk",  "vp_s0_db"),
    ]
    pkg_diag = diag("UMLPackageDiagram", D, M0, "Arquitectura_Paquetes_Sprint0", pkg_views)

    # S0.3 Despliegue
    D = "diag_s0_dep"
    dep_elems: list[dict] = [
        M("UMLNode",     "nd_s0_and",  M0, "Dispositivo Android (Técnico)"),
        M("UMLNode",     "nd_s0_ngx",  M0, "Nginx (Reverse Proxy)"),
        M("UMLNode",     "nd_s0_api",  M0, "FastAPI (Backend REST + IA)"),
        M("UMLNode",     "nd_s0_app",  M0, "React App (Panel Web)"),
        M("UMLNode",     "nd_s0_pdb",  M0, "PostgreSQL (Base de Datos)"),
        M("UMLArtifact", "art_s0_apk", M0, "App Flutter (APK)"),
        M("UMLDependency", "dep_s0_an", M0, "HTTPS / REST",
          client=ref("nd_s0_and"), supplier=ref("nd_s0_ngx")),
        M("UMLDependency", "dep_s0_na", M0, "/api/*",
          client=ref("nd_s0_ngx"), supplier=ref("nd_s0_api")),
        M("UMLDependency", "dep_s0_nw", M0, "/*",
          client=ref("nd_s0_ngx"), supplier=ref("nd_s0_app")),
        M("UMLDependency", "dep_s0_ad", M0, "TCP 5432",
          client=ref("nd_s0_api"), supplier=ref("nd_s0_pdb")),
    ]
    dep_views: list[dict] = [
        node_v("vn_s0_and",  D, "nd_s0_and",  30,  50, 190, 80),
        artifact_v("vart_s0_apk", D, "art_s0_apk",  45,  90, 160, 38),
        node_v("vn_s0_ngx",  D, "nd_s0_ngx",  280,  40, 200, 70),
        node_v("vn_s0_api",  D, "nd_s0_api",  280, 150, 200, 70),
        node_v("vn_s0_app",  D, "nd_s0_app",  530,  40, 220, 70),
        node_v("vn_s0_pdb",  D, "nd_s0_pdb",  530, 150, 220, 70),
        edge_v("UMLDependencyView", "ve_s0_an", D, "dep_s0_an", "vn_s0_and", "vn_s0_ngx"),
        edge_v("UMLDependencyView", "ve_s0_na", D, "dep_s0_na", "vn_s0_ngx", "vn_s0_api"),
        edge_v("UMLDependencyView", "ve_s0_nw", D, "dep_s0_nw", "vn_s0_ngx", "vn_s0_app"),
        edge_v("UMLDependencyView", "ve_s0_ad", D, "dep_s0_ad", "vn_s0_api", "vn_s0_pdb"),
    ]
    dep_diag = diag("UMLDeploymentDiagram", D, M0, "Despliegue_Sprint0", dep_views)

    # S0.4 Clases conceptuales
    D = "diag_s0_cls"
    C = [40, 235, 430, 625]   # 4 columnas
    cls_elems: list[dict] = [
        M_class("cls_s0_usr", M0, "Usuario",
                [("nombre",""), ("apellido",""), ("correo",""),
                 ("contrasena",""), ("rol",""), ("activo","")]),
        M_class("cls_s0_org", M0, "Organizacion",
                [("nombre",""), ("direccion",""), ("contacto",""), ("activo","")]),
        M_class("cls_s0_pry", M0, "Proyecto",
                [("nombre",""), ("descripcion",""), ("estado",""),
                 ("fechaInicio",""), ("fechaFin","")]),
        M_class("cls_s0_ins", M0, "Instalacion",
                [("nombre",""), ("descripcion","")]),
        M_class("cls_s0_pla", M0, "PlanoDePlanta",
                [("archivo",""), ("escala",""), ("anchoMetros",""), ("altoMetros","")]),
        M_class("cls_s0_med", M0, "Medicion",
                [("rssi_dBm",""), ("ssid",""), ("bssid",""),
                 ("frecuencia_GHz",""), ("canal",""),
                 ("coordenadaX",""), ("coordenadaY",""), ("fechaHora","")]),
        M_class("cls_s0_mpa", M0, "MapaDeCalor",
                [("imagenGenerada",""), ("algoritmo",""), ("fechaGeneracion","")]),
        M_class("cls_s0_rpt", M0, "ReporteIA",
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
        class_v("vc_s0_usr", D, "cls_s0_usr", C[0],  40, 175, 150),
        class_v("vc_s0_org", D, "cls_s0_org", C[1],  40, 175, 120),
        class_v("vc_s0_pry", D, "cls_s0_pry", C[2],  40, 175, 130),
        class_v("vc_s0_ins", D, "cls_s0_ins", C[3],  40, 175,  80),
        class_v("vc_s0_pla", D, "cls_s0_pla", C[3], 200, 175, 110),
        class_v("vc_s0_med", D, "cls_s0_med", C[2], 230, 175, 195),
        class_v("vc_s0_mpa", D, "cls_s0_mpa", C[1], 210, 175, 100),
        class_v("vc_s0_rpt", D, "cls_s0_rpt", C[0], 210, 175, 100),
        edge_v("UMLAssociationView", "ve_s0_up", D, "ac_s0_up", "vc_s0_usr", "vc_s0_pry"),
        edge_v("UMLAssociationView", "ve_s0_op", D, "ac_s0_op", "vc_s0_org", "vc_s0_pry"),
        edge_v("UMLAssociationView", "ve_s0_pi", D, "ac_s0_pi", "vc_s0_pry", "vc_s0_ins"),
        edge_v("UMLAssociationView", "ve_s0_ip", D, "ac_s0_ip", "vc_s0_ins", "vc_s0_pla"),
        edge_v("UMLAssociationView", "ve_s0_pm", D, "ac_s0_pm", "vc_s0_pry", "vc_s0_med"),
        edge_v("UMLAssociationView", "ve_s0_mm", D, "ac_s0_mm", "vc_s0_med", "vc_s0_mpa"),
        edge_v("UMLAssociationView", "ve_s0_mr", D, "ac_s0_mr", "vc_s0_mpa", "vc_s0_rpt"),
    ]
    cls_diag = diag("UMLClassDiagram", D, M0, "Modelo_Datos_Conceptual_Sprint0", cls_views)

    all_elems = ctx_elems + pkg_elems + dep_elems + cls_elems + [ctx_diag, pkg_diag, dep_diag, cls_diag]
    return [{"_type": "UMLModel", "_id": sid(M0), "_parent": ref(proj_k),
             "name": "Sprint 0 — Modelos Iniciales", "visibility": "public",
             "ownedElements": all_elems}]


# ═══════════════════════════════════════════════════════════════════════════
# SPRINT 1
# ═══════════════════════════════════════════════════════════════════════════
def build_sprint1(proj_k: str) -> list[dict]:
    M1 = "m_s1"

    # S1.1 Contexto
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
        actor_v("va_s1_adm", D, "a_s1_adm",  30, 150),
        actor_v("va_s1_tec", D, "a_s1_tec",  30, 380),
        uc_v("vuc_s1_10", D, "uc_s1_10", 200,  30, 220, 44),
        uc_v("vuc_s1_01", D, "uc_s1_01", 200,  95, 190, 44),
        uc_v("vuc_s1_09", D, "uc_s1_09", 200, 160, 190, 44),
        uc_v("vuc_s1_13", D, "uc_s1_13", 200, 225, 200, 44),
        uc_v("vuc_s1_18", D, "uc_s1_18", 200, 290, 210, 44),
        uc_v("vuc_s1_19", D, "uc_s1_19", 200, 370, 220, 44),
        edge_v("UMLAssociationView", "ve_s1_a10", D, "as_s1_a10", "va_s1_adm", "vuc_s1_10"),
        edge_v("UMLAssociationView", "ve_s1_a01", D, "as_s1_a01", "va_s1_adm", "vuc_s1_01"),
        edge_v("UMLAssociationView", "ve_s1_a09", D, "as_s1_a09", "va_s1_adm", "vuc_s1_09"),
        edge_v("UMLAssociationView", "ve_s1_a13", D, "as_s1_a13", "va_s1_adm", "vuc_s1_13"),
        edge_v("UMLAssociationView", "ve_s1_a18", D, "as_s1_a18", "va_s1_adm", "vuc_s1_18"),
        edge_v("UMLAssociationView", "ve_s1_t19", D, "as_s1_t19", "va_s1_tec", "vuc_s1_19"),
    ]
    ctx_diag = diag("UMLUseCaseDiagram", D, M1, "Contexto_Sprint1", ctx_views)

    # S1.2 Paquetes
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
        pkg_v("vp_s1_mob", D, "pkg_s1_mob",  40,  40, 210, 120),
        pkg_v("vp_s1_bk",  D, "pkg_s1_bk",  310,  40, 210, 120),
        pkg_v("vp_s1_web", D, "pkg_s1_web",  580,  40, 220, 120),
        pkg_v("vp_s1_db",  D, "pkg_s1_db",  310, 220, 210,  90),
        edge_v("UMLDependencyView", "ve_s1_mb", D, "dep_s1_mb", "vp_s1_mob", "vp_s1_bk"),
        edge_v("UMLDependencyView", "ve_s1_wb", D, "dep_s1_wb", "vp_s1_web", "vp_s1_bk"),
        edge_v("UMLDependencyView", "ve_s1_bd", D, "dep_s1_bd", "vp_s1_bk",  "vp_s1_db"),
    ]
    pkg_diag = diag("UMLPackageDiagram", D, M1, "Paquetes_Sprint1", pkg_views)

    # S1.3 Despliegue
    D = "diag_s1_dep"
    dep_elems: list[dict] = [
        M("UMLNode", "nd_s1_and",  M1, "Dispositivo Android"),
        M("UMLNode", "nd_s1_brw",  M1, "PC / Navegador Web"),
        M("UMLNode", "nd_s1_ngx",  M1, "nginx:alpine"),
        M("UMLNode", "nd_s1_api",  M1, "backend:python"),
        M("UMLNode", "nd_s1_pdb",  M1, "db:postgres15"),
        M("UMLArtifact", "art_s1_apk",   M1, "App Flutter"),
        M("UMLArtifact", "art_s1_react", M1, "Panel Admin React"),
        M("UMLDependency", "dep_s1_an", M1, "HTTPS :443",
          client=ref("nd_s1_and"), supplier=ref("nd_s1_ngx")),
        M("UMLDependency", "dep_s1_bn", M1, "HTTPS :443",
          client=ref("nd_s1_brw"), supplier=ref("nd_s1_ngx")),
        M("UMLDependency", "dep_s1_na", M1, ":8000 /api/v1",
          client=ref("nd_s1_ngx"), supplier=ref("nd_s1_api")),
        M("UMLDependency", "dep_s1_ad", M1, ":5432",
          client=ref("nd_s1_api"), supplier=ref("nd_s1_pdb")),
    ]
    dep_views: list[dict] = [
        node_v("vn_s1_and",  D, "nd_s1_and",  30,  50, 180, 80),
        artifact_v("vart_s1_apk", D, "art_s1_apk", 45,  90, 150, 38),
        node_v("vn_s1_brw",  D, "nd_s1_brw",  30, 200, 180, 80),
        artifact_v("vart_s1_rct", D, "art_s1_react", 45, 240, 150, 38),
        node_v("vn_s1_ngx",  D, "nd_s1_ngx",  270,  60, 200, 70),
        node_v("vn_s1_api",  D, "nd_s1_api",  270, 160, 200, 70),
        node_v("vn_s1_pdb",  D, "nd_s1_pdb",  270, 260, 200, 70),
        edge_v("UMLDependencyView", "ve_s1_an", D, "dep_s1_an", "vn_s1_and", "vn_s1_ngx"),
        edge_v("UMLDependencyView", "ve_s1_bn", D, "dep_s1_bn", "vn_s1_brw", "vn_s1_ngx"),
        edge_v("UMLDependencyView", "ve_s1_na", D, "dep_s1_na", "vn_s1_ngx", "vn_s1_api"),
        edge_v("UMLDependencyView", "ve_s1_ad", D, "dep_s1_ad", "vn_s1_api", "vn_s1_pdb"),
    ]
    dep_diag = diag("UMLDeploymentDiagram", D, M1, "Despliegue_Sprint1", dep_views)

    # S1.4 Clases
    D = "diag_s1_cls"
    cls_elems: list[dict] = [
        M_class("cls_s1_usr", M1, "Usuario",
                [("nombre","string"), ("apellido","string"), ("correo","string"),
                 ("contrasena_hash","string"), ("rol","enum"), ("activo","bool"),
                 ("fecha_creacion","datetime")]),
        M_class("cls_s1_org", M1, "Organizacion",
                [("nombre","string"), ("direccion","string"),
                 ("contacto","string"), ("activo","bool"), ("fecha_creacion","datetime")]),
        M_class("cls_s1_pry", M1, "Proyecto",
                [("nombre","string"), ("descripcion","string"),
                 ("estado","enum"), ("fecha_inicio","date"),
                 ("fecha_fin","date"), ("fecha_creacion","datetime")]),
        M_assoc("ac_s1_up", M1, "cls_s1_usr", "cls_s1_pry", "gestiona", "1", "0..*"),
        M_assoc("ac_s1_op", M1, "cls_s1_org", "cls_s1_pry", "tiene",    "1", "0..*"),
    ]
    cls_views: list[dict] = [
        class_v("vc_s1_usr", D, "cls_s1_usr",  40,  40, 185, 175),
        class_v("vc_s1_org", D, "cls_s1_org",  295,  40, 185, 145),
        class_v("vc_s1_pry", D, "cls_s1_pry",  550,  40, 185, 160),
        edge_v("UMLAssociationView", "ve_s1_up", D, "ac_s1_up", "vc_s1_usr", "vc_s1_pry"),
        edge_v("UMLAssociationView", "ve_s1_op", D, "ac_s1_op", "vc_s1_org", "vc_s1_pry"),
    ]
    cls_diag = diag("UMLClassDiagram", D, M1, "Datos_Conceptual_Sprint1", cls_views)

    all_m1 = ctx_elems + pkg_elems + dep_elems + cls_elems + [ctx_diag, pkg_diag, dep_diag, cls_diag]
    model_s1 = {"_type": "UMLModel", "_id": sid(M1), "_parent": ref(proj_k),
                "name": "Sprint 1 — Fundación CRUD", "visibility": "public",
                "ownedElements": all_m1}

    # S1.5 Secuencia Autenticación
    COL1 = "col_s1_auth"; INT1 = "int_s1_auth"; D = "diag_s1_seq"
    ll_keys  = ["ll_s1_usr", "ll_s1_fe", "ll_s1_api", "ll_s1_svc", "ll_s1_db"]
    ll_names = ["Usuario", "Frontend (Web/App)", "FastAPI /auth/login",
                "AuthService", "PostgreSQL usuarios"]
    ll_models = [M("UMLLifeline", k, INT1, n) for k, n in zip(ll_keys, ll_names)]
    msg_data = [
        ("msg_s1_01", "ll_s1_usr", "ll_s1_fe",  "Ingresa correo + contraseña"),
        ("msg_s1_02", "ll_s1_fe",  "ll_s1_api", "POST /api/v1/auth/login"),
        ("msg_s1_03", "ll_s1_api", "ll_s1_svc", "autenticar(email, password)"),
        ("msg_s1_04", "ll_s1_svc", "ll_s1_db",  "SELECT usuario WHERE correo"),
        ("msg_s1_05", "ll_s1_db",  "ll_s1_svc", "registro del usuario",    "reply"),
        ("msg_s1_06", "ll_s1_svc", "ll_s1_svc", "verificar bcrypt(pw, hash)"),
        ("msg_s1_07", "ll_s1_svc", "ll_s1_api", "usuario autenticado",     "reply"),
        ("msg_s1_08", "ll_s1_api", "ll_s1_fe",  "200 OK {access_token}",   "reply"),
        ("msg_s1_09", "ll_s1_fe",  "ll_s1_usr", "Redirige al dashboard",   "reply"),
    ]
    msg_models = [M("UMLMessage", d[0], INT1, d[3],
                    messageSort=d[4] if len(d) > 4 else "synchCall",
                    source=ref(d[1]), target=ref(d[2])) for d in msg_data]
    LL_W = 130; LL_GAP = 165; N = len(msg_data)
    LL_X  = [40 + i * LL_GAP for i in range(5)]
    LL_CX = [x + LL_W // 2 for x in LL_X]
    LL_IDX = {k: i for i, k in enumerate(ll_keys)}
    LL_H = 120 + N * 60 + 80
    ll_views = [lifeline_v(f"vll_s1_{i}", D, ll_keys[i], LL_X[i], 32, LL_W, LL_H) for i in range(5)]
    msg_views = []
    for j, d in enumerate(msg_data):
        y = 120 + j * 60; s = LL_IDX[d[1]]; t = LL_IDX[d[2]]
        msg_views.append(seq_msg_v(f"vmsg_s1_{j:02d}", D, d[0],
                                   f"vll_s1_{s}", f"vll_s1_{t}",
                                   LL_CX[s], y, LL_CX[t], y))
    seq_diag = diag("UMLSequenceDiagram", D, INT1, "Secuencia_Autenticacion_Sprint1", ll_views + msg_views)
    collab_s1 = {
        "_type": "UMLCollaboration", "_id": sid(COL1), "_parent": ref(proj_k),
        "name": "Secuencia_Autenticacion_Sprint1",
        "ownedElements": [{"_type": "UMLInteraction", "_id": sid(INT1), "_parent": ref(COL1),
                           "name": "Secuencia_Autenticacion_Sprint1",
                           "ownedElements": ll_models + msg_models + [seq_diag]}],
    }
    return [model_s1, collab_s1]


# ═══════════════════════════════════════════════════════════════════════════
# SPRINT 2
# ═══════════════════════════════════════════════════════════════════════════
def build_sprint2(proj_k: str) -> list[dict]:
    M2 = "m_s2"

    # S2.1 Casos de Uso
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
        actor_v("va_s2_tec", D, "a_s2_tec",  30, 200),
        uc_v("vuc_s2_02", D, "uc_s2_02", 210,  60, 185, 44),
        uc_v("vuc_s2_11", D, "uc_s2_11", 210, 165, 185, 44),
        uc_v("vuc_s2_01", D, "uc_s2_01", 210, 320, 200, 44),
        edge_v("UMLAssociationView", "ve_s2_t2",  D, "as_s2_t2",  "va_s2_tec", "vuc_s2_02"),
        edge_v("UMLAssociationView", "ve_s2_t11", D, "as_s2_t11", "va_s2_tec", "vuc_s2_11"),
        edge_v("UMLAssociationView", "ve_s2_t1",  D, "as_s2_t1",  "va_s2_tec", "vuc_s2_01"),
        edge_v("UMLDependencyView",  "ve_s2_d11", D, "dep_s2_112", "vuc_s2_11", "vuc_s2_02"),
    ]
    ctx_diag = diag("UMLUseCaseDiagram", D, M2, "Sprint2_CasosUso", ctx_views)

    # S2.2 Clases
    D = "diag_s2_cls"
    cls_elems: list[dict] = [
        M_class("cls_s2_pry", M2, "Proyecto",
                [("id","entero"), ("nombre","texto"), ("cliente","texto"), ("estado","texto")]),
        M_class("cls_s2_pla", M2, "Plano",
                [("id","entero"), ("nombre_archivo","texto"), ("formato","texto"),
                 ("ancho_px","entero"), ("alto_px","entero"), ("escala_m_por_px","decimal")]),
        M_assoc("ac_s2_pp", M2, "cls_s2_pry", "cls_s2_pla", "contiene", "1", "0..*"),
    ]
    cls_views: list[dict] = [
        class_v("vc_s2_pry", D, "cls_s2_pry",  80,  60, 180, 110),
        class_v("vc_s2_pla", D, "cls_s2_pla", 360,  60, 195, 155),
        edge_v("UMLAssociationView", "ve_s2_pp", D, "ac_s2_pp", "vc_s2_pry", "vc_s2_pla"),
    ]
    cls_diag = diag("UMLClassDiagram", D, M2, "Sprint2_Clases", cls_views)

    all_m2 = ctx_elems + cls_elems + [ctx_diag, cls_diag]
    model_s2 = {"_type": "UMLModel", "_id": sid(M2), "_parent": ref(proj_k),
                "name": "Sprint 2 — Planos y Calibración", "visibility": "public",
                "ownedElements": all_m2}

    def _seq(col_k, int_k, d_k, name, ll_ks, ll_ns, msgs, ll_w=120, ll_gap=155):
        ll_models = [M("UMLLifeline", k, int_k, n) for k, n in zip(ll_ks, ll_ns)]
        msg_models = [M("UMLMessage", d[0], int_k, d[3],
                        messageSort=d[4] if len(d) > 4 else "synchCall",
                        source=ref(d[1]), target=ref(d[2])) for d in msgs]
        n_ll = len(ll_ks)
        LL_X  = [30 + i * ll_gap for i in range(n_ll)]
        LL_CX = [x + ll_w // 2 for x in LL_X]
        LL_IDX = {k: i for i, k in enumerate(ll_ks)}
        LL_H = 120 + len(msgs) * 60 + 80
        tag = col_k.replace("col_", "")
        ll_views = [lifeline_v(f"vll_{tag}_{i}", d_k, ll_ks[i], LL_X[i], 32, ll_w, LL_H)
                    for i in range(n_ll)]
        msg_views = []
        for j, d in enumerate(msgs):
            y = 120 + j * 60; s = LL_IDX[d[1]]; t = LL_IDX[d[2]]
            msg_views.append(seq_msg_v(f"vmsg_{tag}_{j:02d}", d_k, d[0],
                                       f"vll_{tag}_{s}", f"vll_{tag}_{t}",
                                       LL_CX[s], y, LL_CX[t], y))
        sd = diag("UMLSequenceDiagram", d_k, int_k, name, ll_views + msg_views)
        return {"_type": "UMLCollaboration", "_id": sid(col_k), "_parent": ref(proj_k),
                "name": name,
                "ownedElements": [{"_type": "UMLInteraction", "_id": sid(int_k),
                                   "_parent": ref(col_k), "name": name,
                                   "ownedElements": ll_models + msg_models + [sd]}]}

    # S2.3 Seq Subida
    c2a = _seq("col_s2_sub", "int_s2_sub", "diag_s2_seq_sub", "Sprint2_Secuencia_Subida",
               ["ll_s2_tec", "ll_s2_app", "ll_s2_api", "ll_s2_bk", "ll_s2_stor", "ll_s2_db"],
               ["Tecnico", "PlanoEditorPage", "ApiClient", "Backend /planos",
                "StorageService", "PostgreSQL"],
               [("msg_s2a_01","ll_s2_tec","ll_s2_app","seleccionar archivo"),
                ("msg_s2a_02","ll_s2_app","ll_s2_api","POST multipart/form-data"),
                ("msg_s2a_03","ll_s2_api","ll_s2_bk","solicitud autenticada"),
                ("msg_s2a_04","ll_s2_bk","ll_s2_stor","guardar archivo"),
                ("msg_s2a_05","ll_s2_bk","ll_s2_db","insertar metadatos del plano"),
                ("msg_s2a_06","ll_s2_db","ll_s2_bk","id y dimensiones","reply"),
                ("msg_s2a_07","ll_s2_bk","ll_s2_app","201 + URL firmada","reply"),
                ("msg_s2a_08","ll_s2_app","ll_s2_tec","renderizar plano","reply")])

    # S2.4 Seq Calibración
    c2b = _seq("col_s2_cal", "int_s2_cal", "diag_s2_seq_cal", "Sprint2_Secuencia_Calibracion",
               ["ll_s2b_tec", "ll_s2b_app", "ll_s2b_cub", "ll_s2b_bk", "ll_s2b_db"],
               ["Tecnico", "PlanoEditorPage", "PlanosCubit", "Backend /calibracion", "PostgreSQL"],
               [("msg_s2b_01","ll_s2b_tec","ll_s2b_app","tocar dos puntos"),
                ("msg_s2b_02","ll_s2b_app","ll_s2b_tec","solicitar distancia real","reply"),
                ("msg_s2b_03","ll_s2b_tec","ll_s2b_app","ingresar metros"),
                ("msg_s2b_04","ll_s2b_app","ll_s2b_cub","confirmar calibración"),
                ("msg_s2b_05","ll_s2b_cub","ll_s2b_bk","PATCH calibracion"),
                ("msg_s2b_06","ll_s2b_bk","ll_s2b_db","actualizar escala y puntos"),
                ("msg_s2b_07","ll_s2b_db","ll_s2b_bk","calibración persistida","reply"),
                ("msg_s2b_08","ll_s2b_bk","ll_s2b_cub","plano calibrado","reply"),
                ("msg_s2b_09","ll_s2b_cub","ll_s2b_app","estado exitoso","reply"),
                ("msg_s2b_10","ll_s2b_app","ll_s2b_tec","mostrar factor y regla","reply")],
               ll_gap=165)

    return [model_s2, c2a, c2b]


# ═══════════════════════════════════════════════════════════════════════════
# SPRINT 3
# ═══════════════════════════════════════════════════════════════════════════
def build_sprint3(proj_k: str) -> list[dict]:
    M3 = "m_s3"

    # S3.1 Casos de Uso
    D = "diag_s3_ctx"
    ctx_elems: list[dict] = [
        M("UMLActor",   "a_s3_tec", M3, "Técnico"),
        M("UMLUseCase", "uc_s3_03", M3, "PB-03 Capturar señales WiFi"),
        M("UMLUseCase", "uc_s3_04", M3, "PB-04 Marcar puntos de medición"),
        M("UMLUseCase", "uc_s3_11", M3, "PB-11 Plano calibrado"),
        M_assoc("as_s3_t3", M3, "a_s3_tec", "uc_s3_03"),
        M_assoc("as_s3_t4", M3, "a_s3_tec", "uc_s3_04"),
        M("UMLDependency", "dep_s3_311", M3, "<<requires>>",
          client=ref("uc_s3_03"), supplier=ref("uc_s3_11")),
        M("UMLInclude", "inc_s3_43", M3, "",
          client=ref("uc_s3_04"), supplier=ref("uc_s3_03")),
    ]
    ctx_views: list[dict] = [
        actor_v("va_s3_tec", D, "a_s3_tec",  30, 200),
        uc_v("vuc_s3_03", D, "uc_s3_03", 210,  60, 215, 44),
        uc_v("vuc_s3_04", D, "uc_s3_04", 210, 165, 235, 44),
        uc_v("vuc_s3_11", D, "uc_s3_11", 210, 320, 195, 44),
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

    # S3.2 Seq Captura
    COL3 = "col_s3_cap"; INT3 = "int_s3_cap"; D3 = "diag_s3_seq"
    ll3_keys  = ["ll_s3_tec", "ll_s3_app", "ll_s3_scan", "ll_s3_cub", "ll_s3_bk", "ll_s3_db"]
    ll3_names = ["Tecnico", "CapturaPage", "WifiScanner",
                 "CapturaCubit", "Backend /mediciones", "PostgreSQL"]
    ll3_models = [M("UMLLifeline", k, INT3, n) for k, n in zip(ll3_keys, ll3_names)]
    msg3_data = [
        ("msg_s3_01","ll_s3_tec","ll_s3_app","tocar punto en plano"),
        ("msg_s3_02","ll_s3_app","ll_s3_scan","iniciar escaneo"),
        ("msg_s3_03","ll_s3_scan","ll_s3_app","resultados WiFi","reply"),
        ("msg_s3_04","ll_s3_app","ll_s3_cub","enviar lote"),
        ("msg_s3_05","ll_s3_cub","ll_s3_bk","POST /api/mediciones"),
        ("msg_s3_06","ll_s3_bk","ll_s3_db","insertar punto y mediciones"),
        ("msg_s3_07","ll_s3_db","ll_s3_bk","ids y nivel","reply"),
        ("msg_s3_08","ll_s3_bk","ll_s3_cub","201 Created","reply"),
        ("msg_s3_09","ll_s3_cub","ll_s3_app","actualizar plano","reply"),
        ("msg_s3_10","ll_s3_app","ll_s3_tec","mostrar badge por nivel","reply"),
    ]
    msg3_models = [M("UMLMessage", d[0], INT3, d[3],
                     messageSort=d[4] if len(d) > 4 else "synchCall",
                     source=ref(d[1]), target=ref(d[2])) for d in msg3_data]
    LL3_W = 120; LL3_GAP = 155; N3 = len(msg3_data)
    LL3_X  = [30 + i * LL3_GAP for i in range(6)]
    LL3_CX = [x + LL3_W // 2 for x in LL3_X]
    LL3_IDX = {k: i for i, k in enumerate(ll3_keys)}
    LL3_H = 120 + N3 * 60 + 80
    ll3_views = [lifeline_v(f"vll_s3_{i}", D3, ll3_keys[i], LL3_X[i], 32, LL3_W, LL3_H) for i in range(6)]
    msg3_views = []
    for j, d in enumerate(msg3_data):
        y = 120 + j * 60; s = LL3_IDX[d[1]]; t = LL3_IDX[d[2]]
        msg3_views.append(seq_msg_v(f"vmsg_s3_{j:02d}", D3, d[0],
                                    f"vll_s3_{s}", f"vll_s3_{t}",
                                    LL3_CX[s], y, LL3_CX[t], y))
    seq3_diag = diag("UMLSequenceDiagram", D3, INT3, "Sprint3_Secuencia_Captura", ll3_views + msg3_views)
    collab_s3 = {
        "_type": "UMLCollaboration", "_id": sid(COL3), "_parent": ref(proj_k),
        "name": "Sprint3_Secuencia_Captura",
        "ownedElements": [{"_type": "UMLInteraction", "_id": sid(INT3), "_parent": ref(COL3),
                           "name": "Sprint3_Secuencia_Captura",
                           "ownedElements": ll3_models + msg3_models + [seq3_diag]}],
    }

    # S3.3 Estados CapturaCubit
    SM = "sm_s3_estados"; D_st = "diag_s3_st"
    ST = ["st_s3_ini","st_s3_inac","st_s3_load","st_s3_act",
          "st_s3_env","st_s3_thro","st_s3_pau","st_s3_det","st_s3_err","st_s3_fin"]
    SN = [None,"Inactiva","Loading","Activa",
          "Enviando","Throttling","Pausada","PuntoDetalle","Error",None]
    state_models: list[dict] = [M("UMLPseudostate","st_s3_ini",SM,"",kind="initial")]
    for k, n in zip(ST[1:-1], SN[1:-1]):
        state_models.append(M("UMLState", k, SM, n))
    state_models.append(M("UMLFinalState","st_s3_fin",SM,""))
    trans_data = [
        ("tr_s3_01","st_s3_ini","st_s3_inac",""),
        ("tr_s3_02","st_s3_inac","st_s3_load","iniciarSesion"),
        ("tr_s3_03","st_s3_load","st_s3_act","puntos cargados"),
        ("tr_s3_04","st_s3_act","st_s3_env","marcarPunto"),
        ("tr_s3_05","st_s3_env","st_s3_act","lote persistido"),
        ("tr_s3_06","st_s3_act","st_s3_thro","limite alcanzado"),
        ("tr_s3_07","st_s3_thro","st_s3_act","tiempo liberado"),
        ("tr_s3_08","st_s3_act","st_s3_pau","sin conectividad"),
        ("tr_s3_09","st_s3_pau","st_s3_act","reanudar"),
        ("tr_s3_10","st_s3_act","st_s3_det","abrirDetallePunto"),
        ("tr_s3_11","st_s3_det","st_s3_act","cerrarDetalle"),
        ("tr_s3_12","st_s3_env","st_s3_err","fallo de envio"),
        ("tr_s3_13","st_s3_err","st_s3_act","reintentar"),
        ("tr_s3_14","st_s3_act","st_s3_inac","detenerSesion"),
    ]
    trans_models = [M("UMLTransition",d[0],SM,d[3],source=ref(d[1]),target=ref(d[2])) for d in trans_data]
    POS = {
        "st_s3_ini":(190,20), "st_s3_inac":(120,80), "st_s3_load":(120,160),
        "st_s3_act":(120,250), "st_s3_env":(350,165), "st_s3_thro":(350,250),
        "st_s3_pau":(575,165), "st_s3_det":(575,250), "st_s3_err":(350,350),
        "st_s3_fin":(120,450),
    }
    state_views: list[dict] = [pseudo_v("vst_s3_ini", D_st, "st_s3_ini", *POS["st_s3_ini"])]
    for k, n in zip(ST[1:-1], SN[1:-1]):
        state_views.append(state_v(f"vst_{k}", D_st, k, *POS[k], 140, 44))
    state_views.append(final_v("vst_s3_fin", D_st, "st_s3_fin", *POS["st_s3_fin"]))
    VK = {k: ("vst_s3_ini" if k == "st_s3_ini" else
              "vst_s3_fin" if k == "st_s3_fin" else f"vst_{k}") for k in ST}
    trans_views = [trans_v(f"vtr_{d[0]}", D_st, d[0], VK[d[1]], VK[d[2]]) for d in trans_data]
    st_diag = diag("UMLStatechartDiagram", D_st, SM, "Sprint3_Estados", state_views + trans_views)
    statemachine = {
        "_type": "UMLStateMachine", "_id": sid(SM), "_parent": ref(proj_k),
        "name": "Sprint3_Estados",
        "ownedElements": state_models + trans_models + [st_diag],
    }
    return [model_s3, collab_s3, statemachine]


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
def build_project() -> dict:
    PROJ = "proj_paneles_whm"
    owned: list[dict] = []
    owned.extend(build_sprint0(PROJ))
    owned.extend(build_sprint1(PROJ))
    owned.extend(build_sprint2(PROJ))
    owned.extend(build_sprint3(PROJ))
    return {"_type": "Project", "_id": sid(PROJ),
            "name": "Paneles-WHM", "ownedElements": owned}

def main() -> None:
    if OUTPUT.exists():
        print(f"[AVISO] El archivo ya existe: {OUTPUT}")
        resp = input("  ¿Sobreescribir? (s/N): ").strip().lower()
        if resp != "s":
            print("Cancelado."); return
    project = build_project()
    OUTPUT.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"[OK] {OUTPUT}  ({size_kb:.1f} KB)")
    raw = json.dumps(project)
    for t in sorted({"UMLUseCaseDiagram","UMLClassDiagram","UMLPackageDiagram",
                     "UMLDeploymentDiagram","UMLSequenceDiagram","UMLStatechartDiagram"}):
        n = raw.count(f'"_type": "{t}"')
        if n: print(f"  {t}: {n}")

if __name__ == "__main__":
    main()
