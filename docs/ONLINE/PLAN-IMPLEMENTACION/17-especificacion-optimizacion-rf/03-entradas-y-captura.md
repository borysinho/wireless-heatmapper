# 03 — Entradas y Captura

## 1. Principio de procedencia

Cada entrada debe indicar su procedencia:

- `DETECTADA_ANDROID`: obtenida del escaneo móvil;
- `INGRESADA_TECNICO`: declarada manualmente;
- `CATALOGO_FABRICANTE`: tomada de una ficha validada;
- `CONTROLADOR`: importada desde infraestructura existente;
- `ESTIMADA_MOTOR`: valor supuesto por el sistema.

Los valores estimados se muestran como supuestos y reducen la confianza del escenario.

## 2. Datos obtenidos durante la medición

Se conservan RSSI, SSID, BSSID, canal, frecuencia, coordenada y fecha. Cuando Android y el dispositivo lo permitan, se añaden:

- ancho de canal reportado;
- capacidades/estándares anunciados;
- cantidad de muestras, mínimo, máximo, promedio y desviación;
- ruido o SNR, marcados como estimados si no provienen de un analizador confiable.

El escaneo Android no sustituye un analizador de espectro y no puede descubrir de forma confiable la potencia configurada, la antena ni el AP físico que agrupa varios BSSID.

## 3. Ficha obligatoria por AP físico

| Dato                         | Nueva instalación | Red existente | Obligación para alta confianza |
| ---------------------------- | ----------------- | ------------- | ------------------------------ |
| Fabricante y modelo          | Sí                | Sí            | Obligatorio                    |
| Posición X/Y y planta        | AP temporal       | AP existente  | Obligatorio                    |
| Altura y tipo de montaje     | Sí                | Sí            | Obligatorio                    |
| Movible/fijo/retirable       | No aplica         | Sí            | Obligatorio en escenario B     |
| Costo referencial            | Sí                | Opcional      | Requerido para optimizar costo |
| Restricción de cableado/PoE  | Sí                | Sí            | Requerido si limita posiciones |

## 4. Ficha obligatoria por radio

| Dato                         | Unidad/valores                                  |
| ---------------------------- | ------------------------------------------------ |
| Banda                        | `2_4_GHZ`, `5_GHZ`                              |
| BSSID y SSID asociados       | Lista verificada                                |
| Canal y ancho                | Canal; 20/40/80 MHz según capacidad             |
| Potencia configurada         | Valor original + mW/dBm/%                       |
| Referencia de potencia       | IR, EIRP o desconocida                          |
| Potencia máxima y niveles    | dBm normalizados                                |
| Gestión RF                   | Estática, RRM o TPC                             |
| DFS y canales permitidos     | Según equipo, clientes y región                 |
| Radio habilitada             | Sí/no                                           |
| Cantidad de SSID anunciados  | Para estimar sobrecarga                         |

La interfaz convierte mW a dBm, calcula EIRP cuando existen ganancia y pérdidas, y conserva el valor original para auditoría.

## 5. Ficha de antena y montaje

- interna o externa;
- fabricante/modelo, tipo y ganancia dBi;
- patrón de azimut/elevación o beamwidth horizontal/vertical;
- orientación y tilt;
- pérdidas de cable y conectores;
- polarización si el catálogo la especifica.

Si se desconoce la antena, puede usarse una omni de 2,14 dBi como supuesto inicial, claramente rotulado y con mayor incertidumbre.

## 6. Datos del ambiente

Estos datos pertenecen al plano o proyecto, no a un AP:

- escala calibrada y áreas excluidas;
- paredes/obstáculos con material, espesor opcional y atenuación por banda;
- atenuaciones medidas mediante _spot checks_;
- pisos alineados y pérdida entre plantas;
- ocupación baja/típica/pico;
- fuentes de interferencia conocidas;
- ruido por zona y banda cuando exista medición confiable;
- posiciones permitidas/prohibidas para montaje.

## 7. Perfil de servicio y restricciones

- áreas objetivo y criticidad;
- aplicaciones y RSSI/SNR objetivo;
- usuarios y dispositivos simultáneos por zona;
- necesidad de roaming y cobertura secundaria;
- clientes solo 2,4 GHz, dual-band o restricciones DFS;
- presupuesto, máximo de APs y modelos permitidos;
- preferencia entre cobertura, 5 GHz, menor costo o menores cambios.

## 8. Validación previa a optimizar

El backend calcula un reporte de completitud:

| Nivel   | Condición resumida                                                                    |
| ------- | ------------------------------------------------------------------------------------- |
| Alto    | Escala, ambiente, inventario, potencia, antena, bandas y áreas objetivo completos    |
| Medio   | Existen supuestos documentados que permiten predecir con advertencias                 |
| Bajo    | Falta escala, potencia/configuración de AP temporal o relación BSSID-radio            |

Con nivel bajo se permite guardar un borrador, pero no presentarlo como plan definitivo.

