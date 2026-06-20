## 3.3 Desarrollo Móvil con Flutter y Arquitectura BLoC

Flutter construye la interfaz a partir de un árbol declarativo de widgets que el motor de renderizado dibuja con alta frecuencia de actualización. En plataformas Android recientes, la pila gráfica puede apoyarse en Skia o Impeller para mantener animaciones e interacción fluida. Esta base resulta particularmente útil en Wireless HeatMapper, donde el técnico manipula planos, ejecuta zoom, desplaza la vista y necesita retroalimentación visual inmediata durante la captura en campo.

La app se organiza con una arquitectura limpia de tres capas: presentación, dominio y datos. La capa de presentación contiene páginas, componentes visuales y gestores de estado. La capa de dominio modela entidades y casos de uso sin depender de detalles externos. La capa de datos integra clientes HTTP, serialización y repositorios concretos. Esta división reduce acoplamiento y facilita pruebas unitarias sobre flujos críticos como autenticación, calibración y captura WiFi.

El patrón *Business Logic Component* (BLoC, componente de lógica de negocio) y su variante Cubit desacoplan la interfaz de las transiciones de estado. Un Cubit recibe eventos implícitos desde la interacción del usuario, ejecuta lógica de negocio y emite estados observables por la UI. En el proyecto esto se aprecia en `PlanosCubit` y `CapturaCubit`, que controlan carga de datos, modo continuo, detalle de punto, errores de envío y pausas por conectividad o throttling.

Para la visualización del plano se emplean `CustomPainter` e `InteractiveViewer`. El primero permite pintar sobre la superficie elementos como puntos de calibración, líneas de referencia y marcadores de medición. El segundo gestiona zoom y desplazamiento con conservación del contexto visual. Gracias a esta combinación, la coordenada seleccionada por el técnico se traduce a píxeles del plano real y no a coordenadas efímeras de pantalla.

La aplicación integra además tres complementos críticos: `wifi_scan` para obtener resultados de escaneo, `permission_handler` para gestionar permisos Android y `file_picker` para seleccionar planos desde el dispositivo. El cliente HTTP se implementa con Dio, que permite interceptores para JWT, reintentos con retroceso exponencial y manejo centralizado de errores de red. Sobre este flujo opera `ThrottlingManager`, responsable de respetar la restricción de Android 8.0 o superior de 4 escaneos cada 2 minutos.

En conjunto, estas decisiones sostienen la arquitectura móvil del proyecto: una app orientada a trabajo de campo, con interacción táctil sobre planos, captura en línea y separación clara entre presentación, lógica y acceso a datos.

### Referencias

Flutter. (2024). *Flutter — Documentación oficial*. Google. https://docs.flutter.dev/

Google. (2024). *Wi-Fi scan overview*. Android Developers. https://developer.android.com/develop/connectivity/wifi/wifi-scan

bloclibrary.dev. (2024). *bloc package documentation*. https://bloclibrary.dev/

---
