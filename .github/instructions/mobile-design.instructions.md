---
description: "Use when creating or modifying Flutter UI screens, pages, widgets, forms, banners, error feedback, or any visual/interaction design in the mobile app (Wireless HeatMapper). Covers Material 3 palette with light+dark themes, Poppins/Inter typography, design tokens (AppSpacing/AppRadius/AppPalette), shared widgets in lib/shared/widgets/, navigation, splash, branding with logo asset, and loading/error/empty states."
applyTo: "mobile/**/presentation/**/*.dart"
---

# Diseño Mobile — Wireless HeatMapper

Convenciones visuales e interactivas para **todas las pantallas y widgets** de la app móvil.
Complementa [flutter-mobile.instructions.md](flutter-mobile.instructions.md), que cubre arquitectura, BLoC/Cubit y pruebas.

---

## Tema base — Material 3

- Único punto de definición del tema: [`lib/core/theme/app_theme.dart`](../../mobile/lib/core/theme/app_theme.dart).
- `MaterialApp.router` debe declarar **siempre** `theme: AppTheme.light`, `darkTheme: AppTheme.dark` y `themeMode: ThemeMode.system`.
- Color semilla del producto: `kSeedColor` (`Color(0xFF2980B9)`) — exportado desde [`app_tokens.dart`](../../mobile/lib/core/theme/app_tokens.dart).
- **Nunca** instanciar `ThemeData` ni `ColorScheme.fromSeed` en widgets de feature; consumir el tema activo vía `Theme.of(context)`.
- No activar `debugShowCheckedModeBanner`.

```dart
// ✅ Correcto — app.dart
MaterialApp.router(
  theme: AppTheme.light,
  darkTheme: AppTheme.dark,
  themeMode: ThemeMode.system,
  routerConfig: AppRouter.router,
)
```

---

## Tipografía — Poppins (títulos) + Inter (cuerpo)

Definida en `AppTheme._buildTextTheme`. **No usar `GoogleFonts.*` directamente en widgets**: consumir `Theme.of(context).textTheme.*`.

| Rol visual                      | Estilo                 | Fuente           |
| ------------------------------- | ---------------------- | ---------------- |
| Display (hero, splash)          | `displayLarge/Medium`  | Poppins Bold     |
| Título de sección / encabezados | `headlineSmall/Medium` | Poppins SemiBold |
| Título de tarjeta / `AppBar`    | `titleLarge/Medium`    | Poppins SemiBold |
| Cuerpo (formularios, listas)    | `bodyLarge/Medium`     | Inter Regular    |
| Etiquetas auxiliares            | `bodySmall`            | Inter Regular    |
| Botones (heredado del tema)     | `labelLarge`           | Inter SemiBold   |

```dart
// ✅ Correcto
Text(proyecto.nombre, style: Theme.of(context).textTheme.titleMedium)

// ❌ Incorrecto — bypass del tema
Text(proyecto.nombre, style: GoogleFonts.poppins(fontWeight: FontWeight.bold))
```

---

## Tokens de diseño — `app_tokens.dart`

Importar y consumir **siempre** estos tokens en lugar de literales.

### Espaciado (`AppSpacing`)

| Token  | Valor | Uso típico                                |
| ------ | ----- | ----------------------------------------- |
| `xs`   | 4 px  | Separación micro entre badge y texto      |
| `sm`   | 8 px  | Separación entre ícono y label            |
| `md`   | 16 px | Separación estándar entre controles       |
| `lg`   | 24 px | Padding de páginas internas / formularios |
| `xl`   | 32 px | Padding horizontal de pantalla de entrada |
| `xxl`  | 40 px | Padding vertical de pantalla de entrada   |
| `xxxl` | 48 px | Separación entre branding y formulario    |

### Radios (`AppRadius`)

| Token  | Valor  | Uso                            |
| ------ | ------ | ------------------------------ |
| `sm`   | 8 px   | Inputs, botones, banners       |
| `md`   | 12 px  | Cards, contenedores destacados |
| `lg`   | 16 px  | Diálogos                       |
| `pill` | 999 px | Badges, chips                  |

### Paleta semántica (`AppPalette.estadoColor`)

- Mapea `EstadoProyecto` a colores derivados del `ColorScheme` activo (no hardcodea).
- Usar para cualquier indicador de estado (badges, hilos de timeline futuros).

---

## Paleta de colores — todo viene del `ColorScheme`

**Prohibido**: `Colors.red`, `Colors.grey`, `Color(0xFF...)` para estados, errores o texto. Toda diferenciación visual debe derivarse de `Theme.of(context).colorScheme`.

| Uso                          | Token                             |
| ---------------------------- | --------------------------------- |
| Acción primaria / focus      | `colorScheme.primary`             |
| Texto sobre primario         | `colorScheme.onPrimary`           |
| Fondo de avatar destacado    | `colorScheme.primaryContainer`    |
| Error (texto, ícono, borde)  | `colorScheme.error`               |
| Texto sobre error            | `colorScheme.onError`             |
| Fondo de banner sin conexión | `colorScheme.errorContainer`      |
| Texto sobre errorContainer   | `colorScheme.onErrorContainer`    |
| Texto muted / subtítulos     | `colorScheme.onSurfaceVariant`    |
| Bordes sutiles               | `colorScheme.outlineVariant`      |
| Bordes neutros / archivado   | `colorScheme.outline`             |
| Fondo de card                | `colorScheme.surfaceContainerLow` |

Todos estos tokens se invierten automáticamente en dark mode.

---

## Componentes reutilizables — `lib/shared/widgets/`

Antes de crear UI nueva, verificar si existe un componente. **No duplicar patrones.**

| Widget                | Cuándo usarlo                                                                        |
| --------------------- | ------------------------------------------------------------------------------------ |
| `AppBrandingHeader`   | Cabecera de marca (logo + producto + cliente). Login, splash, vacíos heroicos.       |
| `AppLoadingButton`    | Botón primario con `isLoading` integrado. Reemplaza `FilledButton + spinner` manual. |
| `AppEmptyState`       | Pantalla/sección vacía con ícono + mensaje + acción opcional.                        |
| `AppErrorState`       | Pantalla de error con botón "Reintentar".                                            |
| `AppConnectionBanner` | Banner persistente "Sin conexión" — colores derivados del tema.                      |
| `AppEstadoBadge`      | Badge de estado de proyecto. Usa `AppPalette.estadoColor`.                           |

```dart
// ✅ Correcto
AppLoadingButton(
  label: 'Crear proyecto',
  isLoading: state is ProyectoLoading,
  onPressed: _guardar,
)

// ❌ Incorrecto — duplicación del patrón
FilledButton(
  onPressed: cargando ? null : _guardar,
  child: cargando
      ? const SizedBox(width: 20, height: 20,
          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
      : const Text('Crear proyecto'),
)
```

---

## Estructura de pantalla

### Pantalla de entrada (login, splash)

```dart
Scaffold(
  body: SafeArea(
    child: Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.xl,
          vertical: AppSpacing.xxl,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: const [
            AppBrandingHeader(logoSize: 96),
            SizedBox(height: AppSpacing.xxxl),
            // ... formulario ...
          ],
        ),
      ),
    ),
  ),
)
```

### Pantalla interna (lista, formulario, detalle)

- **Sí** usar `AppBar` con título descriptivo.
- Padding del cuerpo: `EdgeInsets.all(AppSpacing.lg)` para formularios.
- Listas con `RefreshIndicator` para pull-to-refresh.
- Búsqueda de listas con **debounce de 300 ms** (ver [`proyectos_page.dart`](../../mobile/lib/features/proyectos/presentation/pages/proyectos_page.dart) como referencia).
- `SafeArea` siempre.
- `CrossAxisAlignment.stretch` cuando los hijos sean botones o inputs full-width.

---

## Branding e identidad visual

- Logo: [`mobile/img/logo.png`](../../mobile/img/logo.png), monograma "B" de Bulldog Tech (registrado como asset en [pubspec.yaml](../../mobile/pubspec.yaml)).
- **Nunca** consumir el logo directamente con `Image.asset`: usar `AppBrandingHeader`, que aplica `ColorFiltered` para invertir el monograma en dark mode.
- Nombre del producto: `'Wireless HeatMapper'` (Poppins Bold).
- Cliente: `'Bulldog Tech.'` — punto final es parte del nombre, no omitirlo.
- Posición canónica: logo → producto → cliente → `SizedBox(height: AppSpacing.xxxl)` → contenido.

---

## Formularios

- Usar `flutter_form_builder` (`FormBuilder` + `FormBuilderTextField`) para entradas con validación declarativa.
- Para formularios simples (creación/edición de entidades) se permite `Form + TextFormField` nativo.
- Todos los campos de texto **deben** tener:
  - `labelText` en español.
  - `prefixIcon` representativo del campo.
  - `textInputAction` correcto (`next` para campos intermedios, `done` para el último).
- El `OutlineInputBorder` y los estilos de input vienen del `inputDecorationTheme`; no redefinir manualmente.
- Campos de contraseña: incluir `suffixIcon` con `IconButton` para alternar visibilidad.
- Deshabilitar campos con `enabled: !bloqueado` durante carga o sin conexión.
- Validadores devuelven mensajes en español, sin revelar información sensible (no distinguir email vs contraseña en login).

---

## Estados de carga, vacío y error

- **Cargando lista**: `CircularProgressIndicator` centrado.
- **Cargando acción**: `AppLoadingButton(isLoading: true)`.
- **Vacío**: `AppEmptyState`.
- **Error completo (sin datos previos)**: `AppErrorState` con `Reintentar`.
- **Error sobre datos cargados**: `SnackBar` con `SnackBarAction(label: 'Reintentar', ...)`.
- Nunca dos indicadores de carga simultáneos.

### SnackBar de error con acción

```dart
ScaffoldMessenger.of(context)
  ..hideCurrentSnackBar()
  ..showSnackBar(SnackBar(
    content: Text(state.mensaje),
    backgroundColor: Theme.of(context).colorScheme.error,
    action: SnackBarAction(
      label: 'Reintentar',
      textColor: Theme.of(context).colorScheme.onError,
      onPressed: () => context.read<MyCubit>().recargar(),
    ),
  ));
```

`behavior: SnackBarBehavior.floating` y `shape` ya vienen del `snackBarTheme`; **no** repetirlos en cada llamada.

### Banner de sin conexión

```dart
if (sinConexion) ...[
  const AppConnectionBanner(),
  const SizedBox(height: AppSpacing.md),
],
```

---

## Diálogos

- Toda confirmación destructiva (eliminar, logout, archivar) debe tener:
  - `icon:` arriba (Material 3) — `Icons.delete_forever_outlined` con `colorScheme.error` para destructivas; `Icons.logout_rounded` para logout; `Icons.archive_outlined` para archivar.
  - Botón cancelar = `TextButton`.
  - Botón confirmar = `FilledButton`. Para destructivos, `style: FilledButton.styleFrom(backgroundColor: scheme.error, foregroundColor: scheme.onError)`.
- El radio del diálogo viene del `dialogTheme` (`AppRadius.lg`); no sobrescribir.

---

## Navegación

- Usar **`go_router`** para toda la navegación. Las rutas se definen en [`app_router.dart`](../../mobile/lib/core/navigation/app_router.dart).
- Pantalla inicial = `/splash` (muestra `AppBrandingHeader` mientras se valida sesión).
- `context.go('/ruta')` para reemplazar (login, logout, splash → siguiente).
- `context.push('/ruta')` para apilar (formulario, detalle).
- Redirecciones post-login y post-logout ocurren en `BlocListener`s, no en el Cubit.
- **Logout**: invocar `AuthCubit.logout()` para borrar el JWT del `flutter_secure_storage`. **Nunca** hacer `context.go('/login')` directo (deja la sesión activa). El listener navega cuando emite `AuthUnauthenticated`.

---

## Dark mode

- El tema oscuro está siempre activo (`themeMode: system`). Toda decisión visual debe ser correcta en ambos modos.
- Validar contraste manualmente al crear pantallas nuevas.
- Para imágenes con un solo tono (logo monocromo), usar `ColorFiltered` con matriz de inversión cuando `Theme.of(context).brightness == Brightness.dark` (ver `AppBrandingHeader` como referencia).

---

## Qué evitar

- `Colors.red/grey/blue/orange/green/etc` o `Color(0xFF...)` hardcodeados — usar `colorScheme`.
- `EdgeInsets`/`SizedBox` con literales — usar `AppSpacing`.
- `BorderRadius.circular(8)` con literales — usar `AppRadius`.
- `GoogleFonts.*` directo en widgets — usar `Theme.of(context).textTheme`.
- `Image.asset('img/logo.png')` directo — usar `AppBrandingHeader`.
- `withOpacity()` — usar `withValues(alpha: ...)`.
- Duplicar el patrón "spinner dentro de botón" — usar `AppLoadingButton`.
- Lógica de negocio o llamadas HTTP dentro de widgets.
- Mensajes de error con detalles internos (trazas, nombres de campo en login).
- `context.go('/login')` para "cerrar sesión" sin invocar `AuthCubit.logout()`.

---

## Roadmap visual (Sprints 2-5)

- **Editor de plano** (`PlanoEditorPage`, Sp2-07): pines de medición coloreados según umbrales CWNA-107:
  - `≥ -70 dBm` → `colorScheme.tertiary` (verde — calidad buena).
  - `-70 a -90 dBm` → `colorScheme.error.withValues(alpha: 0.7)` o color ámbar derivado (calidad aceptable).
  - `< -90 dBm` → `colorScheme.error` (calidad mala).
- **Detalle de proyecto**: layout split (resumen arriba, lista de planos debajo), reutilizar `AppEmptyState`/`AppErrorState`.
- **Captura/heatmap**: introducir `MedicionChip` y `RssiIndicator` reutilizables en `lib/shared/widgets/`.
