/**
 * Generación de escenarios propuestos por IA.
 * Una propuesta IA nace siempre desde datos relevados en campo.
 */

import { useEffect, useMemo, useRef, useState } from "react";
import type { QueryClient } from "@tanstack/react-query";
import { useQueryClient } from "@tanstack/react-query";
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
import { listarConjuntosPlano, listarMapasPlano } from "../api/proyectosApi";
import {
  useConjuntosPorPlanos,
  useEliminarConjuntoAP,
  useGenerarConjuntosIAProyecto,
  useMapasPorPlanos,
  usePlanosProyecto,
  usePrepararConjuntoIAProyecto,
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
  const queryClient = useQueryClient();
  const proyectoId = Number(params.id ?? 0);

  const [form, setForm] = useState(DEFAULT_FORM);
  const [planoId, setPlanoId] = useState<number | null>(null);
  const [conjuntoFuenteId, setConjuntoFuenteId] = useState<number | null>(null);
  const [confirmarEliminacion, setConfirmarEliminacion] = useState(false);
  const [propuestaEliminar, setPropuestaEliminar] = useState<ConjuntoAPOut | null>(
    null,
  );
  const [vistaPrevia, setVistaPrevia] = useState<ConjuntoAPOut | null>(null);
  const [verificandoGeneracion, setVerificandoGeneracion] = useState(false);
  const preparacionesSolicitadasRef = useRef(new Set<string>());

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
  const { mutateAsync: prepararConjuntoIA } =
    usePrepararConjuntoIAProyecto(proyectoId);
  const { mutateAsync: eliminarConjunto, isPending: eliminandoPropuestas } =
    useEliminarConjuntoAP();
  const puedeGenerar =
    Boolean(planoSeleccionado?.calibrado) &&
    conjuntoFuente !== null &&
    !generando &&
    !verificandoGeneracion;

  useEffect(() => {
    if (!planoSeleccionado?.calibrado || !conjuntoFuente || proyectoId <= 0) return;
    const clave = `${proyectoId}:${planoSeleccionado.id}:${conjuntoFuente.id}:${conjuntoFuente.updated_at}`;
    if (preparacionesSolicitadasRef.current.has(clave)) return;
    preparacionesSolicitadasRef.current.add(clave);
    prepararConjuntoIA(conjuntoFuente.id).catch(() => undefined);
  }, [conjuntoFuente, planoSeleccionado, prepararConjuntoIA, proyectoId]);

  const handleGenerar = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!planoSeleccionado?.calibrado) {
      toast.error("Seleccione un plano calibrado antes de generar propuestas IA.");
      return;
    }
    if (!conjuntoFuente) {
      toast.error("Seleccione datos de campo relevados por el técnico.");
      return;
    }
    const idsIAAntes = new Set(conjuntosIA.map((conjunto) => conjunto.id));
    try {
      const respuesta = await generar({
        ...form,
        plano_id: planoSeleccionado.id,
        fuente_entrada: {
          tipo: "CONJUNTO_EXISTENTE",
          conjunto_id: conjuntoFuente.id,
        },
      });
      toast.exito(`${respuesta.conjuntos.length} propuesta(s) IA generada(s).`);
    } catch (error) {
      if (_esErrorGeneracionDiferida(error)) {
        setVerificandoGeneracion(true);
        toast.info("La generación IA sigue procesándose. Verificando resultados...");
        try {
          const propuestasNuevas = await _esperarPropuestasIA({
            planoId: planoSeleccionado.id,
            idsIAAntes,
            cantidadEsperada: form.cantidad_recomendaciones,
          });
          await _refrescarDatosRF({
            queryClient,
            proyectoId,
            planoId: planoSeleccionado.id,
          });
          if (propuestasNuevas.length > 0) {
            toast.exito(`${propuestasNuevas.length} propuesta(s) IA generada(s).`);
          } else {
            toast.info(
              "La solicitud tardó más de lo esperado. Actualice en unos segundos para verificar el resultado.",
            );
          }
        } finally {
          setVerificandoGeneracion(false);
        }
        return;
      }
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

  const handleEliminarPropuesta = async () => {
    if (!propuestaEliminar) return;
    try {
      await eliminarConjunto(propuestaEliminar.id);
      toast.exito("Propuesta IA eliminada.");
      setPropuestaEliminar(null);
      if (vistaPrevia?.id === propuestaEliminar.id) {
        setVistaPrevia(null);
      }
    } catch {
      toast.error("No se pudo eliminar la propuesta IA.");
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
        <h1 className={styles.titulo}>Escenarios generados por IA</h1>
        <p className={styles.subtitulo}>
          Genere alternativas IA derivadas desde datos reales relevados por
          el técnico de campo.
        </p>
      </header>

      <form className={styles.panelGeneracion} onSubmit={handleGenerar}>
        <div className={styles.panelHeader}>
          <div>
            <h3>Fuente de generación</h3>
            <p>La IA reutiliza datos de campo existentes y crea propuestas derivadas.</p>
          </div>
          <Button
            type="submit"
            disabled={!puedeGenerar}
            isLoading={generando || verificandoGeneracion}
          >
            <Sparkles size={16} aria-hidden="true" />
            {verificandoGeneracion ? "Verificando propuestas" : "Generar propuestas"}
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
                <h2>Datos de campo fuente</h2>
              </div>
              {conjuntosFuente.length === 0 ? (
                <p className={styles.subtitulo}>
                  No hay datos relevados por el técnico en este plano.
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
                <span>Banda de la fuente</span>
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
              {conjuntosIA.length} propuesta(s) IA asociada(s) al plano seleccionado.
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
          <EmptyState mensaje="Todavía no hay propuestas IA generadas para este plano." />
        ) : (
          <div className={conjuntosStyles.tablaWrapper}>
            <table className={conjuntosStyles.tabla}>
              <thead>
                <tr>
                  <th>Propuesta</th>
                  <th>Plano</th>
                  <th>Vista</th>
                  <th>Origen</th>
                  <th>Banda</th>
                  <th>APs</th>
                  <th>Acciones</th>
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
                    <td>
                      <Button
                        variante="danger"
                        tamano="sm"
                        disabled={eliminandoPropuestas}
                        onClick={() => setPropuestaEliminar(conjunto)}
                      >
                        <Trash2 size={14} aria-hidden="true" />
                        Eliminar
                      </Button>
                    </td>
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
          descripcion="Se eliminarán las propuestas IA del plano seleccionado. Los datos de campo usados como fuente no serán modificados."
          textoConfirmar="Eliminar propuestas"
          cargando={eliminandoPropuestas}
          onCancelar={() => setConfirmarEliminacion(false)}
          onConfirmar={handleEliminarPropuestas}
        />
      )}

      {propuestaEliminar && (
        <ConfirmDialog
          titulo={`¿Eliminar "${propuestaEliminar.nombre}"?`}
          descripcion="Se eliminará únicamente esta propuesta IA. Los datos de campo usados como fuente no serán modificados."
          textoConfirmar="Eliminar"
          cargando={eliminandoPropuestas}
          onCancelar={() => setPropuestaEliminar(null)}
          onConfirmar={handleEliminarPropuesta}
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

function _esErrorGeneracionDiferida(error: unknown): boolean {
  const errorHttp = error as {
    code?: string;
    message?: string;
    response?: { status?: number };
  };
  const status = errorHttp.response?.status;
  if (status === 502 || status === 503 || status === 504) return true;
  if (typeof status === "number" && status >= 500) return true;
  if (!errorHttp.response) return true;

  const code = errorHttp.code ?? "";
  const message = (errorHttp.message ?? "").toLowerCase();
  return (
    code === "ECONNABORTED" ||
    code === "ERR_NETWORK" ||
    message.includes("timeout") ||
    message.includes("network")
  );
}

async function _esperarPropuestasIA({
  planoId,
  idsIAAntes,
  cantidadEsperada,
}: {
  planoId: number;
  idsIAAntes: Set<number>;
  cantidadEsperada: number;
}): Promise<ConjuntoAPOut[]> {
  const intentos = 18;
  const esperaMs = 5000;
  let ultimasCompletas: ConjuntoAPOut[] = [];
  for (let intento = 0; intento < intentos; intento += 1) {
    if (intento > 0) await _esperar(esperaMs);
    try {
      const [conjuntos, mapas] = await Promise.all([
        listarConjuntosPlano(planoId),
        listarMapasPlano(planoId),
      ]);
      const nuevas = conjuntos.filter(
        (conjunto) => conjunto.origen === "ia" && !idsIAAntes.has(conjunto.id),
      );
      const idsConMapa = new Set(
        mapas
          .map((mapa) => mapa.conjunto_ap_id)
          .filter((id): id is number => typeof id === "number"),
      );
      ultimasCompletas = nuevas.filter((conjunto) => idsConMapa.has(conjunto.id));
      if (
        ultimasCompletas.length > 0 &&
        ultimasCompletas.length >= cantidadEsperada
      ) {
        return ultimasCompletas;
      }
    } catch {
      // El backend puede seguir procesando mientras el proxy corta consultas
      // intermedias; se reintenta sin mostrar error falso al usuario.
    }
  }
  return ultimasCompletas;
}

async function _refrescarDatosRF({
  queryClient,
  proyectoId,
  planoId,
}: {
  queryClient: QueryClient;
  proyectoId: number;
  planoId: number;
}) {
  await Promise.all([
    queryClient.invalidateQueries({ queryKey: ["admin", "planos", planoId] }),
    queryClient.invalidateQueries({ queryKey: ["admin", "planos"] }),
    queryClient.invalidateQueries({
      queryKey: ["admin", "proyectos", proyectoId, "enlaces-cliente"],
    }),
  ]);
}

function _esperar(ms: number): Promise<void> {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}
