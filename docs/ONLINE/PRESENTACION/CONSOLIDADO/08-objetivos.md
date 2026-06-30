# 6. Objetivos del Proyecto

## 6.1 Objetivo General

Desarrollar un sistema integrado y estrictamente en línea, compuesto por una aplicación móvil para Android, un backend REST con módulo de inteligencia artificial y una plataforma web complementaria, que permita a los técnicos de **Bulldog Tech.** realizar el relevamiento, análisis y optimización de la cobertura de redes WiFi en espacios interiores mediante la generación de mapas de calor basados en mediciones reales transmitidas en tiempo real al backend y recomendaciones automáticas de posicionamiento de puntos de acceso apoyadas en algoritmos de aprendizaje automático; y que adicionalmente provea un panel de administración para la gestión organizacional de los técnicos y clientes y un portal de cliente para la visualización interactiva de los resultados entregados.

## 6.2 Objetivos Específicos

- **Analizar los requisitos del sistema** mediante el relevamiento del proceso actual de site survey de Bulldog Tech., la elaboración del Plan del Proyecto y la definición de los nueve requerimientos principales (RP1–RP9) que rigen el alcance funcional y no funcional del sistema.

- **Diseñar la arquitectura del sistema y la base de datos central** sobre los principios de cliente delgado en línea, separación clara en cuatro capas (presentación / aplicación / dominio / persistencia) y única fuente de verdad sobre PostgreSQL, materializada en los modelos UML de Contexto (casos de uso UC01–UC19), Arquitectura (paquetes y despliegue) y Datos (clases conceptuales, esquema lógico relacional y diseño físico).

- **Implementar el módulo de captura automática de parámetros de señal WiFi** (RSSI, SSID, BSSID, canal y frecuencia) durante el recorrido del espacio, transmitiendo cada muestra en línea al backend mediante endpoints REST autenticados con JWT, contemplando las restricciones de scan throttling impuestas por Android 8.0 y superiores.

- **Desarrollar la funcionalidad de importación y georreferenciación de planos** de edificios en formato PNG/JPG/PDF, almacenados de forma central en el backend, con calibración de escala mediante línea de referencia que permita asociar cada medición a una coordenada métrica sobre el plano.

- **Implementar algoritmos de interpolación espacial** ejecutados en el backend (interpolación de distancia inversa ponderada y/o kriging) para generar mapas de calor continuos sobre el plano del edificio.

- **Desarrollar el módulo de análisis automatizado de cobertura**, capaz de identificar zonas muertas (RSSI < −90 dBm), interferencias entre canales (CCI/ACI) y solapamientos entre puntos de acceso, conforme a los umbrales del marco CWNA-107.

- **Aplicar técnicas de inteligencia artificial** para la recomendación de posicionamiento óptimo de puntos de acceso garantizando cobertura objetivo ≥ −70 dBm, expuestas vía endpoint REST consumido tanto por la app móvil como por el portal de cliente.

- **Implementar la generación de reportes técnicos exportables** (PDF) que documenten la cobertura relevada, el análisis automático y el plan de implementación de APs propuesto.

- **Desarrollar el panel de administración web** que permita gestionar las cuentas de los técnicos (alta, baja y activación), administrar el catálogo de clientes y supervisar la totalidad de los proyectos de la organización con su estado y actividad reciente.

- **Desarrollar el portal de cliente web** que permita visualizar de forma interactiva los mapas de calor (actual y proyectado), el análisis de cobertura y el plan de APs recomendado, accesible mediante un enlace único generado por el técnico al cierre del proyecto.

- **Validar la efectividad del software** mediante pruebas unitarias y de integración (cobertura de código ≥ 80 % en backend), pruebas de aceptación con el Product Owner por cada Sprint, y pruebas de campo en instalaciones reales del cliente Bulldog Tech.
