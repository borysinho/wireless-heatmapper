# Aspectos para la puesta en marcha

## Objetivo

Definir las condiciones necesarias para operar Wireless HeatMapper como producto real: infraestructura cloud, costos, licenciamiento, cuentas de publicacion movil, terminos legales, privacidad y adopcion asistida por IA.

## Comparacion cloud

La arquitectura requiere un servidor de aplicacion, base de datos PostgreSQL, reverse proxy, almacenamiento de planos, backups y monitoreo. Para un inicio controlado se compara AWS, Google Cloud y Azure.

| Criterio | AWS | Google Cloud | Azure |
| -------- | --- | ------------ | ----- |
| Computo | EC2 o ECS. | Compute Engine o Cloud Run. | Virtual Machine, App Service o Container Apps. |
| Base de datos | RDS PostgreSQL o PostgreSQL en VM. | Cloud SQL PostgreSQL o PostgreSQL en VM. | Azure Database for PostgreSQL o PostgreSQL en VM. |
| Costeo | AWS Pricing Calculator. | Google Cloud Pricing Calculator. | Azure Pricing Calculator. |
| Ventaja | Ecosistema maduro y amplio. | Buen soporte de analitica y servicios gestionados. | Integracion directa con entorno Microsoft y VM actual del proyecto. |
| Riesgo | Complejidad inicial. | Costos variables si no se controla egress. | Costos de servicios gestionados pueden subir al escalar. |

## Proyeccion de costos iniciales

Los montos son referenciales y deben recalcularse con las calculadoras oficiales antes de compra o despliegue final.

| Escenario | Infraestructura | Costo mensual estimado |
| --------- | --------------- | ---------------------- |
| Economico | Una VM con Docker Compose, PostgreSQL local, backups manuales. | USD 20 a USD 50 |
| Base | VM 2 vCPU/4 GB, disco persistente, backups automatizados. | USD 40 a USD 90 |
| Gestionado | App service/containers + PostgreSQL gestionado + storage. | USD 80 a USD 180 |
| Escalable | Contenedores gestionados, base gestionada, monitoreo y CDN. | USD 180+ |

Para la entrega academica se utiliza Azure por disponibilidad actual del frontend publicado. Para operacion comercial, se recomienda mantener el escenario base hasta validar clientes pagos.

## Cuentas de tiendas moviles

### Google Play

Google Play Console requiere cuenta de Google, aceptacion del Developer Distribution Agreement, verificacion de identidad, seleccion de tipo de cuenta personal u organizacion y pago unico de registro de USD 25. Las cuentas personales nuevas tienen requisitos adicionales de pruebas antes de distribucion publica.

### Apple Developer

Apple Developer Program tiene membresia anual de USD 99 para distribucion en App Store. La inscripcion puede ser individual u organizacion. Las organizaciones deben verificar identidad, contar con D-U-N-S Number y acreditar autoridad para vincular legalmente a la entidad.

## Tipo de licencia

Se recomienda licenciamiento SaaS:

- El cliente paga suscripcion por organizacion.
- Team 24 Software opera backend, web, seguridad y backups.
- La app movil se distribuye como cliente delgado.
- Los datos del cliente se mantienen segregados por organizacion/proyecto.

Tambien puede ofrecerse licencia por proyecto unico para consultores o clientes con baja recurrencia. No se recomienda on-premise en la primera etapa porque incrementa soporte, instalacion y complejidad operativa.

## Terminos y condiciones

Los terminos deben cubrir:

- Descripcion del servicio.
- Roles de usuario.
- Uso permitido y prohibido.
- Responsabilidad sobre datos cargados.
- Disponibilidad y mantenimiento.
- Limitaciones de responsabilidad.
- Propiedad intelectual.
- Suspension de cuentas.
- Soporte y canales oficiales.
- Cambios al servicio.

## Politica de privacidad

La politica debe explicar:

- Datos personales tratados: nombre, email, rol y actividad.
- Datos tecnicos: proyectos, planos, mediciones WiFi, tokens y logs.
- Finalidad: operar el servicio, generar heatmaps, soporte y seguridad.
- Conservacion: mientras exista relacion contractual o necesidad legal.
- Seguridad: autenticacion, control de acceso, cifrado en transito y backups.
- Derechos del usuario: acceso, correccion, eliminacion cuando corresponda.

## Adopcion asistida por IA

Se propone un agente de ayuda integrado que observe contexto de pantalla, rol y flujo actual para responder preguntas sin que el usuario explique desde cero. Ejemplos:

- Si el tecnico esta calibrando plano, explicar como marcar distancia real.
- Si esta capturando WiFi, advertir sobre throttling Android.
- Si el administrador publica enlace, explicar vencimiento y contenido visible.
- Si el cliente consulta portal, explicar interpretacion de colores y RSSI.

## Fuentes oficiales de costos y cuentas

- AWS Pricing Calculator.
- Google Cloud Pricing Calculator.
- Azure Pricing Calculator.
- Google Play Console Help.
- Apple Developer Program.

