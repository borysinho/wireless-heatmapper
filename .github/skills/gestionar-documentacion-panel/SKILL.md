---
name: gestionar-documentacion-panel
description: "Crea, edita, revisa y consolida la documentación de los Paneles del proyecto Wireless HeatMapper. Garantiza formalismo académico-profesional, continuidad para conversión a Word, redacción humanizada sin marcas de IA, y coherencia entre todos los archivos individuales de cada Panel."
argument-hint: "Panel a trabajar (ej. PANEL-1, PANEL-2) o acción específica (ej. revisar-formalismo, consolidar, crear-seccion, humanizar)"
user-invocable: true
disable-model-invocation: false
---

# Skill: Gestionar Documentación de Paneles

## Propósito

Manejar de forma uniforme y consistente la documentación de los Paneles del proyecto Wireless HeatMapper. Esta documentación corresponde a un proyecto de ingeniería de software profesional implementado para Bulldog Tech., empresa real del sector tecnológico. Los documentos generados deben ser aptos para su entrega formal, impresión y defensa ante tribunal evaluador.

## Alcance

Esta skill aplica a todos los archivos dentro de `docs/PANELES/` y sus subcarpetas. Cada Panel contiene archivos individuales que, al ensamblarse en orden según el `00-indice.md` correspondiente, producen un único documento formal continuo.

---

## 1. Estructura esperada de cada Panel

Cada carpeta de Panel debe contener:

```
PANEL X/
├── [apuntes de clase]          ← Solo lectura. Contexto del docente.
└── PERFIL-PROYECTO/ (u otro nombre de entregable)
    ├── 00-indice.md            ← Archivo maestro de ensamble
    ├── 01-caratula.md
    ├── 02-tabla-contenidos.md
    ├── 03-introduccion.md
    ├── NN-[seccion].md
    └── SPRINT-N/
        ├── 01-[subseccion].md
        └── ...
```

El archivo `00-indice.md` controla el orden de ensamble mediante directivas `[[include: ruta]]`. Siempre debe mantenerse actualizado cuando se agrega o elimina un archivo.

---

## 2. Reglas de formalismo del documento

### 2.1 Prohibiciones absolutas

Los siguientes elementos están **prohibidos** en cualquier archivo de documentación formal:

- Iconos Unicode o emojis de cualquier tipo (ningún simbolo como flechas decorativas, checkmarks visuales, estrellas, caras, etc.)
- Tablas que usen iconos como valor de celda (reemplazar con texto: "Sí / No", "Implementado / Pendiente", "Cumple / No cumple")
- Lenguaje coloquial, abreviaciones informales o jerga técnica sin definir
- Referencias a "proyecto universitario", "materia", "docente", "nota" o cualquier contexto académico interno en el cuerpo del documento (ese contexto solo va en los archivos de apuntes de clase, nunca en el entregable)
- Primera persona del plural como voz narrativa dominante ("hicimos", "decidimos", "creemos"); preferir tercera persona o construcciones impersonales
- Frases de relleno típicas de texto generado por IA (ver sección 5)

### 2.2 Requisitos de formalismo

- Todo documento debe redactarse en español formal (es-BO), con ortografía y puntuación correctas
- Las tablas deben tener encabezado claro y alineación coherente
- Los términos técnicos en inglés deben escribirse en cursiva la primera vez que aparecen y, si es necesario, acompañarse de una definición breve entre paréntesis
- Las siglas deben definirse la primera vez que se usan: "Received Signal Strength Indicator (RSSI)"
- Los títulos de sección deben seguir la jerarquía del documento sin saltar niveles (H1 → H2 → H3)
- Las referencias bibliográficas deben seguir el formato APA 7.a edición

### 2.3 Tono y persona narrativa

- Narrar el proyecto como una iniciativa profesional real que está siendo ejecutada para un cliente
- Evitar el tono expositivo escolar ("En este documento se explicará..."); preferir el tono técnico-profesional ("El presente documento describe...")
- Las decisiones de diseño deben justificarse técnicamente, no pedagógicamente
- Las pruebas y validaciones deben describirse como parte del proceso de aseguramiento de calidad, no como requisitos de evaluación

---

## 3. Reglas de continuidad para conversión a Word

El proceso automatizado de conversión (pandoc u otro) ensambla todos los archivos en orden y produce un único documento. Para que el resultado sea correcto:

### 3.1 Encabezados

- Cada archivo individual comienza con exactamente **un encabezado H1 (`#`)**, que corresponde al título de la sección
- No usar H1 dentro del cuerpo del archivo para subsecciones; H2 (`##`) en adelante para el contenido interno
- Los números de sección en los títulos deben ser consistentes con el índice del documento (ej.: `# 4. Antecedentes`, no `# Antecedentes`)

### 3.2 Saltos de página

- Insertar un separador `---` al final de cada archivo para que el proceso de conversión introduzca un salto de página entre secciones
- No insertar separadores decorativos intermedios que no correspondan a un salto de página real

### 3.3 Referencias cruzadas

- No usar rutas de archivo relativas como referencias visibles (ej.: `ver [05-descripcion-problema.md]`) porque se rompen en Word
- Para referencias internas usar el nombre de la sección: "véase la sección Descripción del Problema"

### 3.4 Imágenes y diagramas

- Los diagramas PlantUML deben estar en bloques de código con la etiqueta `plantuml`
- Cada diagrama debe tener un `title` interno descriptivo, ya que ese título aparece como pie de figura en la conversión
- Si un diagrama no puede renderizarse automáticamente, proveer una descripción textual equivalente inmediatamente después del bloque

### 3.5 Numeración

- Las tablas deben tener un título descriptivo arriba: `**Tabla 1.** Comparación de herramientas de análisis Wi-Fi`
- Las figuras (diagramas) deben tener un pie de figura: `_Figura 1. Diagrama de causa-efecto — Deficiente gestión de cobertura Wi-Fi_`

---

## 4. Estructura mínima del documento final (Panel 1)

El documento ensamblado debe contener obligatoriamente los siguientes elementos, en este orden:

| Orden | Elemento                          | Observaciones                                                                 |
| ----- | --------------------------------- | ----------------------------------------------------------------------------- |
| 1     | Caratula                          | Institución, carrera, título del proyecto, integrantes, registro, lugar, fecha |
| 2     | Tabla de contenidos               | Al menos dos niveles de profundidad                                           |
| 3     | Introducción                      | Contextualiza el documento; motiva al lector                                  |
| 4     | Antecedentes                      | Fundamento teórico + comparativa de software similar (mínimo 3 aplicaciones) |
| 5     | Descripción del problema          | Narrativa detallada + diagrama Ishikawa + modelo de dominio                   |
| 6     | Situación problemática            | 5 a 10 líneas; solo el problema central sin mencionar tecnología               |
| 7     | Situación deseada                 | 5 a 10 líneas; impacto esperado en el negocio del cliente                     |
| 8     | Objetivos                         | Objetivo general + objetivos específicos con entregable por cada uno           |
| 9     | Alcance                           | Organizado por módulos o épicas; incluye límites explícitos del sistema        |
| 10    | Tecnología de desarrollo          | Stack + justificación + proceso de desarrollo (Scrum con Gantt)               |
| 11    | Bibliografía                      | Normas APA 7.a edición                                                        |
| 12    | Anexos                            | Esquema gráfico, datos del cliente, CV de integrantes, carta de formalización |
| 13    | Resultado Sprint 0                | Organización del equipo + ingeniería de requisitos + modelos iniciales        |
| 14    | Resultado Sprint 1                | Historias de usuario + modelos + implementación + pruebas                     |

---

## 5. Patrones de escritura a evitar (humanización)

Los siguientes patrones son característicos de texto generado por IA. Deben identificarse y reescribirse cuando aparezcan en cualquier archivo:

### 5.1 Frases de apertura y cierre típicas de IA

| Patrón a evitar                             | Alternativa sugerida                              |
| ------------------------------------------- | ------------------------------------------------- |
| "Es importante destacar que..."             | Eliminar y comenzar directamente con el hecho     |
| "Cabe mencionar que..."                     | Eliminar y comenzar directamente con el hecho     |
| "En conclusión, podemos decir que..."       | Usar "En definitiva,..." o reformular             |
| "Es fundamental comprender que..."          | Eliminar; el texto debe ser autoexplicativo       |
| "Sin duda alguna,..."                       | Eliminar; las afirmaciones deben sustentarse solas|
| "En el marco del presente proyecto..."      | Usar "En este proyecto..." o reformular           |
| "Como se mencionó anteriormente,..."        | Reemplazar con referencia específica a la sección |
| "A lo largo del documento se abordará..."   | Reformular con qué contiene el documento          |

### 5.2 Estructura de párrafo artificialmente simétrica

Evitar párrafos donde todas las oraciones tienen exactamente la misma longitud o estructura. Mezclar oraciones cortas directas con oraciones más largas que profundizan el argumento.

### 5.3 Enumeraciones exhaustivas sin criterio

Evitar listas que enumeran "todos los aspectos posibles" sin jerarquía. Seleccionar los puntos más relevantes y justificar por qué se incluyen.

### 5.4 Hipérboles corporativas

| Patrón a evitar                                             | Alternativa                                    |
| ----------------------------------------------------------- | ---------------------------------------------- |
| "solución integral, robusta y escalable"                    | Describir qué hace concretamente               |
| "de vanguardia", "de última generación"                     | Especificar la versión o el estándar           |
| "garantiza una experiencia óptima al usuario"               | Describir el comportamiento esperado           |
| "revoluciona la forma en que..."                            | Describir el cambio específico que produce     |

### 5.5 Redundancias y circularidades

Evitar definir un concepto usando el mismo concepto: "Un mapa de calor Wi-Fi es un mapa que muestra el calor de la señal Wi-Fi". Buscar una definición que aporte información nueva.

---

## 6. Checklist de revisión antes de marcar un archivo como listo

Verificar cada punto antes de considerar un archivo completo:

**Contenido:**
- El contenido es coherente con lo indicado por el docente en los apuntes de clase del Panel
- No se menciona el proyecto como universitario; se describe como un proyecto profesional para Bulldog Tech.
- La redacción es técnica, directa y en español formal
- No hay frases de relleno ni patrones típicos de IA

**Formalismo:**
- No hay emojis ni iconos de ningún tipo
- Las tablas con valores binarios usan texto ("Sí/No") y no iconos
- Los términos en inglés están en cursiva la primera vez que aparecen
- Las siglas están definidas en su primera aparición

**Continuidad para Word:**
- El archivo comienza con exactamente un H1 que incluye el número de sección
- El archivo termina con `---`
- No hay rutas de archivo como referencias cruzadas visibles
- Las tablas tienen título descriptivo arriba (`**Tabla N.**`)
- Los diagramas tienen título interno y pie de figura

**Diagramas:**
- Cada bloque PlantUML tiene `title` interno
- El `skinparam` mantiene la paleta institucional: fondo `#EBF5FB`, bordes `#2980B9`, notas `#FFFDE7`
- Los diagramas no usan notación UML anterior a la versión 2.5

---

## 7. Procedimiento para cada acción

### 7.1 Crear una nueva sección

1. Leer los apuntes de clase del Panel correspondiente en `docs/PANELES/PANEL X/` para conocer exactamente qué debe contener la sección
2. Verificar en `00-indice.md` el número y nombre de la sección
3. Crear el archivo con el nombre `NN-nombre-seccion.md`
4. Aplicar las reglas de formalismo (sección 2), continuidad (sección 3) y checklist (sección 6)
5. Agregar la directiva `[[include: NN-nombre-seccion.md]]` en el lugar correcto de `00-indice.md`

### 7.2 Revisar y corregir un archivo existente

1. Leer el archivo completo
2. Aplicar el checklist de la sección 6 punto por punto
3. Reemplazar todos los emojis/iconos en tablas por texto equivalente
4. Identificar y reescribir los patrones de la sección 5
5. Verificar que el H1 incluya el número de sección
6. Confirmar que el archivo termina con `---`
7. Verificar que las tablas tienen título y los diagramas tienen pie de figura

### 7.3 Consolidar (ensamblar) el documento

1. Leer el `00-indice.md` para obtener el orden de archivos
2. Verificar que todos los archivos referenciados existen
3. Verificar que no hay archivos en la carpeta que no estén referenciados en el índice
4. Recorrer cada archivo y aplicar el checklist de la sección 6
5. Reportar cualquier inconsistencia de numeración de secciones o saltos de nivel de encabezado
6. Confirmar que la secuencia narrativa es coherente: el final de cada sección lleva naturalmente al inicio de la siguiente

### 7.4 Humanizar un archivo

1. Leer el archivo completo
2. Identificar cada ocurrencia de los patrones de la sección 5 y marcarlos
3. Reescribir los párrafos afectados variando la longitud de oraciones, eliminando frases de relleno y sustituyendo hipérboles por descripciones concretas
4. Verificar que la reescritura mantiene el significado técnico original
5. Asegurar que el resultado sigue siendo preciso, formal y verificable

---

## 8. Contexto del proyecto

- **Cliente real:** Bulldog Tech. (empresa tecnológica, Santa Cruz de la Sierra, Bolivia)
- **Sistema:** Wireless HeatMapper — app Android + backend FastAPI + panel web React
- **Equipo:** Fernandez Ortega Jhasmany Jhunnior (Scrum Master) y Quiroga Flores Herland Borys (Product Owner)
- **Marco de trabajo:** Scrum con actividades de ingeniería de software integradas
- **Modalidad:** 100% en línea; sin persistencia local en el cliente móvil

## 9. Archivos de referencia

- Apuntes del docente (solo lectura): `docs/PANELES/PANEL 1/Clase 1 - Perfil del Proyecto.md` y `docs/PANELES/PANEL 1/Clases 21-04-2026 - Descripción general del proyecto y primer sprint.md`
- Plan de sprints: `docs/PANELES/plan-de-sprints.md`
- Documentos del Panel 1 (editables): `docs/PANELES/PANEL 1/PERFIL-PROYECTO/`
- Paleta de colores PlantUML: fondo `#EBF5FB`, bordes `#2980B9`, notas/paquetes `#FFFDE7`, fondo general `#FAFAFA`

## 10. Restricciones

- No modificar los archivos de apuntes de clase (son fuentes de solo lectura)
- No referenciar documentos fuera de `docs/PANELES/` en el cuerpo del entregable
- No introducir contenido de sprints futuros al no completados en el Panel correspondiente
- No usar el plan histórico `docs/SCRUM/` como fuente de información
- No reintroducir PB-14 (sincronización offline) ni HU eliminadas en la modalidad online
- Mantener los identificadores estables: RP1..RP9, PB-01..PB-19 (sin PB-14), Sp{N}-NN
