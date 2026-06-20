---
description: "Use when creating or modifying UI components, CSS Modules, color tokens, layout, typography, spacing, forms, tables, badges, modals, or any visual/interaction design in the web frontend (React + TypeScript) of Wireless HeatMapper. Applies to admin panel and client portal."
applyTo: "web/**/*.{tsx,css}"
---

# Diseño Frontend — Wireless HeatMapper Web

Convenciones visuales e interactivas para **todas las vistas web** (panel admin + portal de cliente). Complementa [react-web.instructions.md](react-web.instructions.md) que cubre arquitectura y estado.

---

## Estilado: CSS Modules

- **Siempre** usar CSS Modules (`.module.css` por archivo de componente/página) como base.
- No usar estilos inline salvo valores calculados dinámicamente en JS.
- Tailwind CSS o Material UI se permiten con justificación explícita en PR; no son el default.
- Nombres de clases en **español**, camelCase: `.botonPrimario`, `.encabezado`, `.alerta`.

---

## Paleta de colores — usar variables CSS de `index.css`

Los componentes **deben referenciar las custom properties** definidas en `src/index.css`, no colores hardcodeados. Esto garantiza soporte correcto de dark mode (`prefers-color-scheme: dark`).

### Tokens de superficie y texto

| Token              | Uso principal                    | Valor light  |
| ------------------ | -------------------------------- | ------------ |
| `var(--bg)`        | Fondo de tarjetas                | `#fff`       |
| `var(--bg-page)`   | Fondo de página/layout           | `#f0f4f8`    |
| `var(--bg-surface)`| Fondo de cabeceras de tabla      | `#f7fafc`    |
| `var(--text)`      | Texto corriente                  | `#4a5568`    |
| `var(--text-h)`    | Títulos y encabezados            | `#1a202c`    |
| `var(--text-muted)`| Subtítulos, placeholders         | `#718096`    |
| `var(--border)`    | Bordes de inputs, divisores      | `#e2e8f0`    |
| `var(--border-light)`| Divisores de filas de tabla    | `#f0f4f8`    |
| `var(--shadow-sm)` | Sombra suave de tarjetas         | ver index.css|
| `var(--shadow-md)` | Sombra modal y dropdowns         | ver index.css|
| `var(--shadow-lg)` | Sombra de modales primarios      | ver index.css|

### Tokens semánticos de color

| Token                        | Uso                               |
| ---------------------------- | --------------------------------- |
| `var(--color-primary)`       | Botón primario, focus, links      |
| `var(--color-primary-hover)` | Hover del botón primario          |
| `var(--color-primary-bg)`    | Fondo de elementos activos        |
| `var(--color-danger)`        | Error, destrucción                |
| `var(--color-danger-bg)`     | Fondo de alertas de error         |
| `var(--color-danger-border)` | Borde de alertas de error         |
| `var(--color-success)`       | Confirmación, activo              |
| `var(--color-success-bg)`    | Fondo de badge activo             |
| `var(--color-success-border)`| Borde de badge activo             |
| `var(--color-info)`          | Información, admin, en_progreso   |
| `var(--color-info-bg)`       | Fondo de badge info               |
| `var(--color-info-border)`   | Borde de badge info               |
| `var(--color-warning)`       | Archivado, advertencia            |
| `var(--color-warning-bg)`    | Fondo de badge warning            |
| `var(--color-warning-border)`| Borde de badge warning            |
| `var(--color-muted-bg)`      | Fondo de badge neutro             |
| `var(--color-muted-text)`    | Texto de badge neutro             |

### Tokens de navegación

| Token                   | Uso                              |
| ----------------------- | -------------------------------- |
| `var(--nav-bg)`         | Fondo del sidebar                |
| `var(--nav-text)`       | Texto de ítems de nav            |
| `var(--nav-text-active)`| Texto del ítem activo            |
| `var(--nav-item-hover)` | Fondo hover de ítem de nav       |
| `var(--nav-item-active)`| Fondo del ítem activo            |

### Tokens de radio y transición

| Token                | Valor    |
| -------------------- | -------- |
| `var(--radius-sm)`   | `5px`    |
| `var(--radius-md)`   | `6px`    |
| `var(--radius-lg)`   | `10px`   |
| `var(--radius-xl)`   | `12px`   |
| `var(--radius-pill)` | `999px`  |
| `var(--transition-fast)` | `0.15s` |

---

## Iconografía — lucide-react obligatorio

- **Usar siempre `lucide-react`** para iconos de UI (navegación, acciones, estados vacíos). No usar emojis en la interfaz.
- Tamaño estándar: `size={18}` en navegación/botones, `size={14}` en acciones de tabla, `size={40}` en estados vacíos.
- `strokeWidth={1.5}` para iconos decorativos o de gran tamaño; `strokeWidth` por defecto (`2`) para acciones.
- Siempre incluir `aria-hidden="true"` en iconos decorativos.

```tsx
// Correcto
import { Archive, UserCog } from "lucide-react";
<Archive size={14} aria-hidden="true" />

// Incorrecto
<span>🗂️</span>
```

---

## Componentes compartidos — `@/shared/components`

Antes de crear un botón, badge, modal de confirmación o estado vacío custom, **usar los primitivos existentes**:

| Componente      | Props clave                                                  |
| --------------- | ------------------------------------------------------------ |
| `<Button>`      | `variante?: "primary"\|"secondary"\|"danger"\|"ghost"`, `tamano?: "sm"\|"md"\|"lg"`, `isLoading?`, `fullWidth?` |
| `<Badge>`       | `variante: "activo"\|"inactivo"\|"admin"\|"tecnico"\|"en_progreso"\|"completado"\|"archivado"\|"neutro"`, `etiqueta?`, `icono?` |
| `<EmptyState>`  | `mensaje?`, `icono?`                                         |
| `<ConfirmDialog>` | `titulo`, `descripcion?`, `textoConfirmar?`, `textoCancelar?`, `peligroso?`, `cargando?`, `onCancelar`, `onConfirmar` |
| `useToast()`    | `exito(msg)`, `error(msg)`, `info(msg)`                      |
| `<ToastContainer>` | Sin props — colocar una sola vez en el layout raíz       |

### Regla crítica: no usar `window.confirm()`

Toda acción destructiva (desactivar, archivar, eliminar) debe usar `<ConfirmDialog>` controlado por estado:

```tsx
// Patrón correcto
const [itemDesactivar, setItemDesactivar] = useState<ItemType | null>(null);

// En JSX de la fila:
<Button variante="danger" tamano="sm" onClick={() => setItemDesactivar(item)}>
  Desactivar
</Button>

// Al final del JSX:
{itemDesactivar && (
  <ConfirmDialog
    titulo={`¿Desactivar "${itemDesactivar.nombre}"?`}
    onCancelar={() => setItemDesactivar(null)}
    onConfirmar={async () => { await desactivar(itemDesactivar.id); setItemDesactivar(null); }}
  />
)}
```

---

## Responsive obligatorio

Toda vista debe funcionar correctamente en **tres puntos de quiebre**:

| Breakpoint  | Ancho       | Comportamiento esperado                                    |
| ----------- | ----------- | ---------------------------------------------------------- |
| Desktop     | > 1024px    | Layout completo con sidebar visible                        |
| Tablet      | ≤ 1024px    | Sidebar comprimido (200px), contenido ajustado             |
| Mobile      | ≤ 768px     | Sidebar oculto por defecto; drawer con overlay al abrir    |
| Small mobile| ≤ 480px     | Columnas de tabla menos relevantes ocultas; modales full-width |

- El sidebar admin usa `transform: translateX(-100%)` en mobile con transición `0.25s`.
- Tablas: `overflow-x: auto` + `min-width` para scroll horizontal en móvil.
- Modales: `width: 100%; max-width: NNNpx; padding: 1rem` en el overlay para mobile.

---

## Tipografía

- Usar la fuente del sistema definida en `:root` (`var(--sans)`, `var(--heading)`). No importar Google Fonts sin consenso.
- Jerarquía de tamaños establecida:
  - Título de página: `1.4–1.5rem`, `font-weight: 700`, color `var(--text-h)`.
  - Subtítulo / descripción: `0.9rem`, color `var(--text-muted)`.
  - Etiquetas de formulario: `0.875rem`, `font-weight: 500 o 600`.
  - Texto de tabla: `0.9rem`.
  - Badges / etiquetas pequeñas: `0.8rem`, `font-weight: 600`.

---

## Espaciado y dimensiones

- Usar unidades `rem` para márgenes, padding y tamaños de fuente; `px` solo para bordes y sombras.
- Tarjetas: `border-radius: var(--radius-xl)`, `padding: 2rem–2.5rem`.
- Botones e inputs: `border-radius: var(--radius-md)`.
- Badges de estado: `border-radius: var(--radius-pill)`.

---

## Componentes de formulario

- Todo `<input>` debe tener `id` único y `<label htmlFor>` asociado (accesibilidad).
- Estado de foco: `outline: 2px solid var(--color-primary); background: var(--color-primary-bg)`.
- Mensajes de error/validación: usar `role="alert"` y clase `.alerta`.
- Nunca deshabilitar `autocomplete` en campos de credenciales; asignar `autoComplete="username"` / `"current-password"` correctamente.
- Validación de cliente antes de llamada HTTP; nunca dejar el form sin feedback visible.

---

## Interacciones y transiciones

- Transiciones: usar `transition: background var(--transition-fast), color var(--transition-fast)`.
- No usar `transition: all` — es costoso y opaco.
- Botones primarios: `background: var(--color-primary)` → hover `var(--color-primary-hover)`.

---

## Tablas de datos

Patrón estándar:

```css
.tablaWrapper {
  background: var(--bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow-x: auto;
}
.tabla th {
  background: var(--bg-surface);
  color: var(--text);
  font-weight: 600;
  border-bottom: 1px solid var(--border);
}
.tabla td {
  border-bottom: 1px solid var(--border-light);
}
.tabla tr:last-child td {
  border-bottom: none;
}
```

- Última fila sin borde inferior.
- `overflow-x: auto` en el wrapper para responsividad horizontal.
- Incluir `min-width` en la tabla para garantizar scroll en mobile.

---

## Accesibilidad mínima obligatoria

- `role="alert"` en mensajes de error que aparecen dinámicamente.
- `aria-label` en botones cuyo texto es solo un ícono.
- `aria-hidden="true"` en iconos decorativos dentro de botones con texto.
- `role="dialog" aria-modal="true" aria-labelledby="id-titulo"` en todos los modales.
- Navegación por teclado funcional en formularios y tablas críticas.
- No usar colores como único indicador de estado (acompañar con texto o ícono).

---

## Idioma de la UI

Todos los textos visibles al usuario van en **español (es-BO)**:

- Etiquetas, placeholders, mensajes de error, tooltips, títulos de columna.
- Mensajes de estados vacíos: "No hay registros aún."
- Mensajes de carga: "Cargando…" (puntos suspensivos Unicode `…`, no `...`).

---

## Anti-patrones

- No usar `style={{ color: '#...' }}` hardcodeado en JSX para tokens que ya existen en CSS.
- No omitir estados de carga, vacío y error en vistas que consumen datos del servidor.
- No usar `window.confirm()` — usar siempre `<ConfirmDialog>`.
- No usar emojis como iconos de UI — usar siempre `lucide-react`.
- No mezclar lógica de negocio dentro del CSS; usar `style` inline solo para valores calculados en JS.
