---
name: gestionar-diagramas-staruml
description: "Crea, edita y mantiene el archivo maestro StarUML del proyecto Wireless HeatMapper garantizando uniformidad visual, nomenclatura estable, paleta de colores institucional y conformidad obligatoria con UML 2.5 o superior en todos los diagramas."
argument-hint: "Acción a realizar: crear-diagrama, editar-diagrama, generar-paneles, validar-archivo, agregar-modelo-sprint (ej. agregar-modelo-sprint Sprint2_Clases)"
user-invocable: true
disable-model-invocation: false
---

# Skill: Gestionar Diagramas StarUML

## Propósito

Crear y mantener el archivo maestro `diagrams/Modelos - Wireless Headmapper.mdj` de StarUML con todos los diagramas del proyecto Wireless HeatMapper. Todos los diagramas deben ser uniformes en paleta de colores, nomenclatura, layout y —sin excepción— conformes con **UML 2.5 o superior**.

El script de generación vive en `diagrams/generar_paneles.py` y debe ejecutarse cada vez que se actualice el modelo.

---

## 1. Regla fundamental: UML 2.5+

> **OBLIGATORIO E INNEGOCIABLE:** Todo diagrama generado o editado en el archivo StarUML debe emplear exclusivamente la notación y semántica de **UML 2.5 o superior** (OMG UML Specification 2.5.1, 2017).

Esto implica:

- **Diagramas de clases:** Usar multiplicidades en formato `0..1`, `1`, `*`, `1..*`. Nunca `0,1` ni `n`. Las interfaces se modelan con `<<interface>>` o usando la notación de bola (lollipop). Las clases abstractas con nombre en cursiva o marcador `{abstract}`.
- **Diagramas de casos de uso:** Los actores son `UMLActor`. Las relaciones `<<include>>` y `<<extend>>` son `UMLInclude` y `UMLExtend` respectivamente — nunca flechas genéricas etiquetadas.
- **Diagramas de secuencia:** Usar `UMLLifeline` (no "objeto de secuencia" de UML 1.x). Los mensajes síncronos son `UMLMessage` con `messageSort = "synchCall"`, asincrónicos con `"asynchCall"`, respuestas con `"reply"`. Los fragmentos combinados (`alt`, `opt`, `loop`) son `UMLCombinedFragment`.
- **Diagramas de estado:** Usar `UMLStatechart` (no `UMLActivityDiagram`). Los estados compuestos usan `UMLState` con subestados en `ownedElements`. Las transiciones con guardia se anotan con `[condición]`.
- **Diagramas de paquetes:** Los estereotipos de componentes siguen UML 2.5 (`<<component>>`, `<<subsystem>>`).
- **Diagramas de despliegue:** Los nodos usan `UMLNode`; los artefactos `UMLArtifact`; las instancias desplegadas `UMLComponentInstance` o similar de UML 2.5.

Verificar contra la especificación: [https://www.omg.org/spec/UML/2.5.1/PDF](https://www.omg.org/spec/UML/2.5.1/PDF)

---

## 2. Archivo maestro StarUML

### 2.1 Ubicación y formato

| Propiedad       | Valor                                                       |
| --------------- | ----------------------------------------------------------- |
| Ruta            | `diagrams/Modelos - Wireless Headmapper.mdj`                |
| Formato         | JSON puro (no minificado), codificación UTF-8               |
| Extensión       | `.mdj` — proyecto completo con nodo raíz `_type: "Project"` |
| Versión StarUML | 6.x                                                         |

### 2.2 Estructura jerárquica obligatoria

```
Project  (_id: "__project__")
├── UMLModel  "Modelo de Contexto"           ← Sprint 0 — casos de uso generales
├── UMLModel  "Arquitectura Sprint 0"         ← Sprint 0 — paquetes + despliegue + clases
├── UMLModel  "Sprint 1 — Autenticación"      ← Sprint 1 — UC + clases + secuencia
├── UMLModel  "Sprint 2 — Gestión Proyectos"  ← Sprint 2 — UC + clases + 2 secuencias
└── UMLModel  "Sprint 3 — Captura WiFi"       ← Sprint 3 — UC + secuencia + estados
```

Cada `UMLModel` contiene sus propios diagramas en `ownedElements`. No mezclar diagramas de sprints distintos dentro de un mismo `UMLModel`.

### 2.3 Identificadores estables (\_id)

Los IDs se generan con `uuid.uuid4().hex` (32 caracteres hexadecimales, sin guiones). La función `_sid(clave)` del script los hace deterministas:

```python
import hashlib
def _sid(clave: str) -> str:
    return hashlib.md5(clave.encode()).hexdigest()
```

**Nunca** usar IDs aleatorios en tiempo de ejecución para elementos cuyo nombre semántico es conocido. Esto garantiza que al regenerar el `.mdj` los IDs no cambien y StarUML no pierda referencias.

Convención de claves semánticas:

| Tipo de elemento     | Patrón de clave                       | Ejemplo                         |
| -------------------- | ------------------------------------- | ------------------------------- |
| Modelo de sprint     | `model_<sprint>`                      | `model_sprint1`                 |
| Diagrama             | `diag_<nombre_constante>`             | `diag_contexto_sprint0`         |
| Actor                | `actor_<codigo>`                      | `actor_A1`                      |
| Caso de uso          | `uc_<codigo>`                         | `uc_UC01`                       |
| Clase                | `class_<nombre_snake>`                | `class_usuario`                 |
| Atributo             | `attr_<clase>_<atributo>`             | `attr_usuario_email`            |
| Operación            | `op_<clase>_<operacion>`              | `op_usuario_login`              |
| Asociación           | `assoc_<origen>_<destino>`            | `assoc_proyecto_instalacion`    |
| Lifeline (secuencia) | `ll_<diagrama>_<participante>`        | `ll_seq_auth_tecnico`           |
| Mensaje (secuencia)  | `msg_<diagrama>_<n>`                  | `msg_seq_auth_1`                |
| Estado               | `state_<diagrama>_<nombre_snake>`     | `state_captura_escaneando`      |
| Transición           | `trans_<diagrama>_<origen>_<destino>` | `trans_captura_idle_escaneando` |
| Nodo de despliegue   | `node_<clave>`                        | `node_nginx`                    |
| Paquete              | `pkg_<clave>`                         | `pkg_mobile`                    |

---

## 3. Paleta de colores institucional

Todos los elementos visuales deben usar exactamente estos valores. **No están sujetos a preferencia; son obligatorios.**

| Elemento                            | Propiedad StarUML        | Valor hex |
| ----------------------------------- | ------------------------ | --------- |
| Fondo de clases, actores, lifelines | `fillColor`              | `#EBF5FB` |
| Bordes, líneas, flechas             | `lineColor`              | `#2980B9` |
| Fondo de enumeraciones y notas      | `fillColor`              | `#FFFDE7` |
| Texto (por defecto)                 | `fontColor`              | `#000000` |
| Fondo del área del diagrama         | (propiedad del diagrama) | `#FAFAFA` |

En el script Python, definir estas constantes como:

```python
_V = {
    "fillColor":   "#EBF5FB",
    "lineColor":   "#2980B9",
    "fontColor":   "#000000",
    "font":        "Arial;13;0",
    "parentStyle": False,
}
_NOTE_V   = {**_V, "fillColor": "#FFFDE7"}   # notas y enumeraciones
_ENUM_V   = {**_V, "fillColor": "#FFFDE7"}
```

---

## 4. Tipos de diagramas y sus tipos StarUML

| Diagrama PlantUML        | Tipo StarUML           | Tipo de vista de diagrama |
| ------------------------ | ---------------------- | ------------------------- |
| `@startuml ... usecase`  | `UMLUseCaseDiagram`    | `UMLUseCaseDiagram`       |
| `@startuml ... class`    | `UMLClassDiagram`      | `UMLClassDiagram`         |
| `@startuml ... package`  | `UMLPackageDiagram`    | `UMLPackageDiagram`       |
| `@startuml ... sequence` | `UMLSequenceDiagram`   | `UMLSequenceDiagram`      |
| `@startuml ... state`    | `UMLStatechartDiagram` | `UMLStatechartDiagram`    |
| `@startuml ... deploy`   | `UMLDeploymentDiagram` | `UMLDeploymentDiagram`    |

### 4.1 Vistas de elementos por tipo de diagrama

**Casos de uso:**

- Actor → `UMLActorView` (figura de palito, `width:80, height:100`)
- Caso de uso → `UMLUseCaseView` (elipse, `width:160, height:40` mínimo)
- Asociación → `UMLAssociationView` (línea simple)
- Include / Extend → `UMLIncludeView` / `UMLExtendView` (flecha punteada con estereotipo)

**Clases:**

- Clase → `UMLClassView` con `UMLNameCompartmentView`, `UMLAttributeCompartmentView`, `UMLOperationCompartmentView`
- Asociación → `UMLAssociationView`; composición → `UMLAssociationView` con `aggregation:"composite"` en el extremo
- Generalización → `UMLGeneralizationView`

**Secuencia:**

- Participante → `UMLSeqLifelineView` con `UMLNameCompartmentView` + `UMLLinePartView` (línea vertical)
- Mensaje síncrono → `UMLSeqMessageView` con `messageSort:"synchCall"`
- Mensaje de respuesta → `UMLSeqMessageView` con `messageSort:"reply"`, línea punteada
- Fragmento combinado → `UMLCombinedFragmentView` con `interactionOperator` (`alt`, `opt`, `loop`, `ref`)
- Activación → `UMLActivationView` sobre la lifeline

**Estados:**

- Estado → `UMLStateView` (rectángulo redondeado)
- Estado inicial → `UMLPseudostateView` con `kind:"initial"`
- Estado final → `UMLFinalStateView`
- Transición → `UMLTransitionView`; la guardia se anota en la propiedad `guard`

**Paquetes:**

- Paquete → `UMLPackageView` (rectángulo con pestaña)
- Componente dentro de paquete → `UMLComponentView`

**Despliegue:**

- Nodo → `UMLNodeView` (cubo 3D)
- Artefacto → `UMLArtifactView`
- Dependencia entre nodos → `UMLDependencyView`

---

## 5. Guía de layout (coordenadas)

El origen `(0,0)` es la esquina superior izquierda del canvas de StarUML. Las unidades son píxeles lógicos.

### 5.1 Espaciados mínimos

| Entre elementos                    | Espacio mínimo |
| ---------------------------------- | -------------- |
| Clases en diagrama de clases       | 40 px          |
| Columnas de lifelines en secuencia | 150 px         |
| Filas de casos de uso              | 80 px          |
| Nodos en diagrama de despliegue    | 60 px          |
| Estados en diagrama de estados     | 60 px          |

### 5.2 Punto de partida recomendado

- Primer elemento: `left=40, top=40`
- Diagramas de secuencia: lifelines comienzan en `top=40`; mensajes empiezan en `top=120` con incremento de `60 px` por mensaje

### 5.3 Tamaños por defecto

| Tipo                 | width | height |
| -------------------- | ----- | ------ |
| `UMLClassView`       | 200   | 80+    |
| `UMLActorView`       | 80    | 100    |
| `UMLUseCaseView`     | 160   | 40     |
| `UMLSeqLifelineView` | 120   | 2000+  |
| `UMLStateView`       | 120   | 40     |
| `UMLPackageView`     | 240   | 160+   |
| `UMLNodeView`        | 200   | 80     |

---

## 6. Catálogo de diagramas del proyecto

Los siguientes 16 diagramas deben existir en el archivo maestro. El nombre de la constante en el script es el identificador estable.

### Sprint 0 (modelo: `model_sprint0_uc` y `model_sprint0_arch`)

| #   | Nombre constante                  | Tipo StarUML           | Fuente PlantUML                                                         |
| --- | --------------------------------- | ---------------------- | ----------------------------------------------------------------------- |
| 1   | `Modelo_Contexto_Sprint0`         | `UMLUseCaseDiagram`    | `docs/PANELES/PANEL 1/PERFIL-PROYECTO/SPRINT-0/03-modelos-iniciales.md` |
| 2   | `Arquitectura_Paquetes_Sprint0`   | `UMLPackageDiagram`    | ídem                                                                    |
| 3   | `Despliegue_Sprint0`              | `UMLDeploymentDiagram` | ídem                                                                    |
| 4   | `Modelo_Datos_Conceptual_Sprint0` | `UMLClassDiagram`      | ídem                                                                    |

### Sprint 1 (modelo: `model_sprint1`)

| #   | Nombre constante                  | Tipo StarUML           | Fuente PlantUML                                               |
| --- | --------------------------------- | ---------------------- | ------------------------------------------------------------- |
| 5   | `Contexto_Sprint1`                | `UMLUseCaseDiagram`    | `docs/PANELES/PANEL 1/PERFIL-PROYECTO/SPRINT-1/02-modelos.md` |
| 6   | `Paquetes_Sprint1`                | `UMLPackageDiagram`    | ídem                                                          |
| 7   | `Despliegue_Sprint1`              | `UMLDeploymentDiagram` | ídem                                                          |
| 8   | `Datos_Conceptual_Sprint1`        | `UMLClassDiagram`      | ídem                                                          |
| 9   | `Secuencia_Autenticacion_Sprint1` | `UMLSequenceDiagram`   | ídem                                                          |

### Sprint 2 (modelo: `model_sprint2`)

| #   | Nombre constante                | Tipo StarUML         | Fuente PlantUML                                              |
| --- | ------------------------------- | -------------------- | ------------------------------------------------------------ |
| 10  | `Sprint2_CasosUso`              | `UMLUseCaseDiagram`  | `docs/PANELES/PANEL 2/FUNDAMENTACION/SPRINT-2/02-modelos.md` |
| 11  | `Sprint2_Clases`                | `UMLClassDiagram`    | ídem                                                         |
| 12  | `Sprint2_Secuencia_Subida`      | `UMLSequenceDiagram` | ídem                                                         |
| 13  | `Sprint2_Secuencia_Calibracion` | `UMLSequenceDiagram` | ídem                                                         |

### Sprint 3 (modelo: `model_sprint3`)

| #   | Nombre constante            | Tipo StarUML           | Fuente PlantUML                                              |
| --- | --------------------------- | ---------------------- | ------------------------------------------------------------ |
| 14  | `Sprint3_CasosUso`          | `UMLUseCaseDiagram`    | `docs/PANELES/PANEL 2/FUNDAMENTACION/SPRINT-3/02-modelos.md` |
| 15  | `Sprint3_Secuencia_Captura` | `UMLSequenceDiagram`   | ídem                                                         |
| 16  | `Sprint3_Estados`           | `UMLStatechartDiagram` | ídem                                                         |

---

## 7. Script de generación: `diagrams/generar_paneles.py`

### 7.1 Estructura del script

```
diagrams/generar_paneles.py
├── Imports y constantes (_V, _NOTE_V, _sid)
├── Helpers de vista
│   ├── class_view(diag_id, model_id, left, top, w) → (vid, dict)
│   ├── actor_view(diag_id, model_id, left, top) → (vid, dict)
│   ├── uc_view(diag_id, model_id, left, top, w) → (vid, dict)
│   ├── pkg_view(diag_id, model_id, left, top, w, h) → (vid, dict)
│   ├── node_view(diag_id, model_id, left, top, w) → (vid, dict)
│   ├── lifeline_view(diag_id, model_id, left, top, w, h) → (vid, dict)
│   ├── message_view(diag_id, msg_id, src_ll_vid, tgt_ll_vid, y, label, sort) → (vid, dict)
│   ├── state_view(diag_id, model_id, left, top, w) → (vid, dict)
│   └── transition_view(diag_id, trans_id, src_vid, tgt_vid, ...) → (vid, dict)
├── Constructores de modelos (uno por diagrama)
│   ├── _build_contexto_sprint0() → dict (UMLModel)
│   ├── _build_arquitectura_sprint0() → dict (UMLModel)
│   ├── _build_sprint1() → dict (UMLModel)
│   ├── _build_sprint2() → dict (UMLModel)
│   └── _build_sprint3() → dict (UMLModel)
└── main(): ensambla el Project y escribe el .mdj
```

### 7.2 Plantilla de diagrama de secuencia

```python
def lifeline_view(diag_id, model_id, left, top=40, w=120, h=2000):
    vid = _sid(f"v_ll_{diag_id}_{model_id}")
    name_comp_id = _sid(f"v_nc_{diag_id}_{model_id}")
    line_part_id = _sid(f"v_lp_{diag_id}_{model_id}")
    return vid, {
        "_type": "UMLSeqLifelineView", "_id": vid,
        "_parent": {"$ref": diag_id},
        "model": {"$ref": model_id},
        "font": "Arial;13;0", "parentStyle": False,
        "left": left, "top": top, "width": w, "height": h,
        **_V,
        "nameCompartment": {"$ref": name_comp_id},
        "linePart": {"$ref": line_part_id},
        "subViews": [
            {"_type": "UMLNameCompartmentView", "_id": name_comp_id,
             "_parent": {"$ref": vid}, "model": {"$ref": model_id},
             "parentStyle": True, "font": "Arial;13;0",
             "left": left, "top": top, "width": w, "height": 40},
            {"_type": "UMLLinePartView", "_id": line_part_id,
             "_parent": {"$ref": vid}, "model": {"$ref": model_id},
             "parentStyle": False, "font": "Arial;13;0",
             "left": left + w // 2, "top": top + 40,
             "width": 1, "height": h - 40},
        ]
    }

def message_view(diag_id, msg_id, src_ll_vid, tgt_ll_vid,
                 sx, sy, tx, ty, label, sort="synchCall"):
    vid = _sid(f"v_msg_{diag_id}_{msg_id}")
    return vid, {
        "_type": "UMLSeqMessageView", "_id": vid,
        "_parent": {"$ref": diag_id},
        "model": {"$ref": msg_id},
        "font": "Arial;13;0", "parentStyle": False,
        "lineColor": "#2980B9",
        "source": {"$ref": src_ll_vid},
        "target": {"$ref": tgt_ll_vid},
        "points": f"{sx},{sy} {tx},{ty}",
    }
```

### 7.3 Plantilla de diagrama de estados

```python
def state_view(diag_id, model_id, left, top, w=120, h=40):
    vid = _sid(f"v_state_{diag_id}_{model_id}")
    return vid, {
        "_type": "UMLStateView", "_id": vid,
        "_parent": {"$ref": diag_id},
        "model": {"$ref": model_id},
        "font": "Arial;13;0", **_V,
        "left": left, "top": top, "width": w, "height": h,
    }

def pseudostate_view(diag_id, model_id, left, top, kind="initial"):
    vid = _sid(f"v_ps_{diag_id}_{model_id}")
    return vid, {
        "_type": "UMLPseudostateView", "_id": vid,
        "_parent": {"$ref": diag_id},
        "model": {"$ref": model_id},
        "font": "Arial;13;0", **_V,
        "fillColor": "#2980B9",
        "left": left, "top": top, "width": 20, "height": 20,
    }
```

### 7.4 Reutilizar `docs/XMI/render_mdj.py`

El archivo `docs/XMI/render_mdj.py` contiene funciones de referencia para:

- `class_view`, `enum_view`, `assoc_view` — clases y asociaciones
- `actor_view`, `uc_view` — casos de uso
- `pkg_view`, `node_view`, `dep_view` — paquetes y despliegue
- `_sid`, `_V`, `ref` — utilidades base

El script `diagrams/generar_paneles.py` debe importar o replicar estas funciones. No duplicar código innecesariamente.

---

## 8. Procedimientos

### 8.1 Agregar un diagrama nuevo

1. Determinar a qué sprint pertenece y usar el `UMLModel` correspondiente
2. Crear la función constructora `_build_<nombre>()` en `generar_paneles.py`
3. Registrar el diagrama en la sección 6 de este skill con su nombre constante
4. Asignar IDs estables con `_sid()` usando la convención de la sección 2.3
5. Aplicar la paleta de colores de la sección 3
6. Verificar que todos los tipos usados son UML 2.5+ (sección 1)
7. Ejecutar `python diagrams/generar_paneles.py` y abrir el `.mdj` en StarUML para validar visualmente

### 8.2 Actualizar un diagrama existente

1. Localizar la función constructora en `generar_paneles.py`
2. Modificar el modelo semántico (elementos en `ownedElements`)
3. Actualizar las vistas correspondientes (elementos en `ownedViews`)
4. Mantener los IDs estables — no cambiar las claves `_sid()` de elementos existentes
5. Regenerar y validar en StarUML

### 8.3 Importar como fragmento (`.mfj`)

Si se prefiere importar un diagrama individual en lugar de regenerar todo el proyecto:

1. El `.mfj` comienza directamente desde el elemento raíz (sin nodo `Project`)
2. El `_parent` del elemento raíz apunta al ID del modelo padre en el `.mdj` destino
3. En StarUML: `File > Import > Fragment...` y seleccionar el `.mfj`
4. Verificar que los IDs del fragmento no colisionen con los del proyecto existente

### 8.4 Validar el archivo `.mdj`

Ejecutar la siguiente verificación antes de commit:

```bash
python -c "
import json, sys
with open('diagrams/Modelos - Wireless Headmapper.mdj') as f:
    d = json.load(f)
def check(o, path=''):
    if isinstance(o, dict):
        t = o.get('_type','')
        if 'Diagram' in t or 'Model' in t:
            if not o.get('_id'):
                print(f'Sin _id: {path}')
        for k,v in o.items():
            check(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i,item in enumerate(o):
            check(item, f'{path}[{i}]')
check(d)
print('Validación completada.')
"
```

---

## 9. Restricciones

- **No usar notación UML anterior a 2.5.** Verificar contra la spec OMG 2.5.1 ante cualquier duda.
- No modificar `diagrams/Modelos - Wireless Headmapper.mdj` manualmente con un editor de texto — usar solo el script de generación o StarUML.
- No mezclar diagramas de sprints distintos en el mismo `UMLModel`.
- No cambiar los nombres constantes de la sección 6 una vez que el diagrama existe en el `.mdj` (rompe referencias).
- No usar colores distintos a los de la sección 3 sin autorización explícita del equipo.
- No eliminar diagramas existentes sin actualizar el catálogo de la sección 6.
- Toda adición o cambio al `.mdj` debe hacerse a través del script `generar_paneles.py` para garantizar reproducibilidad.

---

## 10. Contexto del proyecto

- **Cliente real:** Bulldog Tech. (empresa tecnológica, Santa Cruz de la Sierra, Bolivia)
- **Sistema:** Wireless HeatMapper — app Android + backend FastAPI + panel web React
- **Equipo:** Fernandez Ortega Jhasmany Jhunnior (Scrum Master) y Quiroga Flores Herland Borys (Product Owner)
- **Herramienta de modelado:** StarUML 6.x — formato `.mdj` (JSON, UML 2.5+)
- **Script de referencia:** `docs/XMI/render_mdj.py` — infraestructura Python existente
- **Paleta de colores:** `#EBF5FB` (fondo), `#2980B9` (bordes), `#FFFDE7` (notas/enums), `#FAFAFA` (canvas)
