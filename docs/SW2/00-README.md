# Documentacion SW2 - Wireless HeatMapper

Este directorio organiza la documentacion academica requerida para la materia Ingenieria de Software II, tomando como base el mismo producto desarrollado para Taller de Grado I y adaptandolo al alcance documental extendido de SW2.

## Estructura

| Ruta | Proposito |
| ---- | --------- |
| `01-prompts-secuenciales.md` | Prompts maestros para regenerar o actualizar cada documento individual en orden. |
| `DOCUMENTACION/` | Capitulos individuales que se consolidan en el documento final. |
| `diagramas/` | Diagramas UML 2.5+ en PlantUML. |
| `assets/` | Recursos generados para el consolidado, incluidos codigos QR. |
| `build/` | Salida temporal y documento Word generado. |
| `_build_docx.sh` | Script de consolidacion a Microsoft Word con Pandoc, PlantUML y codigos QR. |

## Criterios de uso

- Los capitulos estan redactados en lenguaje formal para presentacion academica.
- La documentacion final no referencia rutas internas del repositorio como fuente argumental.
- Los diagramas se mantienen en PlantUML para compatibilidad con UML 2.5+ y herramientas CASE.
- El consolidado se genera en formato Word mediante el script `_build_docx.sh`.
- Las URLs publicas del repositorio, frontend y releases moviles se incorporan tambien como codigos QR.

