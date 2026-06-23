import axios from "axios";
import type { MapaCalorPortalOut, PortalClienteOut } from "@/features/admin/types";

const portalClient = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

export async function obtenerPortalCliente(
  token: string,
): Promise<PortalClienteOut> {
  const { data } = await portalClient.get<PortalClienteOut>(`/share/${token}`);
  return data;
}

export async function generarHeatmapPortal(
  token: string,
  conjuntoId: number,
  body: {
    modo: "INDIVIDUAL" | "SUBCONJUNTO" | "CONJUNTO_COMPLETO";
    bssids?: string[];
    algoritmo: "IDW" | "KRIGING";
    resolucion: 64 | 128 | 256;
  },
): Promise<MapaCalorPortalOut> {
  const { data } = await portalClient.post<MapaCalorPortalOut>(
    `/share/${token}/conjuntos/${conjuntoId}/heatmaps`,
    body,
  );
  return data;
}
