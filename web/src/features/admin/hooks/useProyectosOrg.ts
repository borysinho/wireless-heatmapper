/**
 * Hooks TanStack Query para proyectos de la organización (admin).
 * Sp1-26, Sp1-51, Sp1-52 — PB-18.
 */

import {
  useMutation,
  useQueries,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import {
  archivarProyectoAdmin,
  actualizarProyectoAdmin,
  actualizarEnlaceCliente,
  actualizarConjuntoAP,
  crearEnlaceCliente,
  crearProyectoAdmin,
  crearConjuntoAP,
  eliminarProyectoAdmin,
  enviarCorreoEnlaceCliente,
  eliminarConjuntoAP,
  eliminarEnlaceCliente,
  eliminarEnlacesClienteProyecto,
  eliminarMapaCalor,
  generarConjuntosIAProyecto,
  generarHeatmapConjunto,
  generarHeatmapsFaltantesConjunto,
  listarConjuntosPlano,
  listarEnlacesCliente,
  listarMapasPlano,
  obtenerProyectoAdmin,
  prepararConjuntoIAProyecto,
  listarAPsPlano,
  listarPlanosProyecto,
  listarProyectosOrg,
  reasignarTecnico,
} from "../api/proyectosApi";
import type {
  EnlaceClienteCrearIn,
  ProyectoReasignarIn,
  ProyectoAdminCreate,
  ProyectoAdminUpdate,
  ProyectosFilter,
  RestriccionesIAIn,
} from "../types";

export function useProyectosOrg(
  page = 1,
  pageSize = 20,
  filtros?: ProyectosFilter,
) {
  return useQuery({
    queryKey: ["admin", "proyectos", { page, pageSize, ...filtros }],
    queryFn: () => listarProyectosOrg(page, pageSize, filtros),
    placeholderData: (prev) => prev,
  });
}

export function useProyectoAdmin(proyectoId: number) {
  return useQuery({
    queryKey: ["admin", "proyectos", proyectoId],
    queryFn: () => obtenerProyectoAdmin(proyectoId),
    enabled: proyectoId > 0,
  });
}

export function useArchivarProyectoAdmin() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => archivarProyectoAdmin(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "proyectos"] }),
  });
}

export function useCrearProyectoAdmin() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ProyectoAdminCreate) => crearProyectoAdmin(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "proyectos"] }),
  });
}

export function useActualizarProyectoAdmin() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: number; body: ProyectoAdminUpdate }) =>
      actualizarProyectoAdmin(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "proyectos"] }),
  });
}

export function useEliminarProyectoAdmin() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => eliminarProyectoAdmin(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "proyectos"] }),
  });
}

export function useReasignarTecnico() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: number; body: ProyectoReasignarIn }) =>
      reasignarTecnico(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "proyectos"] }),
  });
}

export function usePlanosProyecto(proyectoId: number) {
  return useQuery({
    queryKey: ["admin", "proyectos", proyectoId, "planos"],
    queryFn: () => listarPlanosProyecto(proyectoId),
    enabled: proyectoId > 0,
  });
}

export function useAPsPlano(planoId: number | null) {
  return useQuery({
    queryKey: ["admin", "planos", planoId, "aps"],
    queryFn: () => listarAPsPlano(planoId ?? 0),
    enabled: typeof planoId === "number" && planoId > 0,
  });
}

export function useConjuntosPorPlanos(planoIds: number[]) {
  return useQueries({
    queries: planoIds.map((planoId) => ({
      queryKey: ["admin", "planos", planoId, "conjuntos-ap"],
      queryFn: () => listarConjuntosPlano(planoId),
      enabled: planoId > 0,
    })),
  });
}

export function useMapasPorPlanos(planoIds: number[]) {
  return useQueries({
    queries: planoIds.map((planoId) => ({
      queryKey: ["admin", "planos", planoId, "mapas"],
      queryFn: () => listarMapasPlano(planoId),
      enabled: planoId > 0,
    })),
  });
}

export function useCrearConjuntoAP() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ planoId, body }: { planoId: number; body: Parameters<typeof crearConjuntoAP>[1] }) =>
      crearConjuntoAP(planoId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "planos"] }),
  });
}

export function useActualizarConjuntoAP() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ conjuntoId, body }: { conjuntoId: number; body: Parameters<typeof actualizarConjuntoAP>[1] }) =>
      actualizarConjuntoAP(conjuntoId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "planos"] }),
  });
}

export function useEliminarConjuntoAP() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (conjuntoId: number) => eliminarConjuntoAP(conjuntoId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "planos"] }),
  });
}

export function useEliminarMapaCalor() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (mapaId: number) => eliminarMapaCalor(mapaId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "planos"] }),
  });
}

export function useGenerarHeatmapConjunto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ conjuntoId, body }: { conjuntoId: number; body: Parameters<typeof generarHeatmapConjunto>[1] }) =>
      generarHeatmapConjunto(conjuntoId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "planos"] }),
  });
}

export function useGenerarHeatmapsFaltantesConjunto() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      conjuntoId,
      body,
    }: {
      conjuntoId: number;
      body: Parameters<typeof generarHeatmapsFaltantesConjunto>[1];
    }) => generarHeatmapsFaltantesConjunto(conjuntoId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin", "planos"] }),
  });
}

export function useGenerarConjuntosIAProyecto(proyectoId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: RestriccionesIAIn) =>
      generarConjuntosIAProyecto(proyectoId, body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin", "planos"] });
      qc.invalidateQueries({
        queryKey: ["admin", "proyectos", proyectoId, "enlaces-cliente"],
      });
    },
  });
}

export function usePrepararConjuntoIAProyecto(proyectoId: number) {
  return useMutation({
    mutationFn: (conjuntoId: number) =>
      prepararConjuntoIAProyecto(proyectoId, conjuntoId),
  });
}

export function useEnlacesCliente(proyectoId: number) {
  return useQuery({
    queryKey: ["admin", "proyectos", proyectoId, "enlaces-cliente"],
    queryFn: () => listarEnlacesCliente(proyectoId),
    enabled: proyectoId > 0,
  });
}

export function useCrearEnlaceCliente(proyectoId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: EnlaceClienteCrearIn) =>
      crearEnlaceCliente(proyectoId, body),
    onSuccess: () =>
      qc.invalidateQueries({
        queryKey: ["admin", "proyectos", proyectoId, "enlaces-cliente"],
      }),
  });
}

export function useActualizarEnlaceCliente(proyectoId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      enlaceId,
      revocado,
    }: {
      enlaceId: number;
      revocado: boolean;
    }) => actualizarEnlaceCliente(enlaceId, revocado),
    onSuccess: () =>
      qc.invalidateQueries({
        queryKey: ["admin", "proyectos", proyectoId, "enlaces-cliente"],
      }),
  });
}

export function useEliminarEnlaceCliente(proyectoId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (enlaceId: number) => eliminarEnlaceCliente(enlaceId),
    onSuccess: () =>
      qc.invalidateQueries({
        queryKey: ["admin", "proyectos", proyectoId, "enlaces-cliente"],
      }),
  });
}

export function useEliminarEnlacesClienteProyecto(proyectoId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => eliminarEnlacesClienteProyecto(proyectoId),
    onSuccess: () =>
      qc.invalidateQueries({
        queryKey: ["admin", "proyectos", proyectoId, "enlaces-cliente"],
      }),
  });
}

export function useEnviarCorreoEnlaceCliente(proyectoId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      enlaceId,
      clienteId,
    }: {
      enlaceId: number;
      clienteId: number;
    }) => enviarCorreoEnlaceCliente(enlaceId, { cliente_id: clienteId }),
    onSuccess: () =>
      qc.invalidateQueries({
        queryKey: ["admin", "proyectos", proyectoId, "enlaces-cliente"],
      }),
  });
}
