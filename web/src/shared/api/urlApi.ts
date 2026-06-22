/**
 * Convierte una URL relativa devuelta por el backend en una URL consumible
 * desde la web. En desarrollo y producción, `/api` es el punto de entrada al
 * proxy; las URLs absolutas ya incluyen su origen público y no se modifican.
 */
export function resolverUrlApi(url: string): string {
  if (/^https?:\/\//i.test(url) || url.startsWith("data:") || url.startsWith("blob:")) {
    return url;
  }

  const ruta = url.startsWith("/") ? url : `/${url}`;
  return ruta === "/api" || ruta.startsWith("/api/") ? ruta : `/api${ruta}`;
}
