# 12. Anexos

## 12.1 Esquema Gráfico: Situación Actual vs. Situación Deseada

El siguiente diagrama ilustra el contraste entre el estado actual de gestión de cobertura Wi-Fi en Bulldog Tech. y el escenario que se alcanzará con la implementación de Wireless HeatMapper:

```plantuml
@startuml Situacion_Actual_Deseada
skinparam backgroundColor #FAFAFA
skinparam packageBackgroundColor #EBF5FB
skinparam packageBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

left to right direction

package "SITUACIÓN ACTUAL" as actual #FFE0E0 {
  usecase "Reportes de\nfalla Wi-Fi" as r1
  usecase "Diagnóstico\ninformal" as r2
  usecase "Sin registro\nni historial" as r3
  usecase "Decisiones\nempíricas" as r4
  usecase "Problemas\nrecurrentes" as r5

  r1 --> r2
  r2 --> r3
  r3 --> r4
  r4 --> r5
  r5 --> r1 : ciclo vicioso
}

package "SITUACIÓN DESEADA" as deseada #E0F7E0 {
  usecase "Técnico realiza\nlevantamiento\ncon app móvil" as d1
  usecase "Backend genera\nheatmap georreferenciado" as d2
  usecase "IA analiza y\nrecomienda mejoras" as d3
  usecase "Panel web muestra\nresultados y reportes" as d4
  usecase "Decisiones técnicas\nbasadas en datos" as d5
  usecase "Historial y\ncomparativa temporal" as d6

  d1 --> d2
  d2 --> d3
  d3 --> d4
  d4 --> d5
  d5 --> d6
}

actual --> deseada : Wireless HeatMapper

@enduml
```

---

## 12.2 Datos del Caso de Estudio

| Campo               | Detalle                                                        |
| ------------------- | -------------------------------------------------------------- |
| **Empresa**         | Bulldog Tech.                                                  |
| **Rubro**           | Servicios tecnológicos: soporte, consultoría, redes           |
| **Ubicación**       | Santa Cruz de la Sierra, Bolivia                               |
| **Problemática**    | Deficiente gestión y diagnóstico de cobertura Wi-Fi interna    |
| **Áreas afectadas** | Taller técnico, área administrativa, sala de atención al cliente |
| **Necesidad clave** | Herramienta accesible de site survey y heatmapping Wi-Fi       |

---

## 12.3 Currículum Vitae de los Integrantes

### Fernandez Ortega Jhasmany Jhunnior

| Campo              | Detalle                                               |
| ------------------ | ----------------------------------------------------- |
| **Carrera**        | Ingeniería Informática — FICCT, UAGRM                |
| **Registro**       | 207025509                                             |
| **Rol en el proyecto** | Scrum Master / Desarrollador                      |
| **Áreas de enfoque** | Backend, infraestructura, DevOps                   |

---

### Quiroga Flores Herland Borys

| Campo              | Detalle                                               |
| ------------------ | ----------------------------------------------------- |
| **Carrera**        | Ingeniería Informática — FICCT, UAGRM                |
| **Registro**       | 200104373                                             |
| **Rol en el proyecto** | Product Owner / Desarrollador                    |
| **Áreas de enfoque** | Análisis de requisitos, frontend web, mobile       |

---

## Nota sobre la Carta de Formalización

La **Carta de Formalización** del acuerdo con el cliente Bulldog Tech. es un documento físico firmado que se adjunta de forma impresa al presente trabajo. Contiene el compromiso formal entre el equipo de desarrollo y el representante de Bulldog Tech. para la ejecución del proyecto Wireless HeatMapper bajo el marco de trabajo Scrum.

---
