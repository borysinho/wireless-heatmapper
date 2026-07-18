#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOC_DIR="$ROOT_DIR/DOCUMENTACION"
DIAGRAM_DIR="$ROOT_DIR/diagramas"
ASSET_DIR="$ROOT_DIR/assets"
BUILD_DIR="$ROOT_DIR/build"
DIAGRAM_ASSET_DIR="$ASSET_DIR/diagramas"
MERGED="$BUILD_DIR/WirelessHeatMapper-SW2-Consolidado.md"
OUTPUT="$BUILD_DIR/WirelessHeatMapper-SW2-Consolidado.docx"

mkdir -p "$ASSET_DIR" "$BUILD_DIR" "$DIAGRAM_ASSET_DIR"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: falta el comando requerido: $cmd" >&2
    exit 1
  fi
}

generate_qr() {
  local url="$1"
  local output="$2"
  if command -v qrencode >/dev/null 2>&1; then
    qrencode -o "$output" -s 8 -m 2 "$url"
  elif command -v python3 >/dev/null 2>&1; then
    set +e
    PYTHONPATH="${PYTHONPATH:-}:/tmp/codex-qrcode" python3 - "$url" "$output" <<'PY'
import sys

try:
    import qrcode
except ModuleNotFoundError:
    sys.exit(2)

url = sys.argv[1]
output = sys.argv[2]
img = qrcode.make(url)
img.save(output)
PY
    status=$?
    set -e
    if [[ "$status" -eq 2 ]]; then
      echo "ADVERTENCIA: no se encontro qrencode ni el paquete Python qrcode; no se genero $output" >&2
    elif [[ "$status" -ne 0 ]]; then
      exit "$status"
    fi
  else
    echo "ADVERTENCIA: no se encontro qrencode ni python3; no se genero $output" >&2
  fi
}

render_diagrams() {
  if command -v plantuml >/dev/null 2>&1; then
    JAVA_TOOL_OPTIONS="${JAVA_TOOL_OPTIONS:-} -Djava.awt.headless=true" plantuml -tpng -o "$DIAGRAM_ASSET_DIR" "$DIAGRAM_DIR"/*.puml
  elif command -v java >/dev/null 2>&1 && [[ -f "$ROOT_DIR/../PlantUML_Language_Reference_Guide_en.pdf" ]]; then
    echo "ADVERTENCIA: plantuml no esta instalado como comando. Instale PlantUML para renderizar los diagramas." >&2
  else
    echo "ADVERTENCIA: no se encontro plantuml; el Word se generara sin imagenes UML renderizadas." >&2
  fi
}

append_point() {
  local title="$1"
  local file="$2"

  {
    printf '\n\n'
    printf '### %s\n\n' "$title"
  } >> "$MERGED"

  awk '
    NR == 1 && /^# / { next }
    /^#/ { print "##" $0; next }
    { print }
  ' "$file" >> "$MERGED"
}

append_diagram_section() {
  local title="$1"
  shift

  {
    printf '\n\n'
    printf '#### %s\n\n' "$title"
  } >> "$MERGED"

  for puml in "$@"; do
    local base
    local png
    local diagram_title
    base="$(basename "$puml" .puml)"
    png="$DIAGRAM_ASSET_DIR/$base.png"
    diagram_title="$(echo "$base" | sed 's/[0-9][0-9]-//; s/-/ /g')"
    {
      printf '\n'
      printf '##### %s\n\n' "$diagram_title"
      if [[ -f "$png" ]]; then
        printf '![%s](%s)\n\n' "$diagram_title" "$png"
      else
        printf 'Archivo PlantUML: `%s`.\n\n' "$puml"
      fi
    } >> "$MERGED"
  done
}

append_qr() {
  local title="$1"
  local url="$2"
  local image="$3"

  {
    printf '\n'
    printf '##### %s\n\n' "$title"
    printf '<%s>\n\n' "$url"
    if [[ -f "$image" ]]; then
      printf '![QR %s](%s)\n\n' "$title" "$image"
    fi
  } >> "$MERGED"
}

generate_qr "https://github.com/borysinho/wireless-heatmapper" "$ASSET_DIR/qr-repositorio.png"
generate_qr "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/" "$ASSET_DIR/qr-frontend.png"
generate_qr "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/" "$ASSET_DIR/qr-sitio-empresa.png"
generate_qr "https://www.facebook.com/profile.php?id=61591962512748" "$ASSET_DIR/qr-facebook.png"
generate_qr "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/docs" "$ASSET_DIR/qr-api-docs.png"
generate_qr "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/" "$ASSET_DIR/qr-manual.png"
generate_qr "https://github.com/borysinho/wireless-heatmapper/releases" "$ASSET_DIR/qr-releases.png"

render_diagrams

: > "$MERGED"
cat >> "$MERGED" <<'EOF'
---
title: "Clase 21/04/2026 — Aspectos Generales del Proyecto"
subtitle: "Documentación SW2 - Wireless HeatMapper"
author:
  - "Grupo 24 - Team 24 Software"
date: "Gestión 2026"
lang: es-BO
---

# Clase 21/04/2026 — Aspectos Generales del Proyecto

> **Contexto:** El documento consolidado sigue la estructura solicitada por la clase del 21/04/2026 para presentar los aspectos generales del proyecto de Ingeniería de Software II. Cada grupo se presenta como una empresa de software real.

---

## Organización inicial de grupos

- **Grupo:** 24.
- **Empresa de software:** Team 24 Software.
- **Integrantes:** Jhasmany Jhunnior Fernandez Ortega; Herland Borys Quiroga Flores.
- **Cliente del caso:** Bulldog Tech.
- **Proyecto:** Sistema Inteligente de Análisis y Optimización de Cobertura WiFi mediante Mapas de Calor.
- **Modalidad del producto:** 100 % en línea.

---

## Puntos del Proyecto de la Materia

El docente recapitula que el proyecto tiene múltiples puntos que deben entregarse. A continuación se desarrolla cada uno aplicado a Wireless HeatMapper y Team 24 Software.
EOF

append_point "Punto 1 — PAPS" "$DOC_DIR/02-paps.md"
append_point "Punto 2 — Modelos de Desarrollo" "$DOC_DIR/03-modelos-desarrollo.md"
append_diagram_section "Evidencias de los cuatro modelos obligatorios" \
  "$DIAGRAM_DIR/01-modelo-contexto.puml" \
  "$DIAGRAM_DIR/02-arquitectura-paquetes.puml" \
  "$DIAGRAM_DIR/03-arquitectura-despliegue.puml" \
  "$DIAGRAM_DIR/04-modelo-datos-conceptual.puml" \
  "$DIAGRAM_DIR/05-logica-captura-heatmap.puml" \
  "$DIAGRAM_DIR/06-logica-portal-cliente.puml" \
  "$DIAGRAM_DIR/07-estados-proyecto.puml"
append_point "Punto 3 — Plan/Manual de Garantía de Calidad del Software (SQA / QAP)" "$DOC_DIR/04-manual-calidad.md"
append_point "Punto 4 — Herramientas CASE" "$DOC_DIR/05-herramientas-case.md"
append_diagram_section "Evidencia de navegabilidad CASE" \
  "$DIAGRAM_DIR/08-case-navegabilidad.puml"
append_point "Punto 5 — Aspectos Legales para Apertura de Empresa de Software" "$DOC_DIR/06-aspectos-legales.md"
append_point "Punto 6 — Infraestructura para la Producción de Software" "$DOC_DIR/07-infraestructura-produccion.md"
append_point "Punto 7 — Sitio Web de la Empresa" "$DOC_DIR/08-sitio-web-empresa.md"
{
  printf '\n\n'
  printf '#### Evidencias públicas del sitio web\n\n'
} >> "$MERGED"
append_qr "Sitio empresarial Team 24 Software" "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/" "$ASSET_DIR/qr-sitio-empresa.png"
append_qr "Facebook oficial Team 24 Software" "https://www.facebook.com/profile.php?id=61591962512748" "$ASSET_DIR/qr-facebook.png"
append_point "Punto 8 — Estudio de Mercado" "$DOC_DIR/09-estudio-mercado.md"
append_point "Punto 9 — Pruebas del Software" "$DOC_DIR/10-plan-pruebas.md"
append_diagram_section "Evidencia del flujo de trabajo de pruebas" \
  "$DIAGRAM_DIR/09-flujo-pruebas-rup.puml"
append_point "Punto 10 — Marketing" "$DOC_DIR/11-marketing.md"
append_point "Punto 11 — Aspectos para la Puesta en Marcha" "$DOC_DIR/12-puesta-marcha.md"
append_point "Punto 12 — Software como Producto (Entregable Final)" "$DOC_DIR/13-software-producto.md"
{
  printf '\n\n'
  printf '#### Evidencias públicas del producto\n\n'
} >> "$MERGED"
append_qr "Repositorio GitHub" "https://github.com/borysinho/wireless-heatmapper" "$ASSET_DIR/qr-repositorio.png"
append_qr "Documentación Swagger / OpenAPI" "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/docs" "$ASSET_DIR/qr-api-docs.png"
append_qr "Manual de usuario" "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/" "$ASSET_DIR/qr-manual.png"
append_qr "Releases móviles" "https://github.com/borysinho/wireless-heatmapper/releases" "$ASSET_DIR/qr-releases.png"

cat >> "$MERGED" <<'EOF'

---

## Fechas y Dinámica de Entrega

- **Fecha máxima:** dos semanas antes del último día de clases, según la indicación docente.
- **Entrega incremental:** los puntos pueden revisarse a lo largo del semestre conforme se avance en Scrum.
- **Gestión Scrum:** el tablero, los sprints, el backlog y las evidencias deben mantenerse actualizados sin esperar aviso de revisión.
- **Estado del proyecto:** Wireless HeatMapper se documenta como producto integrado en línea con backend, web, app móvil, despliegue y evidencias públicas.

---

## Actividad del día (21/04/2026)

- La clase se orientó a revisiones con Scrum y seguimiento del estado del sprint/tablero de cada grupo.
- El equipo mantiene la documentación del proyecto como evidencia del avance de Team 24 Software.
- El uso de IA se considera apoyo responsable dentro del enfoque de Desarrollo Dirigido por Especificación, conservando trazabilidad entre requerimientos, diseño, implementación, pruebas y entrega.

---

## Resumen de los 12 Puntos del Proyecto

| # | Punto | Descripción breve | Evidencia en este documento |
| - | ----- | ----------------- | --------------------------- |
| 1 | **PAPS** | Plan Aplicado a Proyecto de Software. | Punto 1. |
| 2 | **Modelos de Desarrollo** | Contexto, Arquitectura, Datos y Lógica con Scrum. | Punto 2 y diagramas UML. |
| 3 | **Manual de Garantía de Calidad** | ISO/IEEE/CMMI aplicado a la empresa, no solo al producto. | Punto 3. |
| 4 | **Herramientas CASE** | Demostración de navegabilidad y uso real de herramientas CASE. | Punto 4 y diagrama de navegabilidad. |
| 5 | **Aspectos Legales** | Trámites para apertura de empresa de software en Bolivia. | Punto 5. |
| 6 | **Infraestructura para producción** | Gestión, versionado, CI/CD, Docker, despliegue e IA integrada. | Punto 6. |
| 7 | **Sitio Web** | Sitio publicado, empresa de software, soporte, contacto y chatbot. | Punto 7 y QR públicos. |
| 8 | **Estudio de Mercado** | Cuantificación, segmentación y monetización basadas en números. | Punto 8. |
| 9 | **Pruebas** | Unidad, QA, PO, caja blanca, checklists y herramientas. | Punto 9 y flujo de pruebas. |
| 10 | **Marketing** | Estrategias y materiales para promocionar el producto. | Punto 10. |
| 11 | **Puesta en Marcha** | AWS/GCP/Azure, licencias, tiendas, términos y privacidad. | Punto 11. |
| 12 | **Software como Producto** | Entrega final completa y funcional. | Punto 12. |

EOF

require_cmd pandoc

PANDOC_ARGS=(
  "$MERGED"
  -o "$OUTPUT"
  --from markdown
  --toc
  --toc-depth=3
  --metadata lang=es-BO
)

REFERENCE_DOCX="$ROOT_DIR/reference.docx"
if [[ -f "$REFERENCE_DOCX" ]]; then
  PANDOC_ARGS+=(--reference-doc "$REFERENCE_DOCX")
fi

pandoc "${PANDOC_ARGS[@]}"

echo "Documento generado: $OUTPUT"
echo "Markdown consolidado: $MERGED"
