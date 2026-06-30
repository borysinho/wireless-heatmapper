#!/usr/bin/env bash
set -euo pipefail

OUT="WirelessHeatMapper-Consolidado.docx"
MERGED="_merged.md"

# Orden de concatenación: portada + 03..22 (omite 00-README y 02-indice)
FILES=(
  01-portada.md
  03-introduccion.md
  04-antecedentes.md
  05-descripcion-problema.md
  06-situacion-problematica.md
  07-situacion-deseada.md
  08-objetivos.md
  09-alcance.md
  10-tecnologia.md
  11-cronograma.md
  12-proceso-scrum-definiciones.md
  13-sprint-0-definicion-inicial.md
  14-sprint-1-planning.md
  15-sprint-1-historias-usuario.md
  16-sprint-1-sprint-backlog.md
  17-sprint-1-patron-desarrollo.md
  18-sprint-1-ejecucion.md
  19-sprint-1-review.md
  20-sprint-1-retrospective.md
  21-bibliografia.md
  22-anexos.md
)

# Concatenar con separador y filtrar:
#  - Bloques ```plantuml ... ```
#  - Bloques ```mermaid ... ```
#  - Líneas de pie de figura: "> *Figura ...*" (1 línea)
#  - Comentario "AGREGAR PROTOTIPOS/INTERFACES"
> "$MERGED"
for f in "${FILES[@]}"; do
  awk '
    BEGIN { in_diag = 0 }
    /^```(plantuml|mermaid|@startuml|@startgantt)/ { in_diag = 1; next }
    in_diag && /^```/ { in_diag = 0; next }
    in_diag { next }
    /^> \*Figura [0-9]+:/ { next }
    /\*\*AGREGAR PROTOTIPOS\/INTERFACES\*\*/ { next }
    { print }
  ' "$f" >> "$MERGED"
  printf '\n\n' >> "$MERGED"
done

pandoc "$MERGED" \
  --from=gfm+yaml_metadata_block \
  --to=docx \
  --output="$OUT" \
  --toc \
  --toc-depth=3 \
  --metadata title="Wireless HeatMapper — Sprint 0 + Sprint 1" \
  --metadata author="Jhasmany J. Fernandez Ortega · Herland B. Quiroga Flores (Grupo 24 — FICCT-UAGRM)" \
  --metadata lang=es-BO \
  --reference-doc=_apa-reference.docx 2>/dev/null || \
pandoc "$MERGED" \
  --from=gfm \
  --to=docx \
  --output="$OUT" \
  --toc \
  --toc-depth=3 \
  --metadata title="Wireless HeatMapper — Sprint 0 + Sprint 1" \
  --metadata author="Jhasmany J. Fernandez Ortega · Herland B. Quiroga Flores (Grupo 24 — FICCT-UAGRM)" \
  --metadata lang=es-BO

echo "OK -> $OUT ($(du -h "$OUT" | cut -f1))"
