# 19 — Modelo de Base de Datos Implementado

**Fuente:** modelos SQLAlchemy en `backend/app/models/` y migraciones Alembic en `backend/alembic/versions/`
**Alcance:** esquema físico actual del backend FastAPI, persistido en PostgreSQL como única fuente de verdad.
**Propósito:** explicar cómo se organiza y fluye la información desde la base de datos implementada.

---

## 1. Lectura funcional del esquema

La base de datos está organizada alrededor de `proyecto`. Un administrador gestiona `usuario` y `cliente`; el técnico trabaja sobre `plano`, captura `punto_medicion` y `lectura_rssi`, define `conjunto_ap` con los APs relevantes del proyecto y genera `mapa_calor`. El portal cliente se controla con `token_enlace_cliente`, cuyo contenido selecciona explícitamente conjuntos y mapas.

La generación IA ya no persiste entidades separadas de escenario, recomendación, valores proyectados, diagnóstico o reporte. La regla vigente es:

- Un conjunto AP de origen `ia` nace desde un único `conjunto_ap` técnico mediante `conjunto_origen_id`.
- El conjunto IA reutiliza la misma estructura de `conjunto_ap` y `conjunto_ap_item`.
- Los metadatos propios de IA se guardan en columnas opcionales del conjunto y de sus items.
- La IA materializa lecturas `IA_ESTIMADA` en `lectura_rssi` para su conjunto derivado.
- El heatmap proyectado se genera con IDW sobre esas lecturas estimadas y se guarda como `mapa_calor` asociado al conjunto IA.
- La publicación al cliente no depende de estados de aprobación; depende del contenido explícito en `token_enlace_cliente`.

Tablas eliminadas por no responder al negocio vigente:

- `analisis_cobertura` y `ap_detectado`: no se realizará diagnóstico persistido.
- `escenario_optimizado`, `recomendacion_ap` y `valor_proyectado_punto`: la propuesta IA se modela como conjuntos AP derivados.
- `reporte`: no se exportará PDF desde el sistema.
- `estado_gobernanza` en conjuntos AP: el proyecto no mantiene flujo de aprobación/publicación por estado.
- `ap_fisico`, `radio_ap` y `bssid_radio`: se elimina el inventario RF físico; la optimización trabaja con conjuntos AP y lecturas RSSI reales/estimadas.

---

## 2. Diagrama físico completo

```plantuml
@startuml
!pragma layout smetana
title Esquema Físico Implementado — PostgreSQL\nWireless HeatMapper (modalidad 100 % en línea)

skinparam entityBackgroundColor #EBF5FB
skinparam entityBorderColor #2980B9
skinparam entityFontColor #1A252F
skinparam entityHeaderBackgroundColor #2980B9
skinparam entityHeaderFontColor white
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7
skinparam noteFontColor #1A252F
hide circle

package "Seguridad, administración y portal" {
  entity "usuario" as USUARIO {
    * id : INTEGER <<PK>>
    --
    nombre : VARCHAR(120) <<NOT NULL>>
    email : VARCHAR(255) <<UNIQUE, NOT NULL>>
    password_hash : VARCHAR(255) <<NOT NULL>>
    rol : VARCHAR(30) <<DEFAULT 'tecnico'>>
    activo : BOOLEAN <<DEFAULT true>>
    ultimo_acceso : TIMESTAMPTZ
    created_at : TIMESTAMPTZ
  }

  entity "refresh_token" as REFRESH {
    * id : INTEGER <<PK>>
    --
    token : VARCHAR(64) <<UNIQUE, NOT NULL>>
    usuario_id : INTEGER <<FK, NOT NULL>>
    expires_at : TIMESTAMPTZ <<NOT NULL>>
    created_at : TIMESTAMPTZ
  }

  entity "dispositivo_push" as PUSH {
    * id : INTEGER <<PK>>
    --
    usuario_id : INTEGER <<FK, NOT NULL>>
    token : VARCHAR(512) <<UNIQUE, NOT NULL>>
    plataforma : VARCHAR(20) <<DEFAULT 'android'>>
    activo : BOOLEAN <<DEFAULT true>>
    ultimo_registro : TIMESTAMPTZ
    created_at : TIMESTAMPTZ
  }

  entity "cliente" as CLIENTE {
    * id : INTEGER <<PK>>
    --
    nombre : VARCHAR(100) <<UNIQUE, NOT NULL>>
    email_referencia : VARCHAR(255)
    activo : BOOLEAN <<DEFAULT true>>
    created_at : TIMESTAMPTZ
  }

  entity "token_enlace_cliente" as TOKEN_CLIENTE {
    * id : INTEGER <<PK>>
    --
    proyecto_id : INTEGER <<FK, NOT NULL>>
    token : VARCHAR(160) <<UNIQUE, NOT NULL>>
    contenido : JSON <<NOT NULL>>
    expira_en : TIMESTAMPTZ <<NOT NULL>>
    revocado : BOOLEAN <<DEFAULT false>>
    creado_por_id : INTEGER <<FK, NULL>>
    accesos : INTEGER <<DEFAULT 0>>
    ultimo_acceso : TIMESTAMPTZ
    ip_ultimo_acceso : VARCHAR(80)
    created_at : TIMESTAMPTZ
  }
}

package "Proyecto, planos y captura" {
  entity "proyecto" as PROYECTO {
    * id : INTEGER <<PK>>
    --
    nombre : VARCHAR(200) <<NOT NULL>>
    descripcion : VARCHAR(500)
    cliente_id : INTEGER <<FK, NULL>>
    estado : estado_proyecto <<DEFAULT 'nuevo'>>
    tecnico_id : INTEGER <<FK, NOT NULL>>
    ultima_actividad : TIMESTAMPTZ
    cantidad_puntos : INTEGER <<DEFAULT 0>>
    created_at : TIMESTAMPTZ
  }

  entity "plano" as PLANO {
    * id : INTEGER <<PK>>
    --
    proyecto_id : INTEGER <<FK, NOT NULL>>
    nombre : VARCHAR(255) <<NOT NULL>>
    descripcion : VARCHAR(500)
    formato : formato_plano <<NOT NULL>>
    ruta_storage : VARCHAR(500) <<UNIQUE, NOT NULL>>
    ancho_px : INTEGER <<NOT NULL>>
    alto_px : INTEGER <<NOT NULL>>
    tamano_bytes : INTEGER <<NOT NULL>>
    calibracion_x1 : FLOAT
    calibracion_y1 : FLOAT
    calibracion_x2 : FLOAT
    calibracion_y2 : FLOAT
    distancia_real_m : FLOAT
    escala_m_por_px : FLOAT
    poligono_interes : JSON
    created_at : TIMESTAMPTZ
    updated_at : TIMESTAMPTZ
  }

  entity "punto_medicion" as PUNTO {
    * id : INTEGER <<PK>>
    --
    plano_id : INTEGER <<FK, NOT NULL>>
    pos_x : FLOAT <<NOT NULL>>
    pos_y : FLOAT <<NOT NULL>>
    nivel : nivel_senal <<NOT NULL>>
    created_at : TIMESTAMPTZ
  }

  entity "lectura_rssi" as LECTURA {
    * id : INTEGER <<PK>>
    --
    punto_id : INTEGER <<FK, NOT NULL>>
    ssid : VARCHAR(255) <<NOT NULL>>
    bssid : VARCHAR(17) <<NOT NULL>>
    rssi : INTEGER <<NOT NULL>>
    canal : INTEGER
    frecuencia_mhz : INTEGER
    nivel : nivel_senal <<NOT NULL>>
    numero_lectura : INTEGER <<DEFAULT 1>>
    origen : VARCHAR(20) <<DEFAULT 'CAMPO'>>
    conjunto_ap_id : INTEGER <<FK, NULL>>
    mapa_calor_id : INTEGER <<FK, NULL>>
    modelo_origen : VARCHAR(60)
    incertidumbre_db : FLOAT
    created_at : TIMESTAMPTZ
  }
}

package "Conjuntos AP y heatmaps" {
  entity "conjunto_ap" as CONJUNTO {
    * id : INTEGER <<PK>>
    --
    plano_id : INTEGER <<FK, NOT NULL>>
    conjunto_origen_id : INTEGER <<FK, NULL>>
    nombre : VARCHAR(100) <<NOT NULL>>
    proposito : VARCHAR(255) <<NOT NULL>>
    descripcion : TEXT
    es_principal : BOOLEAN <<DEFAULT false>>
    banda_objetivo : VARCHAR(10) <<DEFAULT '5'>>
    origen : VARCHAR(30) <<DEFAULT 'manual_movil'>>
    creado_por_id : INTEGER <<FK, NULL>>
    resumen_ia : TEXT
    metricas_ia : JSON
    restricciones_ia : JSON
    version_motor_ia : VARCHAR(80)
    created_at : TIMESTAMPTZ
    updated_at : TIMESTAMPTZ
  }

  entity "conjunto_ap_item" as CONJUNTO_ITEM {
    * id : INTEGER <<PK>>
    --
    conjunto_ap_id : INTEGER <<FK, NOT NULL>>
    bssid : VARCHAR(17) <<NOT NULL>>
    ssid_snapshot : VARCHAR(255)
    canal_snapshot : INTEGER
    rssi_promedio_snapshot : FLOAT
    pos_x : FLOAT
    pos_y : FLOAT
    accion_recomendada : VARCHAR(40)
    justificacion : TEXT
    altura_m : FLOAT
    tipo_montaje : VARCHAR(30)
    banda : VARCHAR(10)
    modelo_ap : VARCHAR(120)
    costo_estimado : FLOAT
    radios : JSON
  }

  entity "mapa_calor" as MAPA {
    * id : INTEGER <<PK>>
    --
    plano_id : INTEGER <<FK, NOT NULL>>
    conjunto_ap_id : INTEGER <<FK, NULL>>
    algoritmo : VARCHAR(20) <<DEFAULT 'IDW'>>
    resolucion : INTEGER <<DEFAULT 128>>
    modo_generacion : VARCHAR(20) <<DEFAULT 'SUBCONJUNTO'>>
    bssid : VARCHAR(17) <<NOT NULL>>
    ssid : VARCHAR(255) <<NOT NULL>>
    ap_pos_x : FLOAT <<NOT NULL>>
    ap_pos_y : FLOAT <<NOT NULL>>
    aps_interes : JSON
    bssids_generacion : JSON
    matriz : JSON <<NOT NULL>>
    escala : JSON <<NOT NULL>>
    ruta_imagen : VARCHAR(500) <<UNIQUE, NOT NULL>>
    cantidad_puntos : INTEGER <<NOT NULL>>
    rssi_min : FLOAT <<NOT NULL>>
    rssi_max : FLOAT <<NOT NULL>>
    firma_mediciones : VARCHAR(120) <<NOT NULL>>
    created_at : TIMESTAMPTZ
  }
}

USUARIO ||--o{ REFRESH : "tokens"
USUARIO ||--o{ PUSH : "dispositivos"
USUARIO ||--o{ PROYECTO : "tecnico_id"
USUARIO ||--o{ TOKEN_CLIENTE : "creado_por"
CLIENTE ||--o{ PROYECTO : "cliente"
PROYECTO ||--o{ PLANO : "planos"
PROYECTO ||--o{ TOKEN_CLIENTE : "enlaces"
PLANO ||--o{ PUNTO : "puntos"
PUNTO ||--o{ LECTURA : "lecturas RSSI"
PLANO ||--o{ CONJUNTO : "conjuntos AP"
CONJUNTO ||--o{ CONJUNTO_ITEM : "items"
CONJUNTO ||--o{ CONJUNTO : "deriva IA"
CONJUNTO ||--o{ LECTURA : "lecturas estimadas"
PLANO ||--o{ MAPA : "heatmaps"
CONJUNTO ||--o{ MAPA : "mapas asociados"

note right of CONJUNTO
  origen = manual_movil | manual_web | ia
  Si origen = ia:
  - conjunto_origen_id apunta a un conjunto tecnico
  - no se permite derivar desde otro conjunto IA
  - metricas_ia/restricciones_ia documentan la generacion
end note

note right of LECTURA
  origen = CAMPO | IA_ESTIMADA
  CAMPO: captura real del tecnico.
  IA_ESTIMADA: valor proyectado para un conjunto IA.
end note

note right of TOKEN_CLIENTE
  contenido JSON:
  {
    "conjunto_ids": [..],
    "mapa_ids": [..]
  }
end note
@enduml
```

---

## 3. Reglas de integridad relevantes

| Tabla                    | Restricción / índice                                      | Sentido funcional                                    |
| ------------------------ | --------------------------------------------------------- | ---------------------------------------------------- |
| `usuario`                | `UNIQUE(email)`                                           | Login único                                         |
| `cliente`                | `UNIQUE(nombre)`                                          | Evita duplicidad de clientes                        |
| `plano`                  | `UNIQUE(ruta_storage)`                                    | Cada archivo cargado tiene una ruta única           |
| `lectura_rssi`           | `INDEX(origen)`, `INDEX(conjunto_ap_id)`                   | Separa lecturas reales y estimadas                  |
| `conjunto_ap_item`       | `UNIQUE(conjunto_ap_id, bssid)`                           | Un AP no se repite dentro del mismo conjunto        |
| `mapa_calor`             | `UNIQUE(ruta_imagen)`                                     | Cada imagen generada tiene almacenamiento único     |
| `token_enlace_cliente`   | `UNIQUE(token)`                                           | El portal público se resuelve por token no repetido |

---

## 4. Reglas de borrado

| Relación                         | Acción                         | Efecto esperado                                         |
| -------------------------------- | ------------------------------ | ------------------------------------------------------- |
| `proyecto` → `plano`             | `ON DELETE CASCADE`            | Borrar proyecto elimina planos                          |
| `plano` → `punto_medicion`       | `ON DELETE CASCADE`            | Borrar plano elimina puntos y lecturas asociadas        |
| `punto_medicion` → `lectura_rssi`  | `ON DELETE CASCADE`          | Borrar punto elimina lecturas RSSI                      |
| `conjunto_ap` → `lectura_rssi`     | `ON DELETE CASCADE`          | Borrar conjunto IA elimina lecturas estimadas           |
| `plano` → `conjunto_ap`          | `ON DELETE CASCADE`            | Borrar plano elimina conjuntos técnicos e IA            |
| `conjunto_ap` → `conjunto_ap_item` | `ON DELETE CASCADE`          | Borrar conjunto elimina sus APs                         |
| `conjunto_ap.conjunto_origen_id` | `ON DELETE SET NULL`           | Si se borra la fuente, la propuesta IA conserva datos   |
| `plano` → `mapa_calor`           | `ON DELETE CASCADE`            | Borrar plano elimina mapas                              |
| `conjunto_ap` → `mapa_calor`     | `ON DELETE SET NULL`           | Borrar conjunto conserva mapas históricos sin vínculo   |
| `proyecto` → `token_enlace_cliente` | `ON DELETE CASCADE`         | Borrar proyecto elimina enlaces públicos                |

---

## 5. Flujo de datos vigente

1. El técnico captura mediciones desde Android.
2. El backend persiste `punto_medicion` y `lectura_rssi` con `origen = CAMPO`.
3. El técnico selecciona los APs relevantes y crea un `conjunto_ap` de origen `manual_movil` o `manual_web`.
4. El backend genera `mapa_calor` desde un conjunto completo, subconjunto o AP individual.
5. La web solicita recomendaciones IA desde un único conjunto técnico.
6. La IA crea uno o más `conjunto_ap` de origen `ia`, cada uno con `conjunto_origen_id` apuntando al conjunto técnico.
7. La IA estima lecturas RSSI para cada AP recomendado y las persiste como `lectura_rssi.origen = IA_ESTIMADA`.
8. Cada mapa proyectado se interpola con IDW desde esas lecturas estimadas y se persiste como `mapa_calor` asociado al conjunto IA.
9. El administrador crea un enlace cliente seleccionando `conjunto_ids` y `mapa_ids`.
10. El portal cliente solo lee lo incluido en `token_enlace_cliente.contenido`.

---

## 6. Resumen ejecutivo

| Área funcional            | Tablas vigentes                                            | Responsabilidad                                      |
| ------------------------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| Seguridad y usuarios      | `usuario`, `refresh_token`, `dispositivo_push`             | Acceso, sesión y notificaciones                      |
| Cliente y proyecto        | `cliente`, `proyecto`                                      | Organización del trabajo                            |
| Captura en campo          | `plano`, `punto_medicion`, `lectura_rssi`                  | Observaciones reales del relevamiento WiFi          |
| Conjuntos AP              | `conjunto_ap`, `conjunto_ap_item`                          | APs relevantes técnicos y propuestas IA derivadas   |
| Heatmaps                  | `mapa_calor`                                               | Mapas reales/proyectados asociados a conjuntos      |
| Lecturas IA               | `lectura_rssi` con `origen = IA_ESTIMADA`                  | Valores proyectados usados por IDW                  |
| Portal cliente            | `token_enlace_cliente`                                     | Publicación explícita por enlace                    |
