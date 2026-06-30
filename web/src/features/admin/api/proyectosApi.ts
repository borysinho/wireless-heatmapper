/** Llamadas a la API de proyectos para el admin. Sprint 1 — PB-18. */

import { apiClient } from "@/shared/api/client";
import type {
  APDisponibleOut,
  ConjuntosIAGeneradosOut,
  ConjuntoAPOut,
  EnlaceClienteCrearIn,
  EnlaceClienteEnviarCorreoIn,
  EnlaceClienteEnviarCorreoOut,
  EnlaceClienteOut,
  MapaCalorOut,
  MapaCalorResumenOut,
  PlanoOut,
  ProyectoListOut,
  ProyectoAdminCreate,
  ProyectoAdminUpdate,
  ProyectoReasignarIn,
  ProyectosFilter,
  ProyectosPageOut,
  RestriccionesIAIn,
} from "../types";

export async function listarProyectosOrg(
  page = 1,
  pageSize = 20,
  filtros?: ProyectosFilter,
): Promise<ProyectosPageOut> {
  const { data } = await apiClient.get<ProyectosPageOut>("/admin/proyectos", {
    params: {
      page,
      page_size: pageSize,
      ...filtros,
    },
  });
  return data;
}

export async function obtenerProyectoAdmin(
  id: number,
): Promise<ProyectoListOut> {
  const { data } = await apiClient.get<ProyectoListOut>(
    `/admin/proyectos/${id}`,
  );
  return data;
}

export async function crearProyectoAdmin(
  body: ProyectoAdminCreate,
): Promise<ProyectoListOut> {
  const { data } = await apiClient.post<ProyectoListOut>(
    "/admin/proyectos",
    body,
  );
  return data;
}

export async function actualizarProyectoAdmin(
  id: number,
  body: ProyectoAdminUpdate,
): Promise<ProyectoListOut> {
  const { data } = await apiClient.put<ProyectoListOut>(
    `/admin/proyectos/${id}`,
    body,
  );
  return data;
}

export async function eliminarProyectoAdmin(id: number): Promise<void> {
  await apiClient.delete(`/admin/proyectos/${id}`);
}

export async function archivarProyectoAdmin(
  id: number,
): Promise<ProyectoListOut> {
  const { data } = await apiClient.patch<ProyectoListOut>(
    `/admin/proyectos/${id}/archivar`,
  );
  return data;
}

export async function reasignarTecnico(
  id: number,
  body: ProyectoReasignarIn,
): Promise<ProyectoListOut> {
  const { data } = await apiClient.patch<ProyectoListOut>(
    `/admin/proyectos/${id}/reasignar`,
    body,
  );
  return data;
}

export async function listarPlanosProyecto(
  proyectoId: number,
): Promise<PlanoOut[]> {
  const { data } = await apiClient.get<PlanoOut[]>(
    `/proyectos/${proyectoId}/planos`,
  );
  return data;
}

export async function listarAPsPlano(
  planoId: number,
): Promise<APDisponibleOut[]> {
  const { data } = await apiClient.get<APDisponibleOut[]>(
    `/planos/${planoId}/aps`,
  );
  return data;
}

export async function listarConjuntosPlano(
  planoId: number,
): Promise<ConjuntoAPOut[]> {
  const { data } = await apiClient.get<ConjuntoAPOut[]>(
    `/planos/${planoId}/conjuntos-ap`,
  );
  return data;
}

export async function listarMapasPlano(planoId: number): Promise<MapaCalorOut[]> {
  const { data } = await apiClient.get<MapaCalorOut[]>(`/planos/${planoId}/mapas`);
  return data;
}

export async function crearConjuntoAP(
  planoId: number,
  body: {
    nombre: string;
    proposito: string;
    descripcion?: string | null;
    es_principal?: boolean;
    banda_objetivo: "2.4" | "5";
    bssids: string[];
  },
): Promise<ConjuntoAPOut> {
  const { data } = await apiClient.post<ConjuntoAPOut>(
    `/planos/${planoId}/conjuntos-ap`,
    body,
  );
  return data;
}

export async function actualizarConjuntoAP(
  conjuntoId: number,
  body: Partial<{
    nombre: string;
    proposito: string;
    descripcion: string | null;
    es_principal: boolean;
    banda_objetivo: "2.4" | "5";
    bssids: string[];
  }>,
): Promise<ConjuntoAPOut> {
  const { data } = await apiClient.patch<ConjuntoAPOut>(
    `/conjuntos-ap/${conjuntoId}`,
    body,
  );
  return data;
}

export async function eliminarConjuntoAP(conjuntoId: number): Promise<void> {
  await apiClient.delete(`/conjuntos-ap/${conjuntoId}`);
}

export async function eliminarMapaCalor(mapaId: number): Promise<void> {
  await apiClient.delete(`/mapas/${mapaId}`);
}

export async function generarHeatmapConjunto(
  conjuntoId: number,
  body: {
    modo: "INDIVIDUAL" | "SUBCONJUNTO" | "CONJUNTO_COMPLETO";
    bssids?: string[];
    algoritmo: "IDW";
    resolucion: 64 | 128 | 256;
  },
): Promise<MapaCalorOut> {
  const { data } = await apiClient.post<MapaCalorOut>(
    `/conjuntos-ap/${conjuntoId}/heatmaps`,
    body,
  );
  return data;
}

export async function generarHeatmapsFaltantesConjunto(
  conjuntoId: number,
  body: {
    algoritmo?: "IDW";
    algoritmos?: Array<"IDW">;
    resolucion: 64 | 128 | 256;
    actualizar_existentes?: boolean;
    reemplazar_existentes?: boolean;
  },
): Promise<MapaCalorResumenOut[]> {
  const { data } = await apiClient.post<MapaCalorResumenOut[]>(
    `/conjuntos-ap/${conjuntoId}/heatmaps/combinaciones-faltantes`,
    body,
  );
  return data;
}

export async function generarConjuntosIAProyecto(
  proyectoId: number,
  body: RestriccionesIAIn,
): Promise<ConjuntosIAGeneradosOut> {
  const { data } = await apiClient.post<ConjuntosIAGeneradosOut>(
    `/proyectos/${proyectoId}/conjuntos-ap/recomendaciones-ia`,
    body,
  );
  return data;
}

export async function listarEnlacesCliente(
  proyectoId: number,
): Promise<EnlaceClienteOut[]> {
  const { data } = await apiClient.get<EnlaceClienteOut[]>(
    `/share/proyectos/${proyectoId}/enlaces`,
  );
  return data;
}

export async function crearEnlaceCliente(
  proyectoId: number,
  body: EnlaceClienteCrearIn,
): Promise<EnlaceClienteOut> {
  const { data } = await apiClient.post<EnlaceClienteOut>(
    `/share/proyectos/${proyectoId}/enlaces`,
    body,
  );
  return data;
}

export async function actualizarEnlaceCliente(
  enlaceId: number,
  revocado: boolean,
): Promise<EnlaceClienteOut> {
  const { data } = await apiClient.patch<EnlaceClienteOut>(
    `/share/enlaces/${enlaceId}`,
    { revocado },
  );
  return data;
}

export async function eliminarEnlaceCliente(enlaceId: number): Promise<void> {
  await apiClient.delete(`/share/enlaces/${enlaceId}`);
}

export async function eliminarEnlacesClienteProyecto(
  proyectoId: number,
): Promise<void> {
  await apiClient.delete(`/share/proyectos/${proyectoId}/enlaces`);
}

export async function enviarCorreoEnlaceCliente(
  enlaceId: number,
  body: EnlaceClienteEnviarCorreoIn,
): Promise<EnlaceClienteEnviarCorreoOut> {
  const { data } = await apiClient.post<EnlaceClienteEnviarCorreoOut>(
    `/share/enlaces/${enlaceId}/correo`,
    body,
  );
  return data;
}
