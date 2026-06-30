# 04 — Modelo de Datos (modalidad online)

**Notación:** UML 2.5 — Diagrama de clases conceptual + lectura relacional  
**Fuente de verdad:** PostgreSQL 15+ en backend FastAPI  
**Estado:** actualizado contra implementación real al 29-jun-2026  
**Detalle físico:** [19-modelo-base-datos-implementado.md](19-modelo-base-datos-implementado.md)

---

## 1. Principios vigentes

En la modalidad 100 % en línea todas las entidades de dominio residen en PostgreSQL. La app móvil no mantiene base de datos local de dominio ni sincronización diferida. El móvil solo conserva credenciales de sesión en `flutter_secure_storage` y preferencias no críticas.

El esquema implementado aplica los refinamientos aprobados en [18-reglas-gobernanza-conjuntos-ap-heatmaps.md](18-reglas-gobernanza-conjuntos-ap-heatmaps.md):

- La IA no crea escenarios independientes; crea `conjunto_ap` de origen `ia`.
- Las propuestas IA derivan de un único conjunto técnico por `conjunto_origen_id`.
- Las lecturas estimadas se materializan como `lectura_rssi.origen = IA_ESTIMADA`.
- Los heatmaps reales y proyectados se guardan en `mapa_calor`.
- La publicación al cliente se controla con `token_enlace_cliente.contenido`.
- No existen tablas vigentes de diagnóstico persistido, reporte PDF ni inventario RF físico.

---

## 2. Diagrama de clases conceptual

```plantuml
@startuml
!pragma layout smetana
title Modelo de Datos Conceptual — Wireless HeatMapper\nModalidad 100 % en línea
skinparam classBackgroundColor #EBF5FB
skinparam classBorderColor #2980B9
skinparam classHeaderBackgroundColor #2980B9
skinparam classHeaderFontColor white
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7
hide circle

enum RolUsuario {
  admin
  tecnico
}

enum EstadoProyecto {
  nuevo
  en_progreso
  completado
  archivado
}

enum FormatoPlano {
  png
  jpg
  pdf
}

enum NivelSenal {
  verde
  amarillo
  naranja
  rojo
  negro
}

class Usuario {
  +id : Integer
  +nombre : String
  +email : String
  +passwordHash : String
  +rol : RolUsuario
  +activo : Boolean
  +ultimoAcceso : DateTime
}

class RefreshToken {
  +id : Integer
  +token : String
  +expiresAt : DateTime
}

class DispositivoPush {
  +id : Integer
  +token : String
  +plataforma : String
  +activo : Boolean
}

class Cliente {
  +id : Integer
  +nombre : String
  +emailReferencia : String
  +activo : Boolean
}

class Proyecto {
  +id : Integer
  +nombre : String
  +descripcion : String
  +estado : EstadoProyecto
  +ultimaActividad : DateTime
  +cantidadPuntos : Integer
}

class Plano {
  +id : Integer
  +nombre : String
  +descripcion : String
  +formato : FormatoPlano
  +rutaStorage : String
  +anchoPx : Integer
  +altoPx : Integer
  +escalaMPorPx : Float
  +poligonoInteres : JSON
}

class PuntoMedicion {
  +id : Integer
  +posX : Float
  +posY : Float
  +nivel : NivelSenal
}

class LecturaRSSI {
  +id : Integer
  +ssid : String
  +bssid : String
  +rssi : Integer
  +canal : Integer
  +frecuenciaMhz : Integer
  +nivel : NivelSenal
  +numeroLectura : Integer
  +origen : String
  +modeloOrigen : String
  +incertidumbreDb : Float
}

class ConjuntoAP {
  +id : Integer
  +nombre : String
  +proposito : String
  +descripcion : String
  +esPrincipal : Boolean
  +bandaObjetivo : String
  +origen : String
  +resumenIA : String
  +metricasIA : JSON
  +restriccionesIA : JSON
  +versionMotorIA : String
}

class ConjuntoAPItem {
  +id : Integer
  +bssid : String
  +ssidSnapshot : String
  +canalSnapshot : Integer
  +rssiPromedioSnapshot : Float
  +posX : Float
  +posY : Float
  +accionRecomendada : String
  +justificacion : String
  +banda : String
  +modeloAP : String
  +costoEstimado : Float
  +radios : JSON
}

class MapaCalor {
  +id : Integer
  +algoritmo : String
  +resolucion : Integer
  +modoGeneracion : String
  +bssid : String
  +ssid : String
  +apsInteres : JSON
  +bssidsGeneracion : JSON
  +matriz : JSON
  +escala : JSON
  +rutaImagen : String
  +cantidadPuntos : Integer
  +rssiMin : Float
  +rssiMax : Float
  +firmaMediciones : String
}

class TokenEnlaceCliente {
  +id : Integer
  +token : String
  +contenido : JSON
  +expiraEn : DateTime
  +revocado : Boolean
  +accesos : Integer
  +ultimoAcceso : DateTime
  +ipUltimoAcceso : String
}

Usuario "1" --o "0..*" RefreshToken : sesion
Usuario "1" --o "0..*" DispositivoPush : notifica
Usuario "1" --o "0..*" Proyecto : tecnico
Usuario "0..1" --o "0..*" ConjuntoAP : crea
Usuario "0..1" --o "0..*" TokenEnlaceCliente : crea
Cliente "0..1" --o "0..*" Proyecto : encarga
Proyecto "1" *-- "0..*" Plano : contiene
Proyecto "1" *-- "0..*" TokenEnlaceCliente : publica
Plano "1" *-- "0..*" PuntoMedicion : registra
PuntoMedicion "1" *-- "0..*" LecturaRSSI : contiene
Plano "1" *-- "0..*" ConjuntoAP : organiza
ConjuntoAP "0..1" --o "0..*" ConjuntoAP : deriva IA
ConjuntoAP "1" *-- "1..*" ConjuntoAPItem : incluye
ConjuntoAP "0..1" --o "0..*" LecturaRSSI : estimadas IA
Plano "1" *-- "0..*" MapaCalor : genera
ConjuntoAP "0..1" --o "0..*" MapaCalor : contexto

note bottom of LecturaRSSI
  origen = CAMPO | IA_ESTIMADA
  CAMPO nunca se modifica por la IA.
end note

note bottom of ConjuntoAP
  origen = manual_movil | manual_web | ia
  Si origen = ia, debe derivar de un
  conjunto tecnico mediante conjunto_origen_id.
end note

note bottom of TokenEnlaceCliente
  contenido JSON:
  conjunto_ids y mapa_ids publicados.
  El portal no accede al proyecto completo.
end note
@enduml
```

---

## 3. Lectura relacional vigente

| Área | Tablas | Responsabilidad |
| ---- | ------ | --------------- |
| Seguridad y sesión | `usuario`, `refresh_token`, `dispositivo_push` | Login, refresh token y notificaciones FCM |
| Clientes y proyectos | `cliente`, `proyecto` | Catálogo de clientes y trabajo de survey |
| Planos y captura | `plano`, `punto_medicion`, `lectura_rssi` | Planos calibrados, puntos y RSSI real/estimado |
| Conjuntos AP | `conjunto_ap`, `conjunto_ap_item` | Selecciones técnicas y propuestas IA derivadas |
| Heatmaps | `mapa_calor` | Matrices e imágenes generadas por IDW |
| Portal cliente | `token_enlace_cliente` | Publicación explícita por token |

---

## 4. Entidades eliminadas

| Entidad eliminada | Motivo |
| ----------------- | ------ |
| `analisis_cobertura` | No se persiste diagnóstico separado |
| `ap_detectado` | No se confirma inventario inferido desde diagnóstico |
| `escenario_optimizado` | La propuesta IA se modela como `conjunto_ap.origen = ia` |
| `recomendacion_ap` | Las recomendaciones viven en `conjunto_ap_item` |
| `valor_proyectado_punto` | Los valores proyectados viven en `lectura_rssi` y `mapa_calor` |
| `reporte` | No se exporta PDF desde el alcance vigente |
| `ap_fisico`, `radio_ap`, `bssid_radio` | Se eliminó inventario RF físico persistido |

---

## 5. Reglas de integridad principales

| Regla | Aplicación |
| ----- | ---------- |
| Usuario único por email | `usuario.email` único |
| Cliente único por nombre | `cliente.nombre` único |
| Plano pertenece a un proyecto | `plano.proyecto_id` con borrado en cascada |
| Punto pertenece a un plano | `punto_medicion.plano_id` con borrado en cascada |
| Lectura pertenece a un punto | `lectura_rssi.punto_id` con borrado en cascada |
| AP no repetido en conjunto | `UNIQUE(conjunto_ap_id, bssid)` |
| Conjunto IA no modifica su fuente | `conjunto_origen_id` conserva trazabilidad |
| Enlace cliente es revocable y expirable | `token_enlace_cliente.token`, `expira_en`, `revocado` |

---

## 6. Referencias técnicas

- [19 — Modelo de Base de Datos Implementado](19-modelo-base-datos-implementado.md)
- [18 — Reglas de Gobierno para Conjuntos de APs, Heatmaps e IA](18-reglas-gobernanza-conjuntos-ap-heatmaps.md)
- [21 — Auditoría de Implementación vs Plan Scrum](21-auditoria-implementacion-vs-plan.md)

