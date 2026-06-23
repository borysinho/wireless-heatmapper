import { useMemo, useState } from "react";
import { Send, XCircle } from "lucide-react";
import { useOutletContext } from "react-router-dom";
import { Badge, Button, EmptyState, useToast } from "@/shared/components";
import {
  useCambiarEstadoConjuntoAP,
  useConjuntosPorPlanos,
  usePlanosProyecto,
} from "../hooks/useProyectosOrg";
import type { ConjuntoAPOut, EstadoGobernanzaConjunto } from "../types";
import styles from "./ConjuntosAPProyecto.module.css";

type FiltroOrigen = "todos" | "manual_movil" | "ia";

export default function ConjuntosAPProyecto() {
  const { proyectoId } = useOutletContext<{
    proyectoId: number;
    proyectoNombre: string;
  }>();
  const toast = useToast();
  const [filtroOrigen, setFiltroOrigen] = useState<FiltroOrigen>("todos");

  const {
    data: planos,
    isLoading: cargandoPlanos,
    isError: errorPlanos,
  } = usePlanosProyecto(proyectoId);
  const planoIds = useMemo(() => (planos ?? []).map((plano) => plano.id), [planos]);
  const consultasConjuntos = useConjuntosPorPlanos(planoIds);
  const { mutateAsync: cambiarEstado, isPending: cambiando } =
    useCambiarEstadoConjuntoAP(proyectoId);

  const conjuntos = useMemo(
    () =>
      consultasConjuntos
        .flatMap((consulta) => consulta.data ?? [])
        .sort((a, b) => (a.updated_at < b.updated_at ? 1 : -1)),
    [consultasConjuntos],
  );
  const planosPorId = useMemo(
    () => new Map((planos ?? []).map((plano) => [plano.id, plano])),
    [planos],
  );
  const cargandoConjuntos = consultasConjuntos.some((consulta) => consulta.isLoading);
  const errorConjuntos = consultasConjuntos.some((consulta) => consulta.isError);
  const conjuntosFiltrados =
    filtroOrigen === "todos"
      ? conjuntos
      : conjuntos.filter((conjunto) => conjunto.origen === filtroOrigen);
  const resumen = _resumenConjuntos(conjuntos);

  const handleEstadoCliente = async (
    conjunto: ConjuntoAPOut,
    estado: EstadoGobernanzaConjunto,
  ) => {
    try {
      await cambiarEstado({ conjuntoId: conjunto.id, estadoGobernanza: estado });
      toast.exito(
        estado === "publicado_cliente"
          ? `Conjunto "${conjunto.nombre}" compartido con el cliente.`
          : `Conjunto "${conjunto.nombre}" quitado del portal cliente.`,
      );
    } catch {
      toast.error("No se pudo actualizar la selección para cliente.");
    }
  };

  if (cargandoPlanos || cargandoConjuntos) return <div className={styles.skeleton} />;
  if (errorPlanos || errorConjuntos) {
    return <EmptyState mensaje="No se pudieron cargar los conjuntos de APs." />;
  }
  if (!planos || planos.length === 0) {
    return <EmptyState mensaje="El proyecto todavía no tiene planos." />;
  }

  return (
    <section className={styles.contenedor}>
      <div className={styles.encabezadoSeccion}>
        <div>
          <h2>Conjuntos de APs para cliente</h2>
          <p>
            Seleccione qué conjunto podrá consultar el cliente para generar heatmaps
            por AP individual, subconjunto o conjunto completo.
          </p>
        </div>
      </div>

      <div className={styles.resumen}>
        <ResumenItem etiqueta="Móvil" valor={resumen.manual_movil} />
        <ResumenItem etiqueta="IA" valor={resumen.ia} />
        <ResumenItem etiqueta="Compartidos" valor={resumen.publicado_cliente} />
      </div>

      <div className={styles.filtros}>
        {(["todos", "manual_movil", "ia"] as FiltroOrigen[]).map(
          (origen) => (
            <button
              key={origen}
              type="button"
              className={filtroOrigen === origen ? styles.filtroActivo : ""}
              onClick={() => setFiltroOrigen(origen)}
            >
              {_labelOrigen(origen)}
            </button>
          ),
        )}
      </div>

      {conjuntosFiltrados.length === 0 ? (
        <EmptyState mensaje="No hay conjuntos de APs para el filtro seleccionado." />
      ) : (
        <div className={styles.tablaWrapper}>
          <table className={styles.tabla}>
            <thead>
              <tr>
                <th>Conjunto</th>
                <th>Plano</th>
                <th>Origen</th>
                <th>Estado</th>
                <th>APs</th>
                <th>Cliente</th>
              </tr>
            </thead>
            <tbody>
              {conjuntosFiltrados.map((conjunto) => {
                const publicado = conjunto.estado_gobernanza === "publicado_cliente";
                return (
                  <tr key={conjunto.id}>
                    <td className={styles.nombre}>
                      <strong>{conjunto.nombre}</strong>
                      <small>{conjunto.proposito}</small>
                    </td>
                    <td>
                      {planosPorId.get(conjunto.plano_id)?.nombre ??
                        `Plano #${conjunto.plano_id}`}
                    </td>
                    <td>{_labelOrigen(conjunto.origen)}</td>
                    <td>
                      <Badge
                        variante="en_progreso"
                        etiqueta={_labelEstado(conjunto.estado_gobernanza)}
                      />
                    </td>
                    <td>{conjunto.cantidad_aps}</td>
                    <td>
                      <div className={styles.acciones}>
                        {publicado ? (
                          <Button
                            variante="ghost"
                            tamano="sm"
                            disabled={cambiando}
                            onClick={() =>
                              handleEstadoCliente(conjunto, "aprobado_interno")
                            }
                          >
                            <XCircle size={14} aria-hidden="true" />
                            Quitar del cliente
                          </Button>
                        ) : (
                          <Button
                            variante="secondary"
                            tamano="sm"
                            disabled={
                              cambiando || conjunto.estado_gobernanza === "descartado"
                            }
                            onClick={() =>
                              handleEstadoCliente(conjunto, "publicado_cliente")
                            }
                          >
                            <Send size={14} aria-hidden="true" />
                            Compartir con cliente
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function ResumenItem({ etiqueta, valor }: { etiqueta: string; valor: number }) {
  return (
    <div className={styles.resumenItem}>
      <span>{etiqueta}</span>
      <strong>{valor}</strong>
    </div>
  );
}

function _resumenConjuntos(conjuntos: ConjuntoAPOut[]) {
  return conjuntos.reduce(
    (acc, conjunto) => {
      if (conjunto.origen in acc) {
        acc[conjunto.origen as "manual_movil" | "ia"] += 1;
      }
      if (conjunto.estado_gobernanza === "publicado_cliente") {
        acc.publicado_cliente += 1;
      }
      return acc;
    },
    { manual_movil: 0, ia: 0, publicado_cliente: 0 },
  );
}

function _labelOrigen(origen: string): string {
  return (
    ({ todos: "Todos", manual_movil: "Móvil", manual_web: "Web", ia: "IA" } as Record<
      string,
      string
    >)[origen] ?? origen
  );
}

function _labelEstado(estado: string): string {
  return (
    ({
      borrador_tecnico: "Borrador técnico",
      preliminar: "Preliminar",
      pendiente_revision: "Pendiente revisión",
      aprobado_interno: "Aprobado interno",
      publicado_cliente: "Compartido con cliente",
      descartado: "Descartado",
    } as Record<string, string>)[estado] ?? estado
  );
}
