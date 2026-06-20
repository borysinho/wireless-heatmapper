# 06 — Flujos de Experiencia de Usuario

## 1. Principios

- La app móvil continúa siendo cliente delgado; formularios, inventario y escenarios se persisten inmediatamente en el backend.
- El técnico puede guardar borradores incompletos, pero recibe bloqueos claros antes de optimizar.
- La interfaz utiliza “BSSID detectado”, “radio” y “AP físico” con significados distintos.
- Todo resultado proyectado lleva la etiqueta **Estimación**, nunca “medición”.

## 2. Flujo de instalación nueva

1. Seleccionar “Instalación nueva”.
2. Definir áreas objetivo y perfil de servicio.
3. Registrar el AP temporal y su configuración por radio.
4. Marcar su posición, altura y orientación.
5. Capturar puntos para 2,4 y/o 5 GHz.
6. Repetir con otras posiciones temporales si es necesario.
7. Completar materiales, atenuaciones y restricciones de montaje.
8. Revisar completitud y supuestos.
9. Solicitar alternativas.
10. Comparar mapas por banda, configuración y costo.

## 3. Flujo de red existente

1. Seleccionar “Optimizar red existente”.
2. Ver BSSID detectados agrupados provisionalmente por banda/SSID.
3. Crear o importar APs físicos.
4. Arrastrar/asociar cada BSSID a su radio y AP correspondientes.
5. Confirmar posición y configuración actual.
6. Marcar APs fijos, movibles o retirables.
7. Definir áreas, clientes y restricciones.
8. Validar inventario y generar alternativas.
9. Revisar acciones `antes → después` por AP.

## 4. Pantallas propuestas

| Pantalla                 | Contenido principal                                                     |
| ------------------------ | ----------------------------------------------------------------------- |
| Tipo de optimización     | Instalación nueva o red existente                                       |
| Requisitos RF            | Áreas objetivo, aplicaciones, densidad, bandas, roaming y presupuesto   |
| Inventario de APs        | APs físicos, estado, posición y completitud                              |
| Editor de radios         | BSSID, banda, canal, ancho, potencia, RRM/DFS y antena                   |
| Caracterización del plano | Muros, materiales, pérdidas y zonas permitidas                         |
| Revisión de entradas     | Bloqueos, advertencias y supuestos                                       |
| Alternativas             | Cobertura, costo, confianza, APs y cambios                              |
| Detalle del escenario    | Plan sobre plano y configuración por radio                              |
| Comparación              | Observado/proyectado/diferencia por 2,4 GHz y 5 GHz                     |

## 5. Visualización por banda

La comparación contiene pestañas:

- `2,4 GHz`;
- `5 GHz`;
- `Combinado`, solo si existe política;
- `Diferencia`.

Al tocar una celda o punto se muestran RSSI observado, proyectado, delta, radio primaria, radio secundaria e incertidumbre.

## 6. Representación de un AP propuesto

Cada AP muestra una ficha compacta:

```text
AP-04 · MOVER · 6,2 m
Modelo: catálogo/modelo aprobado
Montaje: techo, 2,8 m
2,4 GHz: canal 1 · 20 MHz · 8 dBm
5 GHz: canal 44 · 20 MHz · 14 dBm
Impacto: +18 % cobertura 5 GHz
Confianza: media (antena asumida)
```

## 7. Prevención de errores

- Advertir cuando dos BSSID posiblemente pertenecen al mismo AP, sin asociarlos automáticamente como hecho.
- No permitir introducir “50 %” de potencia sin conocer el máximo o conservarlo como valor no normalizado.
- Confirmar dominio regulatorio antes de ofrecer canales/DFS.
- Mostrar que una señal fuerte en 2,4 GHz no demuestra cobertura suficiente en 5 GHz.
- Evitar que la acción “aplicar escenario” sugiera configuración automática; en esta versión genera un plan técnico.

