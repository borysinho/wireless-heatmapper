## 3.4 Desarrollo Web con React 18 y TypeScript

React 18 estructura la interfaz mediante componentes funcionales y *hooks* (ganchos) que encapsulan estado, efectos y memorias derivadas. `useState` gestiona datos locales, `useEffect` sincroniza la vista con cambios externos, `useContext` distribuye información transversal como autenticación, y `useCallback` ayuda a estabilizar referencias de función cuando el componente lo requiere. Este modelo es adecuado para un panel administrativo que combina formularios, tablas, navegación y consumo intensivo de API.

TypeScript agrega tipado estático sobre JavaScript. En un sistema como Wireless HeatMapper, donde backend, móvil y web comparten conceptos de dominio, las interfaces tipadas reducen ambigüedad en contratos de datos y mejoran la detección temprana de errores. Los *type guards* (guardas de tipo) permiten validar estructuras en tiempo de ejecución cuando la información proviene del servidor o de entradas externas.

La arquitectura del panel corresponde a una *Single Page Application* (SPA, aplicación de página única). El enrutamiento ocurre del lado del cliente y evita recargas completas para operaciones internas de administración. Cuando un módulo no es requerido de inmediato, puede cargarse mediante división de código con `React.lazy`, lo que reduce el volumen inicial transferido al navegador.

El estado del servidor se administra con TanStack Query. La biblioteca conserva resultados en caché, usa `queryKey` para identificar recursos, controla vigencia con `staleTime` y simplifica invalidaciones después de mutaciones como creación o edición. Esta aproximación evita duplicar en estado local información cuyo origen autorizado sigue siendo el backend. En términos prácticos, mejora consistencia y reduce solicitudes redundantes.

Vite complementa el flujo con compilación rápida y *Hot Module Replacement* (HMR, reemplazo de módulos en caliente) durante el desarrollo. En producción, el empaquetado aprovecha optimizaciones como *tree shaking* (eliminación de código no usado), lo que favorece entregas ligeras del frontend. Sobre esa base se monta el contexto de autenticación del panel, encargado de almacenar el token, proteger rutas y coordinar el mecanismo de renovación cuando corresponde.

Esta fundamentación se refleja en la arquitectura del panel web del proyecto, especialmente en páginas como Login, Dashboard, Users, Organizations y Projects, que operan como una interfaz administrativa coherente sobre el mismo backend REST utilizado por la app móvil.

### Referencias

Microsoft. (2024). *TypeScript documentation*. https://www.typescriptlang.org/docs/

React. (2024). *React — Documentación oficial*. Meta Open Source. https://react.dev/

TanStack. (2024). *TanStack Query documentation*. https://tanstack.com/query/latest

Vite. (2024). *Vite guide*. https://vite.dev/guide/

---
