# 9. Alcance

El sistema Wireless HeatMapper abarca las siguientes funcionalidades organizadas por módulos:

---

## 9.1 Módulo de Autenticación y Usuarios

Gestiona el acceso seguro al sistema para todos los perfiles de usuario. Incluye:

- Registro e inicio de sesión con autenticación JWT.
- Gestión de roles: Administrador, Técnico y Cliente.
- Recuperación de contraseña y gestión de perfil.
- Control de sesiones activas y cierre de sesión seguro.

---

## 9.2 Módulo de Gestión de Clientes y Proyectos

Permite la administración completa de los clientes (empresas) y sus proyectos de levantamiento Wi-Fi. Incluye:

- Alta, edición y desactivación de clientes (organizaciones).
- Creación y gestión de proyectos de levantamiento por instalación.
- Carga y administración del plano de planta de cada instalación.
- Asignación de técnicos a proyectos.
- Listado, filtrado y seguimiento del estado de proyectos.

---

## 9.3 Módulo de Levantamiento Wi-Fi (App Móvil)

Ejecutado desde la aplicación Android Flutter, permite al técnico recolectar datos de señal en campo. Incluye:

- Visualización del plano de planta del proyecto activo.
- Marcación de puntos de medición sobre el plano con posicionamiento táctil.
- Captura automática de valores RSSI, SSID, BSSID, frecuencia y canal de todas las redes detectadas en cada punto.
- Indicador visual del nivel de cobertura por punto medido.
- Envío inmediato de mediciones al backend (modalidad 100% en línea, sin almacenamiento local).
- Control de throttling Android (máx. 4 escaneos / 2 min en Android 8.0+).

---

## 9.4 Módulo de Generación de Heatmap

Procesa las mediciones recolectadas y genera la visualización de cobertura. Incluye:

- Interpolación de valores RSSI sobre el plano usando algoritmo IDW (*Inverse Distance Weighting*).
- Generación de mapa de calor con escala de colores por umbral (excelente, buena, aceptable, débil, zona muerta).
- Exportación del mapa de calor como imagen PNG y como reporte PDF.
- Historial de mapas por proyecto para comparativa temporal.

---

## 9.5 Módulo de Análisis con Inteligencia Artificial

Procesa los datos de cobertura y genera recomendaciones automatizadas. Incluye:

- Identificación de zonas muertas (RSSI ≤ −90 dBm) y zonas con cobertura insuficiente.
- Detección de solapamiento excesivo de canales entre APs.
- Generación de recomendaciones textuales: reubicación de APs, cambio de canal, potencia de transmisión.
- Puntaje global de calidad de cobertura por instalación.

---

## 9.6 Panel de Administración Web

Interfaz web accesible desde navegador para administradores y clientes. Incluye:

- Dashboard con resumen de proyectos activos y alertas de cobertura.
- CRUD completo de usuarios, clientes y proyectos.
- Visualización de mapas de calor y descarga de reportes.
- Historial de levantamientos y comparativa de evolución de cobertura.
- Gestión de configuración del sistema.

---

## Requerimientos fuera del alcance

Los siguientes aspectos quedan **explícitamente fuera del alcance** del proyecto:

- Soporte para tecnologías de red distintas a Wi-Fi (Bluetooth, LTE, Ethernet).
- Posicionamiento en interiores con GPS o trilateración (el posicionamiento es manual sobre plano).
- Módulo de facturación o cobro de servicios.
- Integración con sistemas ERP o CRM externos.
- Modo offline en la aplicación móvil (toda la persistencia ocurre en el backend).

---
