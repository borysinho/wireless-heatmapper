import { defineConfig } from "vitest/config";
import { loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import type { ServerResponse } from "http";
import type { ViteDevServer } from "vite";
import { existsSync, readFileSync, statSync } from "fs";
import { extname, join, resolve } from "path";

const tiposContenido: Record<string, string> = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
};

function resolverManualRoot(): string | null {
  const candidatos = [
    process.env.VITE_MANUAL_USUARIO_ROOT,
    resolve(__dirname, "../manual-usuario"),
    resolve(__dirname, "manual-usuario"),
    "/app/manual-usuario",
  ].filter((ruta): ruta is string => Boolean(ruta));

  return candidatos.find((ruta) => existsSync(join(ruta, "index.html"))) ?? null;
}

function responderManualNoDisponible(res: ServerResponse) {
  res.statusCode = 404;
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.end(`<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <title>Manual no disponible</title>
  </head>
  <body style="font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.5;">
    <h1>Manual de usuario no disponible</h1>
    <p>El servidor de desarrollo no encontro <code>manual-usuario/index.html</code>.</p>
    <p>Si estas usando Docker, verifica que <code>./manual-usuario</code> este montado en <code>/app/manual-usuario</code>.</p>
  </body>
</html>`);
}

function servirManualUsuarioDev() {
  return {
    name: "manual-usuario-dev",
    configureServer(server: ViteDevServer) {
      server.middlewares.use((req, res, next) => {
        const url = req.url ?? "";
        const pathname = decodeURIComponent(new URL(url, "http://localhost").pathname);

        if (pathname === "/manual") {
          res.statusCode = 302;
          res.setHeader("Location", "/manual/");
          res.end();
          return;
        }

        if (!pathname.startsWith("/manual/")) {
          next();
          return;
        }

        const manualRoot = resolverManualRoot();

        if (!manualRoot) {
          responderManualNoDisponible(res);
          return;
        }

        const relativo = pathname.replace(/^\/manual\/?/, "") || "index.html";
        let archivo = resolve(manualRoot, relativo);

        if (!archivo.startsWith(manualRoot)) {
          res.statusCode = 403;
          res.end("Ruta no permitida.");
          return;
        }

        if (existsSync(archivo) && statSync(archivo).isDirectory()) {
          archivo = join(archivo, "index.html");
        }

        if (!existsSync(archivo)) {
          archivo = join(manualRoot, "index.html");
        }

        res.setHeader(
          "Content-Type",
          tiposContenido[extname(archivo)] ?? "application/octet-stream",
        );
        res.end(readFileSync(archivo));
      });
    },
  };
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Carga variables de entorno del directorio raíz del proyecto web.
  // VITE_PROXY_TARGET permite redirigir el proxy del servidor de desarrollo
  // a un host remoto sin modificar el código fuente.
  // Ejemplo: VITE_PROXY_TARGET=http://10.138.57.250:8000 en web/.env.local
  const env = loadEnv(mode, process.cwd(), "VITE_");
  const proxyTarget = env.VITE_PROXY_TARGET ?? "http://localhost:8000";

  return {
    plugins: [react(), servirManualUsuarioDev()],
    resolve: {
      alias: {
        "@": resolve(__dirname, "src"),
      },
    },
    server: {
      proxy: {
        "/api": {
          target: proxyTarget,
          changeOrigin: true,
          // Elimina el prefijo /api/ para alinear con el proxy Nginx de producción
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: ["src/test/setup.ts"],
      coverage: {
        provider: "v8",
        reporter: ["text", "lcov"],
      },
    },
  };
});
