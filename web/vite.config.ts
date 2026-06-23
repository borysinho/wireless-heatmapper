import { defineConfig } from "vitest/config";
import { loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { existsSync, readFileSync, statSync } from "fs";
import { extname, join, resolve } from "path";

const tiposContenido: Record<string, string> = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
};

function servirManualUsuarioDev() {
  const manualRoot = resolve(__dirname, "../manual-usuario");

  return {
    name: "manual-usuario-dev",
    configureServer(server) {
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
