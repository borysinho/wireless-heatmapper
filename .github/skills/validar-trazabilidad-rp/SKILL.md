---
name: validar-trazabilidad-rp
description: "Valida trazabilidad entre RP1..RP9 del PAPS Online y artefactos Scrum del Plan de Implementación vigente (F3, F4, F5 en docs/ONLINE/PLAN-IMPLEMENTACION/). Usar antes de Sprint Review, al cerrar sprint o al modificar HU/tareas para detectar huérfanos, inconsistencias y faltantes de cobertura."
argument-hint: "Opcional: Sprint objetivo (ej. sprint1) o alcance (F3,F4,F5)"
user-invocable: true
disable-model-invocation: false
---

# Skill: Validar Trazabilidad RP

## Resultado esperado

Generar un informe de trazabilidad que confirme, con evidencia en archivos del repositorio, si:

- Cada RP del PAPS Online tiene cobertura por al menos una HU.
- Cada HU del Product Backlog vigente tiene relacion explicita con uno o mas RP (o se justifica como habilitador transversal).
- Las tareas del Sprint Backlog mantienen alineacion con las HU comprometidas del Sprint.
- Existen huérfanos, huecos o inconsistencias que deban corregirse.

## Cuándo usar

- Antes de cada Sprint Review (R-4).
- Al cerrar o abrir Sprint.
- Cuando se agregan/modifican HU en F3/F4.
- Cuando se actualiza F5 y se necesita verificar cobertura funcional.

## Fuentes obligatorias (plan vigente)

- docs/ONLINE/Wireless Heatmapper - PAPS - Modalidad Online.md (PAPS oficial)
- docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md (índice del plan)
- docs/ONLINE/PLAN-IMPLEMENTACION/05-product-backlog-online.md (F3 vigente)
- docs/ONLINE/PLAN-IMPLEMENTACION/08-sprint-1-...md … 13-sprint-6-...md (F4 + F5 por sprint)
- docs/ONLINE/PLAN-IMPLEMENTACION/14-trazabilidad-rp-hu.md (matriz pre-existente — punto de partida)

## Fuentes históricas (no usar para validar alcance vigente)

- docs/Wireless Heatmapper - Plan Aplicado a Proyecto de Software - PAPS.md (PAPS histórico)
- docs/SCRUM/\*\* (plan offline original, conservado como referencia)

## Procedimiento

1. Identificar universo de requerimientos

- Extraer lista completa de RP en el PAPS Online (RP1..RP9).
- Si aparecen nuevos RP fuera de esa serie, registrarlos como alerta.

2. Levantar mapa RP -> HU

- Revisar el Product Backlog vigente (`05-product-backlog-online.md`) y detectar HU que cubren cada RP por descripcion funcional.
- Validar que la cobertura no sea ambigua: cada RP debe mapear a HU concretas.
- Si una HU impacta varios RP, conservar mapeo many-to-many.
- HU habilitadoras (PB-09, PB-13, PB-18) sin RP asignado deben justificarse como transversales.

3. Validar HU detalladas del Sprint (F4)

- Comprobar que las HU detalladas en cada archivo de sprint (`08-..` a `13-..`) existan en el Product Backlog vigente con el mismo ID PB.
- Verificar que criterios de aceptacion mantengan coherencia con RP mapeados.
- Marcar diferencias de alcance entre F3 y F4.

4. Validar ejecucion en Sprint Backlog (F5)

- Confirmar que las HU comprometidas en el F5 del sprint pertenezcan al Sprint declarado.
- Verificar que tareas `Sp{N}-NN` de cada HU tengan relacion directa con la HU correspondiente.
- Marcar tareas sin HU o HU sin tareas cuando corresponda.

5. Detectar inconsistencias de trazabilidad

- RP sin HU asociada.
- HU sin RP asociado y sin justificación de habilitador transversal.
- HU en F4 no presentes en el Product Backlog vigente.
- HU en F5 fuera del Sprint declarado o no comprometidas.
- Cambios de alcance no reflejados entre PAPS Online, F3 vigente, F4 y F5.
- Reapariciones de PB-14 (sincronización offline) — debe permanecer eliminada.

6. Emitir reporte final

- Presentar tabla de cobertura minima:
  - RP
  - HU asociadas (PB)
  - Evidencia (archivo)
  - Estado (OK / Parcial / Falta)
- Incluir lista de hallazgos priorizada por severidad:
  - Alto: rompe trazabilidad o invalida alcance del Sprint.
  - Medio: cobertura parcial o ambigua.
  - Bajo: mejoras de redaccion/consistencia.
- Cerrar con acciones recomendadas y archivo a corregir.

## Reglas de decision

- Si un RP no tiene HU asociada en F3: estado Falta (severidad Alta).
- Si una HU aparece en F4/F5 pero no existe en F3: severidad Alta.
- Si una tarea Sp-NN no se puede vincular a PB del Sprint: severidad Media.
- Si el mapeo existe pero es ambiguo por redaccion: severidad Media.
- Si solo hay desalineacion menor de texto sin afectar alcance: severidad Baja.

## Checklist de calidad

- Se revisaron PAPS Online, Product Backlog vigente, F4 y F5 del Sprint activo.
- Se validaron todos los RP del universo objetivo.
- Se reportaron huérfanos y faltantes con evidencia concreta.
- Se clasificaron hallazgos por severidad.
- Se propusieron acciones concretas de correccion sobre archivos del plan vigente.

## Formato sugerido de salida

1. Resumen ejecutivo

- Cobertura total: X/Y RP cubiertos.
- HU huérfanas: N.
- Tareas sin trazabilidad: N.

2. Hallazgos

- Lista ordenada por severidad con archivo donde se detecta.

3. Matriz de trazabilidad

- Tabla RP -> HU -> Tareas (si aplica) -> Estado.

4. Acciones recomendadas

- Correcciones puntuales por archivo.
- Validacion sugerida antes del siguiente R-4.

## Restricciones del proyecto

- Mantener nomenclatura oficial: RP1..RP9, PB-XX, Sp{N}-NN.
- No renombrar IDs existentes durante la validacion.
- Preservar idioma espanol en reportes y recomendaciones.
- No duplicar contenido del PAPS Online en el plan; enlazar cuando corresponda.
- No usar el plan histórico [docs/SCRUM/](../../../docs/SCRUM/00-indice.md) como fuente de alcance vigente.
- Convenciones generales del proyecto en [AGENTS.md](../../../AGENTS.md).
