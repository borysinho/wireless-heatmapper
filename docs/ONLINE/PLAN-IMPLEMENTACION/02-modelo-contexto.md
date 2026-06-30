# 02 — Modelo de Contexto (modalidad online)

**Referencia:** PAPS Online §6, §7 · Enfoque Scrum v3.2 — modelos obligatorios por Sprint  
**Notación:** UML 2.5 (Casos de Uso)  
**Estado:** actualizado contra implementación real al 29-jun-2026

---

## 1. Propósito

El **modelo de contexto** delimita el alcance funcional vigente del sistema mostrando qué hace y con quién interactúa. En la modalidad 100 % en línea, todos los casos de uso del cliente móvil y de la web son mediados por el backend FastAPI; no existe ningún caso de uso que opere sobre estado local persistente.

Este modelo refleja el refinamiento aprobado en [18-reglas-gobernanza-conjuntos-ap-heatmaps.md](18-reglas-gobernanza-conjuntos-ap-heatmaps.md): no hay diagnóstico persistido, no hay exportación PDF desde el sistema y la propuesta IA se modela como conjuntos AP derivados.

## 2. Actores

| Id  | Actor                         | Tipo            | Descripción                                                                                                 |
| --- | ----------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------- |
| A1  | Técnico de campo              | Humano          | Usuario principal de la app móvil. Realiza relevamiento WiFi, planos, capturas, conjuntos AP y heatmaps.    |
| A2  | Administrador (Bulldog Tech.) | Humano          | Usuario del panel web. Gestiona usuarios, clientes, proyectos, propuestas IA y enlaces cliente.             |
| A3  | Cliente / Stakeholder         | Humano          | Accede al portal web mediante enlace único y consulta solo el contenido publicado explícitamente.            |
| A4  | Android WifiManager API       | Sistema externo | Provee al móvil resultados de escaneo: RSSI, SSID, BSSID, canal y frecuencia.                               |
| A5  | Servicio IA (interno backend) | Componente      | Motor backend que genera conjuntos AP derivados y heatmaps proyectados desde mediciones y restricciones RF. |

> No se considera "almacenamiento local" como actor: en esta modalidad no existe persistencia local de dominio.

## 3. Diagrama de casos de uso

```plantuml
@startuml
title Modelo de Contexto — Wireless HeatMapper (modalidad 100 % en línea)\nCasos de Uso vigentes al 29-jun-2026
left to right direction
skinparam packageStyle rectangle
skinparam actorBackgroundColor #EBF5FB
skinparam actorBorderColor #2980B9
skinparam usecaseBackgroundColor #FDFEFE
skinparam usecaseBorderColor #2980B9
skinparam rectangleBackgroundColor #FAFAFA
skinparam rectangleBorderColor #BDC3C7
skinparam arrowColor #5D6D7E
skinparam noteBackgroundColor #FFFDE7

actor "Técnico\nde Campo" as tech #LightBlue
actor "Administrador\n(Bulldog Tech.)" as admin #LightSteelBlue
actor "Cliente /\nStakeholder" as client #LightCoral
actor "Android\nWifiManager API" as wifi #LightGreen
actor "Servicio IA\n(backend)" as ia #LightYellow

rectangle "Wireless HeatMapper (Backend FastAPI + App móvil + Web)" {
  usecase "UC11\nAutenticar\nUsuario" as UC11
  usecase "UC13\nGestionar Usuarios\n(Admin Web)" as UC13
  usecase "UC19\nGestionar Clientes\n(Admin Web)" as UC19
  usecase "UC18\nVer Proyectos de\nla Organización" as UC18
  usecase "UC01\nGestionar Proyecto\nde Survey" as UC01
  usecase "UC12\nVer Historial\nde Proyectos" as UC12

  usecase "UC02\nImportar Plano\n(subida al backend)" as UC02
  usecase "UC03\nCalibrar Escala\ndel Plano" as UC03

  usecase "UC04\nMarcar Punto\nde Medición" as UC04
  usecase "UC05\nCapturar Señales WiFi\n(envío en línea)" as UC05

  usecase "UC06\nGenerar Mapa de Calor\n(conjuntos AP + IDW backend)" as UC06

  usecase "UC08\nObtener Recomendaciones\nde APs (IA)" as UC08
  usecase "UC09\nComparar Actual vs\nPropuesta IA" as UC09

  usecase "UC15\nGenerar Enlace\nde Cliente" as UC15
  usecase "UC16\nVer Heatmap\nInteractivo (Web)" as UC16
  usecase "UC17\nVer Conjuntos y\nPlan AP (Web)" as UC17
}

tech --> UC11
tech --> UC01
tech --> UC02
tech --> UC03
tech --> UC04
tech --> UC05
tech --> UC06
tech --> UC12

admin --> UC11
admin --> UC13
admin --> UC18
admin --> UC19
admin --> UC08
admin --> UC09
admin --> UC15

client --> UC16
client --> UC17

UC01 ..> UC19 : <<include>>\n(selector de cliente)
UC04 ..> UC05 : <<include>>
UC05 -- wifi
UC06 ..> UC04 : <<requires>>\n(5+ puntos)
UC08 -- ia
UC09 ..> UC08 : <<extend>>
UC15 ..> UC16 : <<include>>
UC16 ..> UC17 : <<include>>

note bottom of UC05
  Cada lote de escaneo viaja por HTTPS
  al backend. El cliente móvil no almacena
  muestras entre sesiones.
end note

note bottom of UC06
  La interpolación IDW se ejecuta en backend.
  El cliente solo solicita y renderiza mapa,
  matriz, escala y metadatos de APs.
end note

note bottom of UC08
  La IA está restringida al backend/panel web.
  La salida se persiste como conjunto_ap
  de origen ia, derivado de un conjunto técnico.
end note

note bottom of UC15
  El enlace contiene conjunto_ids y mapa_ids.
  Esa selección explícita define la visibilidad
  del cliente en el portal.
end note
@enduml
```

> **UC eliminados:** UC07 (diagnóstico persistido), UC10 (reporte PDF) y UC14 (sincronización offline) no forman parte del alcance vigente. Sus entidades y endpoints fueron podados de la implementación.

## 4. Trazabilidad UC ↔ RP

| Caso de uso                                     | Requerimiento Principal | Sprint | Estado         |
| ----------------------------------------------- | ----------------------- | ------ | -------------- |
| UC01 Gestionar proyecto                         | RP8                     | 1      | Implementado   |
| UC02 Importar plano                             | RP2                     | 2      | Implementado   |
| UC03 Calibrar escala                            | RP2                     | 2      | Implementado   |
| UC04 Marcar punto                               | RP2                     | 3      | Implementado   |
| UC05 Capturar señales WiFi                      | RP1                     | 3      | Implementado   |
| UC06 Generar heatmap                            | RP3                     | 4      | Implementado   |
| UC08 Recomendaciones IA                         | RP5                     | 5      | Implementado   |
| UC09 Comparar actual vs propuesta IA            | RP5                     | 5      | Implementado   |
| UC11 Autenticar                                 | RP8                     | 1      | Implementado   |
| UC12 Historial de proyectos                     | RP8                     | 1      | Implementado   |
| UC13 Gestionar usuarios (admin)                 | RP7                     | 1      | Implementado   |
| UC15 Generar enlace de cliente                  | RP9                     | 6      | Implementado   |
| UC16 Ver heatmap web (cliente)                  | RP9                     | 6      | Implementado   |
| UC17 Ver conjuntos y plan AP (cliente)          | RP9                     | 6      | Implementado   |
| UC18 Ver proyectos de la organización           | RP7                     | 1      | Implementado   |
| UC19 Gestionar clientes (admin)                 | RP7                     | 1      | Implementado   |
| UC07 Analizar cobertura persistida              | RP4                     | —      | Eliminado      |
| UC10 Exportar reporte PDF                       | RP6                     | —      | Eliminado      |
| UC14 Sincronizar proyecto offline con servidor  | —                       | —      | Eliminado      |

> **Mapeo RP autoritativo:** [PAPS Online §7](../Wireless%20Heatmapper%20-%20PAPS%20-%20Modalidad%20Online.md). RP4 y RP6 se conservan como requerimientos históricos del PAPS, pero quedan sin HU activa por refinamiento de alcance.
