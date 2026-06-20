#!/usr/bin/env bash
# _build_docx.sh — Genera el documento consolidado del Segundo Período
#
# Uso:
#   cd docs/ONLINE/PRESENTACION/CONSOLIDADO-CAPITULOS
#   bash _build_docx.sh
#
# Requisitos:
#   - pandoc >= 3.0  (apt install pandoc / brew install pandoc)
#   - (Opcional) reference.docx para aplicar plantilla de estilos Word
#
# Salida:
#   WirelessHeatMapper-SegundoPeriodo.docx  (en la carpeta actual)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONSOLIDADO_DIR="$SCRIPT_DIR/../CONSOLIDADO"
OUTPUT="$SCRIPT_DIR/WirelessHeatMapper-SegundoPeriodo.docx"

# ─────────────────────────────────────────────────────────────────────────────
# Archivos del Capítulo 1 (contenido del primer período reutilizado)
# ─────────────────────────────────────────────────────────────────────────────
CAP1_FILES=(
  "$CONSOLIDADO_DIR/01-portada.md"
  "$SCRIPT_DIR/cap1-encabezado.md"
  "$CONSOLIDADO_DIR/03-introduccion.md"
  "$CONSOLIDADO_DIR/04-antecedentes.md"
  "$CONSOLIDADO_DIR/05-descripcion-problema.md"
  "$CONSOLIDADO_DIR/06-situacion-problematica.md"
  "$CONSOLIDADO_DIR/07-situacion-deseada.md"
  "$CONSOLIDADO_DIR/08-objetivos.md"
  "$CONSOLIDADO_DIR/09-alcance.md"
  "$CONSOLIDADO_DIR/10-tecnologia.md"
  "$CONSOLIDADO_DIR/11-cronograma.md"
  "$CONSOLIDADO_DIR/12-proceso-scrum.md"
  "$CONSOLIDADO_DIR/13-sprint-0.md"
  "$CONSOLIDADO_DIR/14-sprint-1-planificacion.md"
  "$CONSOLIDADO_DIR/15-sprint-1-hu.md"
  "$CONSOLIDADO_DIR/16-sprint-1-diseno-uml.md"
  "$CONSOLIDADO_DIR/17-sprint-1-diseno-ui.md"
  "$CONSOLIDADO_DIR/18-sprint-1-implementacion.md"
  "$CONSOLIDADO_DIR/19-sprint-1-review.md"
  "$CONSOLIDADO_DIR/20-sprint-1-retrospective.md"
)

# ─────────────────────────────────────────────────────────────────────────────
# Archivos del Capítulo 2 — Fundamentación Teórica
# ─────────────────────────────────────────────────────────────────────────────
CAP2_FILES=(
  "$SCRIPT_DIR/cap2-encabezado.md"
  "$SCRIPT_DIR/cap2-01-fundamentos-wifi.md"
  "$SCRIPT_DIR/cap2-02-propagacion-rf.md"
  "$SCRIPT_DIR/cap2-03-metricas-cobertura.md"
  "$SCRIPT_DIR/cap2-04-site-survey.md"
  "$SCRIPT_DIR/cap2-05-interpolacion-heatmap.md"
  "$SCRIPT_DIR/cap2-06-ia-optimizacion.md"
)

# ─────────────────────────────────────────────────────────────────────────────
# Archivos del Capítulo 3 — Fundamentación Tecnológica
# ─────────────────────────────────────────────────────────────────────────────
CAP3_FILES=(
  "$SCRIPT_DIR/cap3-encabezado.md"
  "$SCRIPT_DIR/cap3-01-arquitectura-rest.md"
  "$SCRIPT_DIR/cap3-02-flutter-dart.md"
  "$SCRIPT_DIR/cap3-03-fastapi-python.md"
  "$SCRIPT_DIR/cap3-04-postgresql.md"
  "$SCRIPT_DIR/cap3-05-react-typescript.md"
  "$SCRIPT_DIR/cap3-06-docker-nginx.md"
  "$SCRIPT_DIR/cap3-07-jwt-seguridad.md"
  "$SCRIPT_DIR/cap3-08-scikit-ml.md"
)

# ─────────────────────────────────────────────────────────────────────────────
# Sección final: bibliografía y anexos
# ─────────────────────────────────────────────────────────────────────────────
CLOSING_FILES=(
  "$SCRIPT_DIR/bibliografia-actualizada.md"
  "$CONSOLIDADO_DIR/22-anexos.md"
)

# ─────────────────────────────────────────────────────────────────────────────
# Construcción del documento
# ─────────────────────────────────────────────────────────────────────────────
ALL_FILES=(
  "${CAP1_FILES[@]}"
  "${CAP2_FILES[@]}"
  "${CAP3_FILES[@]}"
  "${CLOSING_FILES[@]}"
)

echo "▶  Verificando archivos..."
MISSING=0
for f in "${ALL_FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "  ✗ No encontrado: $f"
    MISSING=$((MISSING + 1))
  fi
done

if [[ $MISSING -gt 0 ]]; then
  echo "Error: $MISSING archivo(s) no encontrado(s). Abortando." >&2
  exit 1
fi
echo "  ✓ Todos los archivos verificados (${#ALL_FILES[@]} archivos)"

echo "▶  Generando $OUTPUT..."

# Opción 1: con plantilla de referencia Word (si existe)
if [[ -f "$SCRIPT_DIR/reference.docx" ]]; then
  pandoc \
    --from=markdown+smart \
    --to=docx \
    --output="$OUTPUT" \
    --reference-doc="$SCRIPT_DIR/reference.docx" \
    --toc \
    --toc-depth=3 \
    "${ALL_FILES[@]}"
else
  # Opción 2: sin plantilla (usa estilos por defecto de pandoc)
  pandoc \
    --from=markdown+smart \
    --to=docx \
    --output="$OUTPUT" \
    --toc \
    --toc-depth=3 \
    "${ALL_FILES[@]}"
fi

echo "✓ Documento generado: $OUTPUT"
