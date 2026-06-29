/**
 * Generación de conjuntos AP propuestos por IA.
 * Una propuesta IA nace siempre desde un único conjunto AP relevado en campo.
 */

import { useMemo, useState } from "react";
import {
  BrainCircuit,
  Eye,
  Layers3,
  RadioTower,
  Sparkles,
  Trash2,
} from "lucide-react";
import { useParams } from "react-router-dom";
import {
  Button,
  ConfirmDialog,
  EmptyState,
  useToast,
} from "@/shared/components";
import { ConjuntoAPPreviewModal } from "../components/ConjuntoAPPreviewModal";
import {
  useConjuntosPorPlanos,
  useEliminarConjuntoAP,
  useGenerarConjuntosIAProyecto,
  useMapasPorPlanos,
  usePlanosProyecto,
} from "../hooks/useProyectosOrg";
import type {
  ConjuntoAPOut,
  MapaCalorOut,
  RestriccionesIAIn,
} from "../types";
import conjuntosStyles from "./ConjuntosAPProyecto.module.css";
import styles from "./EscenariosProyecto.module.css";

const DEFAULT_FORM: Omit<RestriccionesIAIn, "fuente_entrada"> = {
  umbral_objetivo_dbm: -70,
  resolucion: 64,
  cantidad_aps_propuestos: 3,
  cantidad_recomendaciones: 2,
};

export default function EscenariosProyecto() {
  const params = useParams();
  const toast = useToast();
  const proyectoId = Number(params.id ?? 0);

  const [form, setForm] = useState(DEFAULT_FORM);
  const [planoId, setPlanoId] = useState<number | null>(null);
  const [conjuntoFuenteId, setConjuntoFuenteId] = useState<number | null>(null);
  const [confirmarEliminacion, setConfirmarEliminacion] = useState(false);
  const [vistaPrevia, setVistaPrevia] = useState<ConjuntoAPOut | null>(null);

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
  const consultasMapas = useMapasPorPlanos(
    planoSeleccionadoId ? [planoSeleccionadoId] : [],
  );
  const conjuntos = useMemo(
    () => consultasConjuntos.flatMap((consulta) => consulta.data ?? []),
    [consultasConjuntos],
  );
  const mapasPlano = useMemo(
    () => consultasMapas.flatMap((consulta) => consulta.data ?? []),
    [consultasMapas],
  );
  const conjuntosPlano = useMemo(
    () =>
      conjuntos
        .filter((conjunto) => conjunto.plano_id === planoSeleccionadoId)
        .sort((a, b) => (a.updated_at < b.updated_at ? 1 : -1)),
    [conjuntos, planoSeleccionadoId],
  );
  const conjuntosFuente = conjuntosPlano.filter((conjunto) => conjunto.origen !== "ia");
  const conjuntosIA = useMemo(
    () =>
      conjuntosPlano
        .filter((conjunto) => conjunto.origen === "ia")
        .sort((a, b) => {
          const coberturaA = coberturaProyectada(a);
          const coberturaB = coberturaProyectada(b);
          if (coberturaA !== coberturaB) return coberturaB - coberturaA;
          return a.created_at < b.created_at ? 1 : -1;
        }),
    [conjuntosPlano],
  );
  const conjuntoFuente =
    conjuntosFuente.find((conjunto) => conjunto.id === conjuntoFuenteId) ??
    conjuntosFuente[0] ??
    null;
  const cargandoConjuntos = consultasConjuntos.some((consulta) => consulta.isLoading);
  const errorConjuntos = consultasConjuntos.some((consulta) => consulta.isError);
  const cargandoMapas = consultasMapas.some((consulta) => consulta.isLoading);
  const errorMapas = consultasMapas.some((consulta) => consulta.isError);
  const mapasPorConjunto = useMemo(() => {
    const resultado = new Map<number, MapaCalorOut[]>();
    for (const mapa of mapasPlano) {
      if (!mapa.conjunto_ap_id) continue;
      const lista = resultado.get(mapa.conjunto_ap_id) ?? [];
      lista.push(mapa);
      resultado.set(mapa.conjunto_ap_id, lista);
    }
    for (const lista of resultado.values()) {
      lista.sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
    }
    return resultado;
  }, [mapasPlano]);

  const { mutateAsync: generar, isPending: generando } =
    useGenerarConjuntosIAProyecto(proyectoId);
  const { mutateAsync: eliminarConjunto, isPending: eliminandoPropuestas } =
    useEliminarConjuntoAP();
  const puedeGenerar =
    Boolean(planoSeleccionado?.calibrado) && conjuntoFuente !== null && !generando;

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
    } catch (error) {
      toast.error(_detalleError(error, "No se pudieron generar las propuestas IA."));
    }
  };

  const handleEliminarPropuestas = async () => {
    if (conjuntosIA.length === 0) return;
    try {
      await Promise.all(conjuntosIA.map((conjunto) => eliminarConjunto(conjunto.id)));
      toast.exito("Propuestas IA eliminadas del plano.");
      setConfirmarEliminacion(false);
    } catch {
      toast.error("No se pudieron eliminar las propuestas IA.");
    }
  };

  if (cargandoPlanos || cargandoConjuntos || cargandoMapas) {
    return <div className={styles.skeleton} />;
  }
  if (errorPlanos || errorConjuntos || errorMapas) {
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
              <div className={styles.parametroLectura}>
                <span>Banda del conjunto fuente</span>
                <strong>{conjuntoFuente?.banda_objetivo ?? "5"} GHz</strong>
              </div>
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
                APs propuestos
                <input
                  type="number"
                  min={1}
                  max={8}
                  value={form.cantidad_aps_propuestos}
                  onChange={(event) =>
                    setForm((prev) => ({
                      ...prev,
                      cantidad_aps_propuestos: Number(event.target.value),
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
          <Button
            variante="danger"
            disabled={conjuntosIA.length === 0 || eliminandoPropuestas}
            onClick={() => setConfirmarEliminacion(true)}
          >
            <Trash2 size={15} aria-hidden="true" />
            Eliminar propuestas IA
          </Button>
        </div>
        {conjuntosIA.length === 0 ? (
          <EmptyState mensaje="Todavía no hay conjuntos IA generados para este plano." />
        ) : (
          <div className={conjuntosStyles.tablaWrapper}>
            <table className={conjuntosStyles.tabla}>
              <thead>
                <tr>
                  <th>Conjunto</th>
                  <th>Plano</th>
                  <th>Vista</th>
                  <th>Origen</th>
                  <th>Banda</th>
                  <th>APs</th>
                </tr>
              </thead>
              <tbody>
                {conjuntosIA.map((conjunto) => (
                  <tr key={conjunto.id}>
                    <td className={conjuntosStyles.nombre}>
                      <strong>{conjunto.nombre}</strong>
                      <small>
                        {coberturaProyectada(conjunto).toFixed(1)}% cobertura
                      </small>
                    </td>
                    <td>{planoSeleccionado?.nombre ?? `Plano #${conjunto.plano_id}`}</td>
                    <td>
                      <Button
                        variante="secondary"
                        tamano="sm"
                        disabled={!planoSeleccionado || conjunto.items.length === 0}
                        onClick={() => setVistaPrevia(conjunto)}
                      >
                        <Eye size={14} aria-hidden="true" />
                        Previsualizar
                      </Button>
                    </td>
                    <td>{_labelOrigen(conjunto.origen)}</td>
                    <td>
                      <span className={conjuntosStyles.banda}>
                        {conjunto.banda_objetivo} GHz
                      </span>
                    </td>
                    <td>{conjunto.cantidad_aps}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {vistaPrevia && planoSeleccionado && (
        <ConjuntoAPPreviewModal
          conjunto={vistaPrevia}
          mapas={mapasPorConjunto.get(vistaPrevia.id) ?? []}
          plano={planoSeleccionado}
          onCerrar={() => setVistaPrevia(null)}
        />
      )}

      {confirmarEliminacion && (
        <ConfirmDialog
          titulo="¿Eliminar propuestas IA del plano?"
          descripcion="Se eliminarán los conjuntos AP generados por IA del plano seleccionado. Los conjuntos técnicos usados como fuente no serán modificados."
          textoConfirmar="Eliminar propuestas"
          cargando={eliminandoPropuestas}
          onCancelar={() => setConfirmarEliminacion(false)}
          onConfirmar={handleEliminarPropuestas}
        />
      )}
    </section>
  );
}

function numeroMetrica(
  metricas: Record<string, unknown> | null,
  clave: string,
): number | null {
  const valor = metricas?.[clave];
  return typeof valor === "number" ? valor : null;
}

function coberturaProyectada(conjunto: ConjuntoAPOut): number {
  return (
    numeroMetrica(conjunto.metricas_ia, "pct_cobertura_proyectada") ??
    numeroMetrica(conjunto.metricas_ia, "pct_cobertura") ??
    0
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

function _detalleError(error: unknown, alternativo: string): string {
  return (
    (error as { response?: { data?: { detail?: string } } })?.response?.data
      ?.detail ?? alternativo
  );
}
