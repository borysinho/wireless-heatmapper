## 3.5 React y TypeScript para la Plataforma Web

### 3.5.1 React como librería de UI

**React** (versión 18) es la librería JavaScript de código abierto desarrollada por Meta para construir interfaces de usuario declarativas basadas en componentes reutilizables (Meta Open Source, 2023). React fue seleccionado para el Wireless HeatMapper por su madurez, su ecosistema de librerías complementarias y su adopción masiva en la industria, que garantiza soporte y mantenimiento a largo plazo.

El modelo de programación de React se basa en:

- **Componentes funcionales:** la UI se describe como funciones puras que reciben `props` (propiedades inmutables) y devuelven JSX (una descripción declarativa del árbol DOM a renderizar).
- **Hooks:** funciones especiales (`useState`, `useEffect`, `useCallback`) que permiten añadir estado local y efectos secundarios a los componentes funcionales.
- **Virtual DOM:** React mantiene una representación virtual del DOM en memoria y aplica solo los cambios mínimos necesarios al DOM real cuando el estado cambia, minimizando las operaciones de renderizado costosas.

### 3.5.2 TypeScript para tipado estático

**TypeScript** (versión 5.x) es el superconjunto tipado de JavaScript utilizado en toda la base de código web del Wireless HeatMapper. TypeScript añade un sistema de tipos estáticos que se verifica en tiempo de compilación —antes de que el código se ejecute en el navegador— eliminando una clase entera de errores (propiedades inexistentes, argumentos con tipo incorrecto, valores `undefined` no manejados) que en JavaScript puro solo se detectarían en tiempo de ejecución (Microsoft, 2023).

Las ventajas concretas de TypeScript en el proyecto son:

- **Tipado de respuestas de la API:** los tipos de las respuestas del backend (generados automáticamente desde la especificación OpenAPI con `openapi-typescript`) garantizan que si el backend cambia un campo, el compilador TypeScript señala todos los lugares del frontend que deben actualizarse.
- **Refactoring seguro:** renombrar un componente, una función o una interfaz actualiza automáticamente todas sus referencias con el soporte del editor.
- **Documentación implícita:** los tipos de los props y los parámetros de las funciones documentan el contrato de uso de cada componente sin necesidad de comentarios adicionales.

### 3.5.3 Vite como herramienta de build

**Vite** (versión 5.x) es la herramienta de build y servidor de desarrollo utilizada. A diferencia del webpack tradicional, Vite utiliza ESModules nativos del navegador durante el desarrollo (sin bundle) y Rollup para el build de producción, lo que produce tiempos de arranque del servidor de desarrollo de menos de 300 ms —independientemente del tamaño del proyecto— y tiempos de hot module replacement (HMR) de menos de 50 ms (Evan You, 2023).

### 3.5.4 TanStack Query para gestión del estado del servidor

**TanStack Query** (anteriormente React Query) gestiona el estado del servidor en el frontend: caching de respuestas, revalidación automática, paginación y manejo de estados de carga y error para todas las peticiones a la API REST. Su uso elimina la necesidad de un store global (Redux) para la mayoría de los datos, ya que TanStack Query actúa como caché inteligente que sincroniza el estado del servidor con la UI: si el backend tiene datos nuevos, la UI se actualiza automáticamente (Tanners Linsley, 2023).

En el panel de administración del Wireless HeatMapper, TanStack Query gestiona:

- La lista paginada de técnicos (con invalidación automática al crear o desactivar uno).
- El catálogo de clientes (compartido entre la vista de administración y el selector de clientes en la app móvil via la misma API).
- El listado consolidado de proyectos de la organización con filtros por técnico y estado.
