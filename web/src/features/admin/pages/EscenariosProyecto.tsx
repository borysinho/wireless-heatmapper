/**
 * Generación de conjuntos AP propuestos por IA.
 * Una propuesta IA nace siempre desde un único conjunto AP relevado en campo.
 */

import { useMemo, useState } from "react";
import { BrainCircuit, Layers3, RadioTower, Sparkles } from "lucide-react";
import { useParams } from "react-router-dom";
import { Badge, Button, EmptyState, useToast } from "@/shared/components";
import {
  useConjuntosPorPlanos,
  useGenerarConjuntosIAProyecto,
  usePlanosProyecto,
} from "../hooks/useProyectosOrg";
import type { ConjuntoAPOut, RestriccionesIAIn } from "../types";
import styles from "./EscenariosProyecto.module.css";

const DEFAULT_FORM: Omit<RestriccionesIAIn, "fuente_entrada"> = {
  bandas: ["2.4", "5"],
  umbral_objetivo_dbm: -70,
  resolucion: 64,
  cantidad_recomendaciones: 3,
};

export default function EscenariosProyecto() {
  const params = useParams();
  const toast = useToast();
  const proyectoId = Number(params.id ?? 0);

  const [form, setForm] = useState(DEFAULT_FORM);
  const [planoId, setPlanoId] = useState<number | null>(null);
  const [conjuntoFuenteId, setConjuntoFuenteId] = useState<number | null>(null);

  const {
    data: planos,
    isLoading: cargandoPlanos,
    isError: errorPlanos,
  } = usePlanosProyecto(proyectoId);
  const planosOrdenados = useMemo(
    () =>
      [...(planos ?? [])].sort(
        (a, b) => Number(b.calibrado) - Number(a.calibrado),
      ),
    [planos],
  );
  const planoInicial =
    planosOrdenados.find((plano) => plano.calibrado) ?? planosOrdenados[0];
  const planoSeleccionadoId = planoId ?? planoInicial?.id ?? null;
  const planoSeleccionado = planosOrdenados.find(
    (plano) => plano.id === planoSeleccionadoId,
  );
  const planoIds = useMemo(
    () => planosOrdenados.map((plano) => plano.id),
    [planosOrdenados],
  );
  const consultasConjuntos = useConjuntosPorPlanos(planoIds);
  const conjuntos = useMemo(
    () => consultasConjuntos.flatMap((consulta) => consulta.data ?? []),
    [consultasConjuntos],
  );
  const conjuntosPlano = useMemo(
    () =>
      conjuntos
        .filter((conjunto) => conjunto.plano_id === planoSeleccionadoId)
        .sort((a, b) => (a.updated_at < b.updated_at ? 1 : -1)),
    [conjuntos, planoSeleccionadoId],
  );
  const conjuntosFuente = conjuntosPlano.filter((conjunto) => conjunto.origen !== "ia");
  const conjuntosIA = conjuntosPlano.filter((conjunto) => conjunto.origen === "ia");
  const conjuntoFuente =
    conjuntosFuente.find((conjunto) => conjunto.id === conjuntoFuenteId) ??
    conjuntosFuente[0] ??
    null;
  const cargandoConjuntos = consultasConjuntos.some((consulta) => consulta.isLoading);
  const errorConjuntos = consultasConjuntos.some((consulta) => consulta.isError);

  const { mutateAsync: generar, isPending: generando } =
    useGenerarConjuntosIAProyecto(proyectoId);
  const puedeGenerar =
    Boolean(planoSeleccionado?.calibrado) && conjuntoFuente !== null && !generando;

  const handleToggleBanda = (banda: "2.4" | "5") => {
    setForm((prev) => {
      const bandas = prev.bandas.includes(banda)
        ? prev.bandas.filter((item) => item !== banda)
        : [...prev.bandas, banda];
      return { ...prev, bandas: bandas.length > 0 ? bandas : [banda] };
    });
  };

  const handleGenerar = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!planoSeleccionado?.calibrado) {
      toast.error("Seleccione un plano calibrado antes de generar propuestas IA.");
      return;
    }
    if (!conjuntoFuente) {
      toast.error("Seleccione un conjunto AP relevado por el técnico.");
      return;
    }
    try {
      const respuesta = await generar({
        ...form,
        plano_id: planoSeleccionado.id,
        fuente_entrada: {
          tipo: "CONJUNTO_EXISTENTE",
          conjunto_id: conjuntoFuente.id,
        },
      });
      toast.exito(`${respuesta.conjuntos.length} conjunto(s) IA generado(s).`);
    } catch {
      toast.error("No se pudieron generar las propuestas IA.");
    }
  };

  if (cargandoPlanos || cargandoConjuntos) return <div className={styles.skeleton} />;
  if (errorPlanos || errorConjuntos) {
    return <EmptyState mensaje="No se pudo cargar la información RF del proyecto." />;
  }
  if (!planosOrdenados.length) {
    return <EmptyState mensaje="El proyecto todavía no tiene planos." />;
  }

  return (
    <section>
      <header className={styles.encabezado}>
        <h1 className={styles.titulo}>Conjuntos AP propuestos por IA</h1>
        <p className={styles.subtitulo}>
          Genere alternativas IA derivadas desde un único conjunto AP relevado por
          el técnico de campo.
        </p>
      </header>

      <form className={styles.panelGeneracion} onSubmit={handleGenerar}>
        <div className={styles.panelHeader}>
          <div>
            <h3>Fuente de generación</h3>
            <p>La IA reutiliza conjuntos AP existentes y crea nuevos conjuntos derivados.</p>
          </div>
          <Button type="submit" disabled={!puedeGenerar} isLoading={generando}>
            <Sparkles size={16} aria-hidden="true" />
            Generar propuestas
          </Button>
        </div>

        <div className={styles.generacionGrid}>
          <div className={styles.columnaFuente}>
            <section className={styles.banda}>
              <div className={styles.seccionHeader}>
                <Layers3 size={16} aria-hidden="true" />
                <h2>Plano</h2>
              </div>
              <div className={styles.planosGrid}>
                {planosOrdenados.map((plano) => (
                  <button
                    key={plano.id}
                    type="button"
                    className={`${styles.planoCard} ${
                      plano.id === planoSeleccionadoId ? styles.planoActivo : ""
                    }`}
                    onClick={() => {
                      setPlanoId(plano.id);
                      setConjuntoFuenteId(null);
                    }}
                  >
                    <span>{plano.nombre}</span>
                    <small>
                      {plano.calibrado ? "Calibrado" : "Sin calibración"} ·{" "}
                      {plano.cantidad_puntos} punto(s)
                    </small>
                  </button>
                ))}
              </div>
            </section>

            <section className={styles.banda}>
              <div className={styles.seccionHeader}>
                <RadioTower size={16} aria-hidden="true" />
                <h2>Conjunto técnico fuente</h2>
              </div>
              {conjuntosFuente.length === 0 ? (
                <p className={styles.subtitulo}>
                  No hay conjuntos relevados por el técnico en este plano.
                </p>
              ) : (
                <div className={styles.conjuntosGrid}>
                  {conjuntosFuente.map((conjunto) => (
                    <button
                      key={conjunto.id}
                      type="button"
                      className={`${styles.conjuntoCard} ${
                        conjunto.id === conjuntoFuente?.id
                          ? styles.conjuntoActivo
                          : ""
                      }`}
                      onClick={() => setConjuntoFuenteId(conjunto.id)}
                    >
                      <span>{conjunto.nombre}</span>
                      <small>
                        {_labelOrigen(conjunto.origen)} · {conjunto.cantidad_aps} AP(s)
                      </small>
                    </button>
                  ))}
                </div>
              )}
            </section>
          </div>

          <aside className={`${styles.banda} ${styles.panelParametros}`}>
            <div className={styles.seccionHeader}>
              <BrainCircuit size={16} aria-hidden="true" />
              <h2>Parámetros IA</h2>
            </div>
            <div className={styles.formularioConjunto}>
              <label>
                Bandas
                <div className={styles.selectorBandas}>
                  {(["2.4", "5"] as const).map((banda) => (
                    <button
                      key={banda}
                      type="button"
                      className={
                        form.bandas.includes(banda) ? styles.bandaActiva : ""
                      }
                      onClick={() => handleToggleBanda(banda)}
                    >
                      {banda} GHz
                    </button>
                  ))}
                </div>
              </label>
              <label>
                Umbral objetivo
                <input
                  type="number"
                  min={-90}
                  max={-50}
                  value={form.umbral_objetivo_dbm}
                  onChange={(event) =>
                    setForm((prev) => ({
                      ...prev,
                      umbral_objetivo_dbm: Number(event.target.value),
                    }))
                  }
                />
              </label>
              <label>
                Resolución
                <input
                  type="number"
                  min={32}
                  max={128}
                  value={form.resolucion}
                  onChange={(event) =>
                    setForm((prev) => ({
                      ...prev,
                      resolucion: Number(event.target.value),
                    }))
                  }
                />
              </label>
              <label>
                Cantidad de propuestas
                <input
                  type="number"
                  min={1}
                  max={5}
                  value={form.cantidad_recomendaciones}
                  onChange={(event) =>
                    setForm((prev) => ({
                      ...prev,
                      cantidad_recomendaciones: Number(event.target.value),
                    }))
                  }
                />
              </label>
            </div>
          </aside>
        </div>
      </form>

      <section className={styles.banda}>
        <div className={styles.resultadosHeader}>
          <div>
            <h2>Propuestas IA del plano</h2>
            <p>
              {conjuntosIA.length} conjunto(s) IA asociado(s) al plano seleccionado.
            </p>
          </div>
        </div>
        {conjuntosIA.length === 0 ? (
          <EmptyState mensaje="Todavía no hay conjuntos IA generados para este plano." />
        ) : (
          <div className={styles.resultadosLista}>
            {conjuntosIA.map((conjunto) => (
              <ConjuntoIACard key={conjunto.id} conjunto={conjunto} />
            ))}
          </div>
        )}
      </section>
    </section>
  );
}

function ConjuntoIACard({ conjunto }: { conjunto: ConjuntoAPOut }) {
  const cobertura =
    typeof conjunto.metricas_ia?.pct_cobertura === "number"
      ? `${conjunto.metricas_ia.pct_cobertura.toFixed(1)}% cobertura`
      : null;
  const confianza =
    typeof conjunto.metricas_ia?.confianza === "string"
      ? conjunto.metricas_ia.confianza
      : null;

  return (
    <article className={styles.escenario}>
      <div className={styles.escenarioHeader}>
        <div>
          <h2>{conjunto.nombre}</h2>
          <p>{conjunto.resumen_ia ?? conjunto.descripcion ?? conjunto.proposito}</p>
        </div>
        <Badge variante="activo" etiqueta="Conjunto IA" />
      </div>
      <div className={styles.metricas}>
        <span>{conjunto.cantidad_aps} AP(s)</span>
        {cobertura && <span>{cobertura}</span>}
        {confianza && <span>Confianza {confianza}</span>}
        {conjunto.conjunto_origen_id && (
          <span>Fuente #{conjunto.conjunto_origen_id}</span>
        )}
      </div>
      <div className={styles.recomendaciones}>
        {conjunto.items.map((item, index) => (
          <article key={`${conjunto.id}-${item.bssid}-${index}`}>
            <strong>
              {index + 1}. {item.ssid || "SSID oculto"}
            </strong>
            <span>{item.accion_recomendada ?? "Mantener AP en propuesta"}</span>
            <small>
              {item.bssid} · {item.banda ?? "banda s/d"} ·{" "}
              {typeof item.rssi_promedio === "number"
                ? `${item.rssi_promedio.toFixed(1)} dBm`
                : "RSSI s/d"}
            </small>
            {item.justificacion && <p>{item.justificacion}</p>}
          </article>
        ))}
      </div>
    </article>
  );
}

function _labelOrigen(origen: string): string {
  const labels: Record<string, string> = {
    manual_movil: "Móvil",
    manual_web: "Web",
    ia: "IA",
  };
  return labels[origen] ?? origen;
}
