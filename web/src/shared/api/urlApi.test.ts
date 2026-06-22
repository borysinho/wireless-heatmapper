import { describe, expect, it } from "vitest";
import { resolverUrlApi } from "./urlApi";

describe("resolverUrlApi", () => {
  it("prefija las URLs firmadas relativas con /api", () => {
    expect(resolverUrlApi("/mapas/archivo/heatmap.png?exp=1&sig=firma")).toBe(
      "/api/mapas/archivo/heatmap.png?exp=1&sig=firma",
    );
  });

  it("acepta rutas relativas sin barra inicial", () => {
    expect(resolverUrlApi("mapas/archivo/heatmap.png")).toBe(
      "/api/mapas/archivo/heatmap.png",
    );
  });

  it("no duplica el prefijo /api", () => {
    expect(resolverUrlApi("/api/mapas/archivo/heatmap.png")).toBe(
      "/api/mapas/archivo/heatmap.png",
    );
  });

  it("conserva las URLs absolutas", () => {
    const url = "https://api.ejemplo.bo/mapas/archivo/heatmap.png";
    expect(resolverUrlApi(url)).toBe(url);
  });
});
