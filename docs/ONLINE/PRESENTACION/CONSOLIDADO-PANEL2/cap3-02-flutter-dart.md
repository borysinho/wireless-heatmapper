## Flutter y Dart para el Desarrollo de la Aplicación Móvil

### Flutter como framework de desarrollo multiplataforma

**Flutter** es un framework de código abierto desarrollado por Google para crear aplicaciones nativas compiladas para móvil (Android e iOS), web y escritorio desde una única base de código en el lenguaje **Dart** (Google LLC, 2023). A diferencia de los frameworks basados en WebView (Ionic, Capacitor) o en puentes JavaScript (React Native), Flutter compila directamente a código de máquina nativo ARM mediante el compilador AOT (Ahead-of-Time) de Dart, lo que produce rendimiento comparable al de aplicaciones nativas escritas en Kotlin o Swift.

La selección de Flutter para el Wireless HeatMapper se justifica por:

- **Capa de renderizado propia:** Flutter no depende de los widgets nativos del sistema operativo. Implementa su propio motor de renderizado sobre Skia (ahora Impeller), lo que garantiza una interfaz consistente en todos los dispositivos Android independientemente de la versión del SO o del fabricante.
- **Hot reload:** durante el desarrollo, los cambios de código se reflejan en la aplicación en ejecución en menos de un segundo sin perder el estado, acelerando el ciclo de iteración.
- **Ecosistema de paquetes:** el repositorio pub.dev ofrece paquetes maduros para todas las funcionalidades requeridas: `dio` (cliente HTTP), `flutter_secure_storage` (almacenamiento cifrado de tokens), `go_router` (navegación declarativa), `flutter_bloc` (gestión de estado con BLoC/Cubit).
- **Acceso a API de WiFi en Android:** el paquete `wifi_scan` y las APIs nativas de Android (via `platform channels` o FFI) permiten acceder a `WifiManager.startScan()` y `WifiManager.getScanResults()` para capturar los parámetros RSSI, SSID, BSSID, canal y frecuencia (Google LLC, 2023).

### Dart como lenguaje

**Dart** es un lenguaje de programación orientado a objetos, fuertemente tipado y con tipado estático opcional, diseñado por Google para aplicaciones cliente de alto rendimiento. Sus características relevantes para el proyecto incluyen:

- **Null safety:** el sistema de tipos de Dart garantiza en tiempo de compilación que las variables no-nulables nunca sean `null`, eliminando una clase entera de errores en tiempo de ejecución.
- **Programación asíncrona con `async/await`:** toda la comunicación con el backend (operaciones de red, lectura de `SecureStorage`) se implementa de forma asíncrona sin necesidad de callbacks anidados.
- **Isolates:** el modelo de concurrencia de Dart aísla la memoria entre hilos de ejecución, eliminando las condiciones de carrera (race conditions) típicas de la programación multi-hilo compartida.

### BLoC/Cubit para la gestión de estado

El patrón **BLoC** (Business Logic Component), y su simplificación **Cubit**, es el patrón de gestión de estado adoptado por el Wireless HeatMapper. BLoC separa la lógica de negocio de la presentación mediante tres conceptos:

- **Eventos** (solo en BLoC): acciones del usuario o del sistema que disparan cambios de estado.
- **Estado (State):** la representación inmutable del estado actual de la UI.
- **Cubit/Bloc:** clase que recibe eventos, ejecuta lógica de negocio (típicamente llamadas a repositorios que invocan la API REST) y emite nuevos estados.

La UI Flutter escucha los estados emitidos mediante widgets `BlocBuilder` y `BlocListener`, reconstruyéndose automáticamente solo cuando el estado relevante cambia. Esta separación facilita las pruebas unitarias de la lógica de negocio sin necesitar un emulador Android: los Cubits son clases Dart puras que pueden instanciarse y probarse con `flutter_test` (Felix Angelov, 2022).

### Dio como cliente HTTP

**Dio** es el cliente HTTP seleccionado para la comunicación con el backend REST. Sus ventajas sobre el cliente HTTP nativo de Dart son:

- **Interceptores:** permiten añadir automáticamente el encabezado `Authorization: Bearer <token>` a todas las peticiones, y detectar respuestas 401 para intentar renovar el access token con el refresh token antes de reintentar la petición original.
- **Cancelación de peticiones:** cuando el usuario navega fuera de una pantalla, las peticiones en curso se cancelan para evitar actualizar el estado de un widget ya destruido.
- **Soporte de FormData y multipart:** necesario para la subida de planos en formato PNG/JPG/PDF al backend (RP2).
