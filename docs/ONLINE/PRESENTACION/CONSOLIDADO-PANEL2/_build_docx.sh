#!/usr/bin/env bash
# =============================================================================
# _build_docx.sh — Script de construcción del documento Panel 2
# Wireless HeatMapper · Ingeniería de Software II · Grupo 24 · Mayo 2026
# =============================================================================
# Uso:
#   cd docs/ONLINE/PRESENTACION/CONSOLIDADO-PANEL2
#   bash _build_docx.sh
#
# Requisitos: pandoc >= 3.0
#   Instalar: apt install pandoc   /   brew install pandoc
#
# Salida: WirelessHeatMapper-Panel2.docx (en esta misma carpeta)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="$SCRIPT_DIR"

OUTPUT="$BASE/WirelessHeatMapper-Panel2.docx"

echo "========================================================"
echo "  Wireless HeatMapper — Build Panel 2"
echo "  Fecha: $(date '+%d/%m/%Y %H:%M')"
echo "========================================================"

# Verificar pandoc
if ! command -v pandoc &>/dev/null; then
  echo "[ERROR] pandoc no está instalado."
  echo "        Instalar: apt install pandoc  /  brew install pandoc"
  exit 1
fi

echo "[1/7] Reuniendo archivos fuente..."

# =============================================================================
# PORTADA (CONSOLIDADO-PANEL2)
# =============================================================================
PORTADA="$BASE/01-portada.md"

# =============================================================================
# CAPÍTULO I — Definición del Proyecto
# Secciones 1-8: desde CONSOLIDADO (contenido sin cambios respecto al Panel 1)
# Sección 9 (cronograma): versión actualizada con Sprint 2 y Sprint 3
# =============================================================================
CAP1_HEADER="$BASE/cap1-encabezado-tmp.md"
cat > "$CAP1_HEADER" << 'EOF'
---

# CAPITULO I. DEFINICIÓN DEL PROYECTO

EOF

CAP1_PARTES=(
  "$BASE/03-introduccion.md"
  "$BASE/04-antecedentes.md"
  "$BASE/05-descripcion-problema.md"
  "$BASE/06-situacion-problematica.md"
  "$BASE/07-situacion-deseada.md"
  "$BASE/08-objetivos.md"
  "$BASE/09-alcance.md"
  "$BASE/10-tecnologia.md"
  "$BASE/07-cap1-cronograma-actualizado.md"
)

# =============================================================================
# CAPÍTULO II — Fundamentos Teóricos de Redes Inalámbricas IEEE 802.11
# Desde CONSOLIDADO-CAPITULOS
# =============================================================================
CAP2_PARTES=(
  "$BASE/cap2-encabezado.md"
  "$BASE/cap2-01-fundamentos-wifi.md"
  "$BASE/cap2-02-propagacion-rf.md"
  "$BASE/cap2-03-metricas-cobertura.md"
  "$BASE/cap2-04-site-survey.md"
  "$BASE/cap2-05-interpolacion-heatmap.md"
  "$BASE/cap2-06-ia-optimizacion.md"
)

# =============================================================================
# CAPÍTULO III — Arquitectura Técnica del Sistema Wireless HeatMapper
# Desde CONSOLIDADO-CAPITULOS
# =============================================================================
CAP3_PARTES=(
  "$BASE/cap3-encabezado.md"
  "$BASE/cap3-01-arquitectura-rest.md"
  "$BASE/cap3-02-flutter-dart.md"
  "$BASE/cap3-03-fastapi-python.md"
  "$BASE/cap3-04-postgresql.md"
  "$BASE/cap3-05-react-typescript.md"
  "$BASE/cap3-06-docker-nginx.md"
  "$BASE/cap3-07-jwt-seguridad.md"
  "$BASE/cap3-08-scikit-ml.md"
)

# =============================================================================
# CAPÍTULO IV — Proceso de Desarrollo Scrum (Sprint 2 y Sprint 3)
# Desde CONSOLIDADO-PANEL2 (nuevos archivos)
# =============================================================================
CAP4_HEADER="$BASE/cap4-encabezado-tmp.md"
cat > "$CAP4_HEADER" << 'EOF'
---

# CAPITULO IV. PROCESO DE DESARROLLO SCRUM

EOF

CAP4_PARTES=(
  "$BASE/cap4-sprint2.md"
  "$BASE/cap4-sprint3.md"
)

# =============================================================================
# BIBLIOGRAFÍA
# Desde CONSOLIDADO-CAPITULOS
# =============================================================================
BIBLIO="$BASE/bibliografia-actualizada.md"

# =============================================================================
# ANEXOS
# Anexo A — Sprint 0: Definición Inicial
# Anexo B — Sprint 1: Fundación Backend + Admin + Auth Móvil
# Resto de anexos (cartas, diagramas, etc.)
# =============================================================================
ANEXOS_HEADER="$BASE/anexos-header-tmp.md"
cat > "$ANEXOS_HEADER" << 'EOF'
---

# Anexos

## Anexo A. Sprint 0

EOF

ANEXO_S0=(
  "$BASE/13-sprint-0-definicion-inicial.md"
)

ANEXO_S1_HEADER="$BASE/anexo-s1-header-tmp.md"
cat > "$ANEXO_S1_HEADER" << 'EOF'

---

## Anexo B. Sprint 1

EOF

ANEXO_S1=(
  "$BASE/14-sprint-1-planning.md"
  "$BASE/15-sprint-1-historias-usuario.md"
  "$BASE/16-sprint-1-sprint-backlog.md"
  "$BASE/17-sprint-1-patron-desarrollo.md"
  "$BASE/18-sprint-1-ejecucion.md"
  "$BASE/19-sprint-1-review.md"
  "$BASE/20-sprint-1-retrospective.md"
)

ANEXO_OTROS=(
  "$BASE/22-anexos.md"
)

# =============================================================================
# Verificar que todos los archivos existen
# =============================================================================
echo "[2/7] Verificando archivos fuente..."

ALL_FILES=(
  "$PORTADA"
  "${CAP1_PARTES[@]}"
  "${CAP2_PARTES[@]}"
  "${CAP3_PARTES[@]}"
  "${CAP4_PARTES[@]}"
  "$BIBLIO"
  "${ANEXO_S0[@]}"
  "${ANEXO_S1[@]}"
)

MISSING=0
for f in "${ALL_FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "  [AVISO] Archivo no encontrado: $f"
    MISSING=$((MISSING + 1))
  fi
done

if [[ $MISSING -gt 0 ]]; then
  echo "  [AVISO] $MISSING archivo(s) faltante(s). Se omitirán del documento."
fi

# =============================================================================
# Construir lista de archivos para pandoc (solo los que existen)
# =============================================================================
echo "[3/7] Construyendo lista de fuentes..."

SOURCES=()

# Portada
[[ -f "$PORTADA" ]] && SOURCES+=("$PORTADA")

# Cap I
[[ -f "$CAP1_HEADER" ]] && SOURCES+=("$CAP1_HEADER")
for f in "${CAP1_PARTES[@]}"; do
  [[ -f "$f" ]] && SOURCES+=("$f")
done

# Cap II
for f in "${CAP2_PARTES[@]}"; do
  [[ -f "$f" ]] && SOURCES+=("$f")
done

# Cap III
for f in "${CAP3_PARTES[@]}"; do
  [[ -f "$f" ]] && SOURCES+=("$f")
done

# Cap IV
[[ -f "$CAP4_HEADER" ]] && SOURCES+=("$CAP4_HEADER")
for f in "${CAP4_PARTES[@]}"; do
  [[ -f "$f" ]] && SOURCES+=("$f")
done

# Bibliografía
[[ -f "$BIBLIO" ]] && SOURCES+=("$BIBLIO")

# Anexos
[[ -f "$ANEXOS_HEADER" ]] && SOURCES+=("$ANEXOS_HEADER")
for f in "${ANEXO_S0[@]}"; do
  [[ -f "$f" ]] && SOURCES+=("$f")
done
[[ -f "$ANEXO_S1_HEADER" ]] && SOURCES+=("$ANEXO_S1_HEADER")
for f in "${ANEXO_S1[@]}"; do
  [[ -f "$f" ]] && SOURCES+=("$f")
done
for f in "${ANEXO_OTROS[@]}"; do
  [[ -f "$f" ]] && SOURCES+=("$f")
done

echo "  Total de archivos fuente: ${#SOURCES[@]}"

# =============================================================================
# Ejecutar pandoc
# =============================================================================
echo "[4/7] Ejecutando pandoc..."

pandoc \
  --from markdown+raw_html+tex_math_dollars \
  --to docx \
  --standalone \
  --toc \
  --toc-depth=3 \
  --reference-doc="$BASE/reference.docx" \
  --resource-path="$BASE" \
  --metadata title="Wireless HeatMapper — Panel 2" \
  --metadata author="Fernandez Ortega Jhasmany Jhunnior; Quiroga Flores Herland Borys" \
  --metadata date="Mayo de 2026" \
  --output "$OUTPUT" \
  "${SOURCES[@]}"

# =============================================================================
# Limpiar archivos temporales
# =============================================================================
echo "[5/7] Limpiando archivos temporales..."
rm -f "$CAP1_HEADER" "$CAP4_HEADER" "$ANEXOS_HEADER" "$ANEXO_S1_HEADER"

# =============================================================================
# También generar versión HTML (útil para revisión rápida sin Word)
# =============================================================================
HTML_OUTPUT="${OUTPUT%.docx}.html"
echo "[6/7] Generando versión HTML de revisión..."

pandoc \
  --from markdown+raw_html+tex_math_dollars \
  --to html5 \
  --standalone \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --metadata title="Wireless HeatMapper — Panel 2" \
  --metadata author="Fernandez Ortega Jhasmany Jhunnior; Quiroga Flores Herland Borys" \
  --metadata date="Mayo de 2026" \
  --output "$HTML_OUTPUT" \
  "${SOURCES[@]}" 2>/dev/null || echo "  [AVISO] HTML omitido (pandoc sin soporte HTML5 o error menor)."

echo "[7/7] ¡Listo!"
echo ""
echo "  Archivo principal : $OUTPUT"
[[ -f "$HTML_OUTPUT" ]] && echo "  Revisión HTML     : $HTML_OUTPUT"
echo ""
echo "========================================================"
