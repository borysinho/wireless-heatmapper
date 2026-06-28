import { useMemo, useState } from "react";
import { Eye, X } from "lucide-react";
import { useOutletContext } from "react-router-dom";
import { resolverUrlApi } from "@/shared/api/urlApi";
import { Button, EmptyState } from "@/shared/components";
import {
  useConjuntosPorPlanos,
  usePlanosProyecto,
} from "../hooks/useProyectosOrg";
import type { ConjuntoAPOut, PlanoOut } from "../types";
import styles from "./ConjuntosAPProyecto.module.css";

type FiltroOrigen = "todos" | "manual_movil" | "ia";
type VistaPreviaConjunto = {
  conjunto: ConjuntoAPOut;
  plano: PlanoOut;
};

export default function ConjuntosAPProyecto() {
  const { proyectoId } = useOutletContext<{
    proyectoId: number;
    proyectoNombre: string;
  }>();
  const [filtroOrigen, setFiltroOrigen] = useState<FiltroOrigen>("todos");
  const [vistaPrevia, setVistaPrevia] = useState<VistaPreviaConjunto | null>(null);

  const {
    data: planos,
    isLoading: cargandoPlanos,
    isError: errorPlanos,
  } = usePlanosProyecto(proyectoId);
  const planoIds = useMemo(() => (planos ?? []).map((plano) => plano.id), [planos]);
  const consultasConjuntos = useConjuntosPorPlanos(planoIds);

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
            Revise los conjuntos creados por el equipo técnico y las propuestas IA
            derivadas desde un conjunto de campo.
          </p>
        </div>
      </div>

      <div className={styles.resumen}>
        <ResumenItem etiqueta="Móvil" valor={resumen.manual_movil} />
        <ResumenItem etiqueta="IA" valor={resumen.ia} />
        <ResumenItem etiqueta="Total" valor={conjuntos.length} />
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
                <th>Vista</th>
                <th>Origen</th>
                <th>APs</th>
              </tr>
            </thead>
            <tbody>
              {conjuntosFiltrados.map((conjunto) => {
                const plano = planosPorId.get(conjunto.plano_id);
                return (
                  <tr key={conjunto.id}>
                    <td className={styles.nombre}>
                      <strong>{conjunto.nombre}</strong>
                      <small>{conjunto.proposito}</small>
                    </td>
                    <td>
                      {plano?.nombre ?? `Plano #${conjunto.plano_id}`}
                    </td>
                    <td>
                      <Button
                        variante="secondary"
                        tamano="sm"
                        disabled={!plano || conjunto.items.length === 0}
                        onClick={() => {
                          if (plano) setVistaPrevia({ conjunto, plano });
                        }}
                      >
                        <Eye size={14} aria-hidden="true" />
                        Previsualizar
                      </Button>
                    </td>
                    <td>{_labelOrigen(conjunto.origen)}</td>
                    <td>{conjunto.cantidad_aps}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {vistaPrevia && (
        <VistaPreviaMapa
          conjunto={vistaPrevia.conjunto}
          plano={vistaPrevia.plano}
          onCerrar={() => setVistaPrevia(null)}
        />
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
      return acc;
    },
    { manual_movil: 0, ia: 0 },
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

function VistaPreviaMapa({
  conjunto,
  plano,
  onCerrar,
}: {
  conjunto: ConjuntoAPOut;
  plano: PlanoOut;
  onCerrar: () => void;
}) {
  const apsConUbicacion = conjunto.items.filter(
    (ap) => typeof ap.pos_x === "number" && typeof ap.pos_y === "number",
  );

  return (
    <div className={styles.overlay} role="dialog" aria-modal="true" aria-labelledby="vista-conjunto-titulo">
      <div className={styles.modalVista}>
        <header className={styles.modalHeader}>
          <div>
            <p>{plano.nombre}</p>
            <h2 id="vista-conjunto-titulo">{conjunto.nombre}</h2>
            <span>
              {_labelOrigen(conjunto.origen)} · {conjunto.cantidad_aps} AP(s)
            </span>
          </div>
          <button type="button" className={styles.cerrarVista} onClick={onCerrar} aria-label="Cerrar vista previa">
            <X size={18} aria-hidden="true" />
          </button>
        </header>

        <div className={styles.mapaPreview}>
          <div
            className={styles.planoPreview}
            style={{
              aspectRatio: `${plano.ancho_px} / ${plano.alto_px}`,
              width: `min(100%, calc(62vh * ${plano.ancho_px / plano.alto_px}))`,
            }}
          >
            <img src={resolverUrlApi(plano.url_firmada)} alt={`Plano ${plano.nombre}`} />
            <div className={styles.capaMarcadores} aria-label="Ubicación de APs del conjunto">
              {apsConUbicacion.map((ap, indice) => (
                <span
                  key={`${ap.bssid}-${indice}`}
                  className={styles.marcadorAp}
                  style={{
                    left: `${((ap.pos_x ?? 0) / plano.ancho_px) * 100}%`,
                    top: `${((ap.pos_y ?? 0) / plano.alto_px) * 100}%`,
                  }}
                  title={`${indice + 1}. ${ap.ssid || "SSID oculto"} · ${ap.bssid}`}
                >
                  {indice + 1}
                </span>
              ))}
            </div>
          </div>
        </div>

        {apsConUbicacion.length === 0 ? (
          <p className={styles.sinUbicaciones}>Este conjunto no tiene coordenadas de AP registradas para el plano.</p>
        ) : (
          <div className={styles.listaApsPreview}>
            {apsConUbicacion.map((ap, indice) => (
              <article key={`${ap.bssid}-detalle-${indice}`}>
                <strong>{indice + 1}. {ap.ssid || "SSID oculto"}</strong>
                <span>{ap.bssid}</span>
                <small>
                  {typeof ap.rssi_promedio === "number" ? `${ap.rssi_promedio.toFixed(1)} dBm` : "RSSI s/d"}
                  {" · "}
                  {ap.canal ? `canal ${ap.canal}` : "canal s/d"}
                  {" · "}
                  {ap.cantidad_puntos ?? 0} punto(s)
                </small>
              </article>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
