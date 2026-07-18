#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOC_DIR="$ROOT_DIR/DOCUMENTACION"
PROJECT_DOCS_DIR="$(cd "$ROOT_DIR/.." && pwd)"
PAPS_SOURCE="$PROJECT_DOCS_DIR/ONLINE/PLAN-IMPLEMENTACION/02-paps.md"
SQAP_SOURCE="$PROJECT_DOCS_DIR/SQAP/Manual de Calidad - SQAP.md"
DIAGRAM_DIR="$ROOT_DIR/diagramas"
ASSET_DIR="$ROOT_DIR/assets"
BUILD_DIR="$ROOT_DIR/build"
DIAGRAM_ASSET_DIR="$ASSET_DIR/diagramas"
MERGED="$BUILD_DIR/WirelessHeatMapper-SW2-Consolidado.md"
OUTPUT="$BUILD_DIR/WirelessHeatMapper-SW2-Consolidado.docx"
NORMALIZED_PAPS="$(mktemp "${TMPDIR:-/tmp}/wireless-paps-normalizado.XXXXXX.md")"

cleanup() {
  rm -f "$NORMALIZED_PAPS"
}
trap cleanup EXIT

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

normalize_paps_tables() {
  local input="$1"
  local output="$2"

  python3 - "$input" "$output" <<'PY'
import re
import sys

entrada = sys.argv[1]
salida = sys.argv[2]


def es_separador(linea: str) -> bool:
    return linea.strip() == "---"


def limpiar(texto: str) -> str:
    texto = texto.replace("**", "")
    texto = re.sub(r"\s+", " ", texto.strip())
    return texto


def sin_negrita(texto: str) -> str:
    return texto.replace("**", "").strip()


def extraer_encabezados(lineas: list[str]) -> list[str]:
    unido = " ".join(limpiar(linea) for linea in lineas if linea.strip())
    encabezados = re.findall(r"\*\*(.*?)\*\*", " ".join(linea.strip() for linea in lineas), flags=re.S)
    encabezados = [limpiar(encabezado) for encabezado in encabezados]
    if len(encabezados) >= 2:
        return encabezados

    partes = [limpiar(parte) for parte in re.split(r"\s{2,}", unido) if limpiar(parte)]
    return partes if len(partes) >= 2 else []


def token_valor(token: str) -> bool:
    token = token.strip(",.;:()")
    return bool(re.fullmatch(r"[0-9]+([.,][0-9]+)?%?|\d{1,2}\s*[A-Za-z]+|[A-Z][0-9]?|---|[0-9]+[+]?|[0-9]+-[0-9]+", token))


def partir_linea(linea: str, columnas: int) -> list[str] | None:
    texto = sin_negrita(linea)
    if not texto:
        return None

    partes = [parte for parte in re.split(r"\s{2,}", texto) if parte]
    if len(partes) >= columnas:
        return partes[: columnas - 1] + [" ".join(partes[columnas - 1 :])]

    tokens = texto.split()
    if columnas >= 3 and len(tokens) >= columnas and all(token_valor(token) for token in tokens[-(columnas - 1) :]):
        return [" ".join(tokens[: -(columnas - 1)])] + tokens[-(columnas - 1) :]

    if columnas == 4 and len(tokens) >= 4 and all(token_valor(token) for token in tokens[-3:]):
        return [" ".join(tokens[:-3])] + tokens[-3:]

    if columnas == 3 and len(tokens) >= 4 and token_valor(tokens[-2]) and token_valor(tokens[-1]):
        return [" ".join(tokens[:-2]), tokens[-2], tokens[-1]]

    return None


def agregar_continuacion(filas: list[list[str]], linea: str, columnas: int) -> None:
    if not filas:
        return

    texto = sin_negrita(linea)
    if not texto:
        return

    partes = [parte for parte in re.split(r"\s{2,}", texto) if parte]
    sangria = len(linea) - len(linea.lstrip(" "))

    if 1 < len(partes) < columnas:
        filas[-1][0] = limpiar(f"{filas[-1][0]} {partes[0]}")
        filas[-1][-1] = limpiar(f"{filas[-1][-1]} {' '.join(partes[1:])}")
        return

    destino = columnas - 1 if sangria > 15 else 0
    filas[-1][destino] = limpiar(f"{filas[-1][destino]} {texto}")


def normalizar_filas(lineas: list[str], columnas: int) -> list[list[str]]:
    filas: list[list[str]] = []
    for linea in lineas:
        if not linea.strip():
            continue

        fila = partir_linea(linea, columnas)
        if fila:
            fila = [limpiar(celda) for celda in fila]
            if any(celda for celda in fila):
                filas.append(fila)
            continue

        agregar_continuacion(filas, linea, columnas)

    return filas


def escapar(texto: str) -> str:
    return texto.replace("|", "\\|")


def emitir_tabla(encabezados: list[str], filas: list[list[str]]) -> list[str]:
    if not encabezados or not filas:
        return []
    columnas = len(encabezados)
    filas = [(fila + [""] * columnas)[:columnas] for fila in filas]
    salida_tabla = [
        "| " + " | ".join(escapar(celda) for celda in encabezados) + " |",
        "| " + " | ".join("---" for _ in encabezados) + " |",
    ]
    salida_tabla.extend("| " + " | ".join(escapar(celda) for celda in fila) + " |" for fila in filas)
    return salida_tabla


with open(entrada, "r", encoding="utf-8-sig") as archivo:
    lineas = archivo.read().splitlines()

resultado: list[str] = []
i = 0
while i < len(lineas):
    if not es_separador(lineas[i]):
        resultado.append(lineas[i])
        i += 1
        continue

    inicio = i + 1
    while inicio < len(lineas) and not lineas[inicio].strip():
        inicio += 1

    medio = inicio
    while medio < len(lineas) and not es_separador(lineas[medio]):
        medio += 1

    fin = medio + 1
    while fin < len(lineas) and not es_separador(lineas[fin]):
        fin += 1

    if medio < len(lineas) and fin < len(lineas):
        encabezados = extraer_encabezados(lineas[inicio:medio])
        if len(encabezados) >= 2:
            filas = normalizar_filas(lineas[medio + 1 : fin], len(encabezados))
            tabla = emitir_tabla(encabezados, filas)
            if tabla:
                resultado.extend(tabla)
                i = fin + 1
                continue

    resultado.append(lineas[i])
    i += 1

with open(salida, "w", encoding="utf-8") as archivo:
    archivo.write("\n".join(resultado) + "\n")
PY
}

append_shifted_markdown() {
  local file="$1"
  local skip_first_h1="${2:-true}"
  local source_dir
  source_dir="$(cd "$(dirname "$file")" && pwd)"

  awk -v skip_first_h1="$skip_first_h1" -v source_dir="$source_dir" '
    BEGIN { skipped = (skip_first_h1 == "true") ? 0 : 1 }
    skipped == 0 && /^# / { skipped = 1; next }
    skipped == 0 { next }
    function print_shifted_heading(line, hashes, text) {
      match(line, /^#+/)
      hashes = substr(line, RSTART, RLENGTH)
      text = substr(line, RLENGTH + 2)
      sub(/^[0-9]+([.][0-9]+)*[.)]?[[:space:]]+/, "", text)
      print "#" hashes " " text
    }
    {
      gsub(/\]\(assets\/team-24-software-logo\.svg\)/, "](" source_dir "/assets/team-24-software-logo.png)")
      gsub(/\]\(assets\//, "](" source_dir "/assets/")
      if (/^###### /) {
        print_shifted_heading($0)
      } else if (/^##### /) {
        print_shifted_heading($0)
      } else if (/^#### /) {
        print_shifted_heading($0)
      } else if (/^### /) {
        print_shifted_heading($0)
      } else if (/^## /) {
        print_shifted_heading($0)
      } else if (/^# /) {
        print_shifted_heading($0)
      } else {
        print
      }
    }
  ' "$file" >> "$MERGED"
}

append_point() {
  local title="$1"
  local file="$2"

  {
    printf '\n\n'
    printf '# %s\n\n' "$title"
  } >> "$MERGED"

  append_shifted_markdown "$file" true
}

append_diagram_section() {
  local title="$1"
  shift

  {
    printf '\n\n'
    printf '## %s\n\n' "$title"
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
      printf '### %s\n\n' "$diagram_title"
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
    printf '### %s\n\n' "$title"
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
normalize_paps_tables "$PAPS_SOURCE" "$NORMALIZED_PAPS"

: > "$MERGED"
cat >> "$MERGED" <<'EOF'
---
title: "Documentación formal del proyecto y empresa"
subtitle: "Team 24 Software - Wireless HeatMapper"
author:
  - "Grupo 24 - Team 24 Software"
date: "Gestión 2026"
lang: es-BO
---

| Campo | Detalle |
| ----- | ------- |
| Universidad | Universidad Autonoma Gabriel Rene Moreno |
| Facultad | Facultad de Ingenieria en Ciencias de la Computacion y Telecomunicaciones |
| Materia | Ingenieria de Software II |
| Empresa de software | Team 24 Software |
| Proyecto | Sistema Inteligente de Analisis y Optimizacion de Cobertura WiFi mediante Mapas de Calor |
| Producto | Wireless HeatMapper |
| Cliente del caso | Bulldog Tech. |
| Grupo | 24 |
| Integrantes | Jhasmany Jhunnior Fernandez Ortega; Herland Borys Quiroga Flores |
| Ciudad | Santa Cruz de la Sierra, Bolivia |
| Gestion | 2026 |
| Modalidad del producto | 100 % en linea |

El presente documento es una presentacion formal, de investigacion y de desarrollo elaborada por Team 24 Software como startup academica de desarrollo de software. La documentacion no se limita al desarrollo puntual de Wireless HeatMapper: presenta a la empresa, su sistema de calidad, su presencia web, sus politicas, su infraestructura, su estrategia de mercado, sus mecanismos de puesta en marcha y la entrega del software como producto real.

La estructura principal sigue exactamente los doce puntos solicitados en la clase del 21/04/2026:

| # | Punto |
| - | ----- |
| 1 | PAPS |
| 2 | Modelos de Desarrollo |
| 3 | Manual de Garantia de Calidad del Software SQAP |
| 4 | Herramientas CASE |
| 5 | Aspectos Legales para Apertura de Empresa de Software |
| 6 | Infraestructura para la Produccion de Software |
| 7 | Sitio Web de la Empresa |
| 8 | Estudio de Mercado |
| 9 | Pruebas del Software |
| 10 | Marketing |
| 11 | Aspectos para la Puesta en Marcha |
| 12 | Software como Producto |
EOF

append_point "1. PAPS" "$NORMALIZED_PAPS"
append_point "2. Modelos de Desarrollo" "$DOC_DIR/03-modelos-desarrollo.md"
append_diagram_section "Evidencias de los cuatro modelos obligatorios" \
  "$DIAGRAM_DIR/01-modelo-contexto.puml" \
  "$DIAGRAM_DIR/02-arquitectura-paquetes.puml" \
  "$DIAGRAM_DIR/03-arquitectura-despliegue.puml" \
  "$DIAGRAM_DIR/04-modelo-datos-conceptual.puml" \
  "$DIAGRAM_DIR/05-logica-captura-heatmap.puml" \
  "$DIAGRAM_DIR/06-logica-portal-cliente.puml" \
  "$DIAGRAM_DIR/07-estados-proyecto.puml"
append_point "3. Manual de Garantía de Calidad del Software SQAP" "$SQAP_SOURCE"
append_point "4. Herramientas CASE" "$DOC_DIR/05-herramientas-case.md"
append_diagram_section "Evidencia de navegabilidad CASE" \
  "$DIAGRAM_DIR/08-case-navegabilidad.puml"
append_point "5. Aspectos Legales para Apertura de Empresa de Software" "$DOC_DIR/06-aspectos-legales.md"
append_point "6. Infraestructura para la Producción de Software" "$DOC_DIR/07-infraestructura-produccion.md"
append_point "7. Sitio Web de la Empresa" "$DOC_DIR/08-sitio-web-empresa.md"
{
  printf '\n\n'
  printf '## Evidencias públicas del sitio web\n\n'
} >> "$MERGED"
append_qr "Sitio empresarial Team 24 Software" "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/" "$ASSET_DIR/qr-sitio-empresa.png"
append_qr "Facebook oficial Team 24 Software" "https://www.facebook.com/profile.php?id=61591962512748" "$ASSET_DIR/qr-facebook.png"
append_point "8. Estudio de Mercado" "$DOC_DIR/09-estudio-mercado.md"
append_point "9. Pruebas del Software" "$DOC_DIR/10-plan-pruebas.md"
append_diagram_section "Evidencia del flujo de trabajo de pruebas" \
  "$DIAGRAM_DIR/09-flujo-pruebas-rup.puml"
append_point "10. Marketing" "$DOC_DIR/11-marketing.md"
append_point "11. Aspectos para la Puesta en Marcha" "$DOC_DIR/12-puesta-marcha.md"
append_point "12. Software como Producto (Entregable Final)" "$DOC_DIR/13-software-producto.md"
{
  printf '\n\n'
  printf '## Evidencias públicas del producto\n\n'
} >> "$MERGED"
append_qr "Repositorio GitHub" "https://github.com/borysinho/wireless-heatmapper" "$ASSET_DIR/qr-repositorio.png"
append_qr "Documentación Swagger / OpenAPI" "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/docs" "$ASSET_DIR/qr-api-docs.png"
append_qr "Manual de usuario" "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/" "$ASSET_DIR/qr-manual.png"
append_qr "Releases móviles" "https://github.com/borysinho/wireless-heatmapper/releases" "$ASSET_DIR/qr-releases.png"

require_cmd pandoc

PANDOC_ARGS=(
  "$MERGED"
  -o "$OUTPUT"
  --from markdown
  --toc
  --toc-depth=1
  --metadata lang=es-BO
)

REFERENCE_DOCX="$ROOT_DIR/reference.docx"
if [[ -f "$REFERENCE_DOCX" ]]; then
  PANDOC_ARGS+=(--reference-doc "$REFERENCE_DOCX")
fi

pandoc "${PANDOC_ARGS[@]}"

echo "Documento generado: $OUTPUT"
echo "Markdown consolidado: $MERGED"
