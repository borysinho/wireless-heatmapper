"""Genera artefacto reproducible del baseline RF de Sprint 5.

La recomendación vigente calibra `ModeloPropagacion` por plano cuando existen
mediciones reales vinculadas a APs ubicados. Este script conserva un payload
sintético reproducible solo como respaldo documental del baseline FSPL, sin
entrenar un modelo global ni introducir dependencias externas al stack base.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.ai.modelo_propagacion import generar_dataset_sintetico


def main() -> None:
    destino = Path(__file__).resolve().parent / "models" / "optimizador_ap.joblib"
    destino.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tipo": "baseline_fspl",
        "descripcion": "FSPL/log-distance con dataset sintético reproducible.",
        "dataset": generar_dataset_sintetico(),
    }
    destino.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(destino)


if __name__ == "__main__":
    main()
