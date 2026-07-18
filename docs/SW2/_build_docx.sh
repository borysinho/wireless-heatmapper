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

append_document() {
  local file="$1"
  printf '\n\n' >> "$MERGED"
  cat "$file" >> "$MERGED"
}

generate_qr "https://github.com/borysinho/wireless-heatmapper" "$ASSET_DIR/qr-repositorio.png"
generate_qr "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/" "$ASSET_DIR/qr-frontend.png"
generate_qr "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/" "$ASSET_DIR/qr-manual.png"
generate_qr "https://github.com/borysinho/wireless-heatmapper/releases" "$ASSET_DIR/qr-releases.png"

render_diagrams

: > "$MERGED"
for file in "$DOC_DIR"/*.md; do
  append_document "$file"
done

cat >> "$MERGED" <<'EOF'

\newpage

# Figuras UML renderizadas

EOF

for puml in "$DIAGRAM_DIR"/*.puml; do
  base="$(basename "$puml" .puml)"
  png="$DIAGRAM_ASSET_DIR/$base.png"
  if [[ -f "$png" ]]; then
    title="$(echo "$base" | sed 's/[0-9][0-9]-//; s/-/ /g')"
    {
      echo
      echo "## $title"
      echo
      echo "![$title]($png)"
      echo
    } >> "$MERGED"
  fi
done

cat >> "$MERGED" <<EOF

\newpage

# Codigos QR

## Repositorio GitHub

<https://github.com/borysinho/wireless-heatmapper>

$(if [[ -f "$ASSET_DIR/qr-repositorio.png" ]]; then echo "![QR repositorio]($ASSET_DIR/qr-repositorio.png)"; fi)

## Frontend publicado

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/>

$(if [[ -f "$ASSET_DIR/qr-frontend.png" ]]; then echo "![QR frontend]($ASSET_DIR/qr-frontend.png)"; fi)

## Manual de usuario

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/>

$(if [[ -f "$ASSET_DIR/qr-manual.png" ]]; then echo "![QR manual]($ASSET_DIR/qr-manual.png)"; fi)

## Releases moviles

<https://github.com/borysinho/wireless-heatmapper/releases>

$(if [[ -f "$ASSET_DIR/qr-releases.png" ]]; then echo "![QR releases]($ASSET_DIR/qr-releases.png)"; fi)

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
