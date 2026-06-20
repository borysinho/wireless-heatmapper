# 02 — Modelo de Contexto (modalidad online)

**Referencia:** PAPS Online §6, §7 · Enfoque Scrum v3.2 — modelos obligatorios por Sprint
**Notación:** UML 2.5 (Casos de Uso)

---

## 1. Propósito

El **modelo de contexto** delimita el alcance funcional del sistema mostrando qué hace (casos de uso) y con quién interactúa (actores). En la modalidad 100 % en línea, todos los casos de uso del cliente móvil y de la web son **mediados por el backend FastAPI**: no existe ningún caso de uso que opere sobre estado local persistente.

## 2. Actores

| Id  | Actor                         | Tipo            | Descripción                                                                          |
| --- | ----------------------------- | --------------- | ------------------------------------------------------------------------------------ |
| A1  | Técnico de campo              | Humano          | Usuario principal de la app móvil. Realiza el relevamiento WiFi en sitio.            |
| A2  | Administrador (Bulldog Tech.) | Humano          | Usuario del panel web. Gestiona técnicos y supervisa proyectos de la organización.   |
| A3  | Cliente / Stakeholder         | Humano          | Recibe el reporte y accede al portal web mediante enlace único.                      |
| A4  | Android WifiManager API       | Sistema externo | Provee al móvil el resultado de los escaneos (RSSI, SSID, BSSID, canal, frecuencia). |
| A5  | Servicio IA (interno backend) | Componente      | Modelo de ML hospedado en el backend; expuesto vía REST.                             |

> No se considera "almacenamiento local" como actor: en esta modalidad no existe.

## 3. Diagrama de casos de uso

```plantuml
@startuml
title Modelo de Contexto — Wireless HeatMapper (modalidad 100 % en línea)\nDiagrama de Casos de Uso (UML 2.5)
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
  ' ── Sprint 1 — IMPLEMENTADO ──────────────────────────────────────────────
  ' UC11: POST /api/auth/login|refresh|logout · LoginPage (Flutter) · LoginAdmin.tsx
  usecase "UC11\nAutenticar\nUsuario" as UC11
  ' UC13: POST|GET|PATCH /api/admin/usuarios · GestionUsuarios.tsx + UsuarioModal.tsx
  usecase "UC13\nGestionar Usuarios\n(Admin Web)" as UC13
  ' UC19: POST|GET|PUT|PATCH /api/admin/clientes · GestionClientes.tsx
  usecase "UC19\nGestionar Clientes\n(Admin Web)" as UC19
  ' UC18: GET /api/admin/proyectos + PATCH archivar/reasignar · ListadoProyectosOrg.tsx
  usecase "UC18\nVer Proyectos de\nla Organización" as UC18
  ' UC01: GET|POST|PUT|PATCH|DELETE /api/proyectos · ProyectoFormPage + ProyectosPage (Flutter)
  usecase "UC01\nGestionar Proyecto\nde Survey" as UC01
  ' UC12: GET /api/proyectos?estado=archivado · ProyectosPage con búsqueda y filtro (Flutter)
  usecase "UC12\nVer Historial\nde Proyectos" as UC12

  ' ── Sprint 2 — Pendiente ──────────────────────────────────────────────────
  usecase "UC02\nImportar Plano\n(subida al backend)" as UC02
  usecase "UC03\nCalibrar Escala\ndel Plano" as UC03

  ' ── Sprint 3 — Pendiente ──────────────────────────────────────────────────
  usecase "UC04\nMarcar Punto\nde Medición" as UC04
  usecase "UC05\nCapturar Señales WiFi\n(envío en línea)" as UC05

  ' ── Sprint 4 — Pendiente ──────────────────────────────────────────────────
  usecase "UC06\nGenerar Mapa de Calor\n(interpolación en backend)" as UC06
  usecase "UC07\nAnalizar Cobertura\n(zonas muertas, CCI/ACI)" as UC07

  ' ── Sprint 5 — Pendiente ──────────────────────────────────────────────────
  usecase "UC08\nObtener Recomendaciones\nde APs (IA)" as UC08
  usecase "UC09\nComparar Escenario\nActual vs Propuesto" as UC09
  usecase "UC10\nExportar Reporte\nTécnico (PDF)" as UC10

  ' ── Sprint 6 — Pendiente ──────────────────────────────────────────────────
  usecase "UC15\nGenerar Enlace\nde Cliente" as UC15
  usecase "UC16\nVer Heatmap\nInteractivo (Web)" as UC16
  usecase "UC17\nVer Análisis y\nPlan AP (Web)" as UC17
}

tech --> UC11
tech --> UC01
tech --> UC02
tech --> UC03
tech --> UC04
tech --> UC06
tech --> UC07
tech --> UC08
tech --> UC09
tech --> UC10
tech --> UC12
tech --> UC15

admin --> UC11
admin --> UC13
admin --> UC18
admin --> UC19

client --> UC16
client --> UC17

UC01 ..> UC19 : <<include>>\n(selector de cliente)
UC04 ..> UC05 : <<include>>
UC05 -- wifi
UC08 -- ia
UC09 ..> UC08 : <<extend>>
UC15 ..> UC16 : <<include>>
UC16 ..> UC17 : <<include>>

note bottom of UC05
  Cada lote de escaneo viaja por
  HTTPS al backend (POST /mediciones).
  El cliente móvil NO almacena las
  muestras entre sesiones.
end note

note bottom of UC06
  La interpolación se ejecuta en el
  backend (FastAPI). El cliente sólo
  solicita y renderiza el resultado.
end note

note bottom of UC13
  El Administrador crea, activa y
  desactiva cuentas de Técnicos.
  Resuelve la dependencia de
  pre-aprovisionamiento de UC11 (RP7).
end note

note bottom of UC19
  El Administrador gestiona el
  catálogo de Clientes (RP7) que
  el Técnico consume al crear/editar
  un Proyecto (UC01).
end note

note bottom of UC15
  Token UUID v4 firmado con expiración
  configurable. Acceso del cliente al
  portal sin instalar la app móvil (RP9).
end note

@enduml
```

> **UC14 (sincronizar proyecto al servidor) eliminado:** en la modalidad online la persistencia es centralizada desde el primer request, por lo que no existe operación de sincronización app↔servidor.

## 4. Trazabilidad UC ↔ RP

| Caso de uso                           | Requerimiento Principal | Sprint |
| ------------------------------------- | ----------------------- | ------ |
| UC01 Gestionar proyecto               | RP8                     | 1      |
| UC02 Importar plano                   | RP2                     | 2      |
| UC03 Calibrar escala                  | RP2                     | 2      |
| UC04 Marcar punto                     | RP2                     | 3      |
| UC05 Capturar señales WiFi            | RP1                     | 3      |
| UC06 Generar heatmap                  | RP3                     | 4      |
| UC07 Analizar cobertura               | RP4                     | 4      |
| UC08 Recomendaciones IA               | RP5                     | 5      |
| UC09 Comparar escenarios              | RP5                     | 5      |
| UC10 Exportar reporte                 | RP6                     | 5      |
| UC11 Autenticar                       | RP8                     | 1      |
| UC12 Historial de proyectos           | RP8                     | 1      |
| UC13 Gestionar usuarios (admin)       | RP7                     | 1      |
| UC15 Generar enlace de cliente        | RP9                     | 6      |
| UC16 Ver heatmap web (cliente)        | RP9                     | 6      |
| UC17 Ver análisis y plan AP (cliente) | RP9                     | 6      |
| UC18 Ver proyectos de la organización | RP7                     | 1      |
| UC19 Gestionar clientes (admin)       | RP7                     | 1      |

> **Mapeo RP autoritativo:** [PAPS Online §7](../Wireless%20Heatmapper%20-%20PAPS%20-%20Modalidad%20Online.md). UC14 eliminado por modalidad online.
