# Guía operativa para implementar Sprints con IA

**Proyecto:** Wireless HeatMapper  
**Objetivo de esta guía:** Estandarizar cómo usar la IA durante cada Sprint para maximizar velocidad, calidad y trazabilidad.

---

## 1. Principio base de trabajo

La forma más efectiva es trabajar por **Historia de Usuario (HU)**, no por Sprint completo en una sola sesión.

- Una conversación de IA por HU.
- Un objetivo claro por sesión.
- Un cierre verificable por criterios de aceptación.

Esto reduce retrabajo, evita respuestas genéricas y mejora la trazabilidad entre PAPS, F3, F4 y F5.

---

## 2. Flujo recomendado por evento Scrum

## R-2 Sprint Planning

1. Confirmar HU comprometidas del Sprint en F5.
2. Preparar un "paquete de contexto" por HU:

- HU y criterios de aceptación (F4).
- Tareas Sp-NN asociadas (F5).
- Restricciones globales del proyecto (AGENTS).

3. Definir orden de implementación por dependencias.
4. Crear objetivo técnico de la HU (qué se debe entregar y cómo se validará).

## R-3 Ejecución del Sprint

Para cada HU, ejecutar el ciclo en este orden:

1. Análisis funcional y técnico de la HU.
2. Diseño mínimo viable (sin sobrearquitectura).
3. Implementación incremental por tarea Sp-NN.
4. Pruebas mínimas por componente.
5. Verificación contra criterios de aceptación.
6. Validación de trazabilidad antes de marcar como lista.

## Daily Scrum

1. Reportar avance por Sp-NN: terminado, en proceso o bloqueado.
2. Reportar bloqueo concreto y siguiente acción.
3. Definir la siguiente tarea más pequeña y ejecutable.

## R-4 Sprint Review

1. Ejecutar validación de trazabilidad RP ↔ HU ↔ tareas.
2. Preparar evidencia de cada criterio de aceptación cumplido.
3. Mostrar incremento funcional, no solo código.
4. Registrar feedback del cliente/PO para backlog.

## R-5 Retrospective

1. Identificar qué prompts funcionaron mejor.
2. Registrar patrones repetibles como instrucciones/prompts/skills.
3. Ajustar compuertas de calidad del próximo Sprint.

---

## 3. Compuertas de calidad (Quality Gates)

Antes de cerrar una tarea Sp-NN:

1. Cumple las instrucciones técnicas del área (mobile, backend, web o infra).
2. Tiene pruebas mínimas relevantes.
3. Cumple criterio de aceptación asociado.
4. Está trazada correctamente con su HU.
5. Es demostrable en Review.

Si falla una compuerta, no se marca como terminada.

---

## 4. Reglas de oro para usar IA de forma efectiva

1. No pedir "haz todo el Sprint" en un solo prompt.
2. Dar contexto mínimo obligatorio en cada sesión (HU + Sp-NN + criterios + restricciones).
3. Pedir siempre salida estructurada: análisis, diseño, implementación, pruebas, validación.
4. Cerrar una tarea antes de abrir otra.
5. Mantener cambios pequeños y verificables.

---

## 5. Plantilla de prompt operativo por HU

Usar esta estructura en cada conversación:

1. HU objetivo: PB-XX (nombre).
2. Sprint activo: Sprint N.
3. Tarea objetivo: Sp-NN.
4. Criterios de aceptación a cubrir: CA1, CA2, ...
5. Restricciones técnicas aplicables (mobile/backend/web/infra).
6. Entrega esperada:

- análisis breve,
- diseño,
- implementación por archivo,
- pruebas mínimas,
- checklist de aceptación.

---

## 6. Ejemplo completo de un ciclo end-to-end

## Escenario

- **Sprint:** 1
- **HU:** PB-09 Autenticar usuario
- **Tarea objetivo:** Sp-03 Implementar AuthRepository
- **Meta:** Validar credenciales contra persistencia local y dejar base para cumplir CA1 y CA2.

## Paso 1: Preparación (R-2 / inicio R-3)

Contexto que se pasa a la IA:

- HU PB-09 en F4.
- Sp-03 en F5.
- Restricciones de mobile (arquitectura por capas + BLoC/Cubit + seguridad).
- Regla: no implementar fuera de la HU comprometida.

## Paso 2: Prompt inicial a IA

"Trabajaremos la HU PB-09 del Sprint 1, tarea Sp-03. Analiza criterios de aceptación CA1 y CA2. Diseña e implementa AuthRepository en arquitectura por capas (data/domain/presentation), con validación de credenciales y manejo de errores. Incluye pruebas unitarias mínimas y checklist de aceptación."

## Paso 3: Entrega esperada de la IA

1. **Análisis:** qué valida y qué no valida la tarea Sp-03.
2. **Diseño:** contrato del repositorio + flujo de validación.
3. **Implementación:** archivos mínimos impactados por capa.
4. **Pruebas:** éxito, credenciales inválidas, error de lectura.
5. **Checklist:** CA1/CA2 en estado parcial o completo según alcance.

## Paso 4: Verificación técnica

1. Revisar que no haya lógica de UI en data/domain.
2. Revisar que no existan credenciales en texto plano.
3. Ejecutar pruebas unitarias.
4. Confirmar que Sp-03 queda trazada con PB-09.

## Paso 5: Daily Scrum

Reporte breve:

- Hecho: Sp-03 implementada y probada.
- Evidencia: pruebas de AuthRepository.
- Siguiente: Sp-04 AuthCubit/AuthBloc.
- Bloqueos: ninguno.

## Paso 6: Cierre de HU para Review

Al finalizar todas las tareas de PB-09:

1. Ejecutar skill de trazabilidad RP ↔ PB ↔ Sp.
2. Confirmar criterios de aceptación de PB-09.
3. Preparar demo de login exitoso y login inválido.

## Resultado del ciclo completo

- Tarea implementada con calidad controlada.
- Evidencia de cumplimiento funcional.
- Trazabilidad mantenida para Review.
- Base reutilizable para la siguiente tarea de la misma HU.

---

## 7. Métrica práctica de control semanal

Para saber si la estrategia con IA está funcionando:

1. Porcentaje de tareas Sp-NN cerradas sin retrabajo.
2. Número de bloqueos técnicos no resueltos en 24 horas.
3. Cobertura de criterios de aceptación por HU.
4. Hallazgos de trazabilidad (objetivo: 0 críticos en Review).

Si estas métricas mejoran Sprint a Sprint, la implementación asistida por IA está siendo efectiva.
