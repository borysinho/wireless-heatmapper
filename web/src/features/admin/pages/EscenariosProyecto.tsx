/**
 * Gestión admin de escenarios IA por proyecto y plano.
 * PB-07/PB-12 ajustadas a gobernanza móvil/web del documento 18.
 */

import { useMemo, useState } from "react";
import {
  CheckCircle2,
  GitCompareArrows,
  Map as MapIcon,
  RadioTower,
  Send,
  Sparkles,
  Trash2,
  XCircle,
} from "lucide-react";
import { useParams } from "react-router-dom";
import {
  Badge,
  Button,
  ConfirmDialog,
  EmptyState,
  useToast,
} from "@/shared/components";
import { resolverUrlApi } from "@/shared/api/urlApi";
import {
  useCambiarEstadoEscenario,
  useComparacionEscenario,
  useConjuntosPorPlanos,
  useEliminarEscenario,
  useEliminarEscenariosProyecto,
  useEscenariosProyecto,
  useGenerarEscenariosProyecto,
  usePlanosProyecto,
} from "../hooks/useProyectosOrg";
import type {
  EscenarioOptimizadoOut,
  EstadoGobernanzaEscenario,
  PlanoOut,
  RestriccionesEscenarioIn,
} from "../types";
import { MapaCalorInteractivo } from "../components/MapaCalorInteractivo";
import styles from "./EscenariosProyecto.module.css";

const DEFAULT_FORM: RestriccionesEscenarioIn = {
  bandas: ["2.4", "5"],
  umbral_objetivo_dbm: -70,
  resolucion: 64,
  cantidad_recomendaciones: 3,
};

interface GrupoEscenarios {
  id: string;
  nombre: string;
  tipo: string;
  cantidadAps: number;
  escenarios: EscenarioOptimizadoOut[];
}

export default function EscenariosProyecto() {
  const params = useParams();
  const toast = useToast();
  const proyectoId = Number(params.id ?? 0);

  const [form, setForm] = useState<RestriccionesEscenarioIn>(DEFAULT_FORM);
  const [planoId, setPlanoId] = useState<number | null>(null);
  const [conjuntoFuenteId, setConjuntoFuenteId] = useState<number | null>(null);
  const [escenarioComparacionId, setEscenarioComparacionId] = useState<number | null>(
    null,
  );
  const [confirmarDescartarTodos, setConfirmarDescartarTodos] = useState(false);
  const [confirmarEliminarTodos, setConfirmarEliminarTodos] = useState(false);
  const [grupoEliminar, setGrupoEliminar] = useState<GrupoEscenarios | null>(null);
  const [descartandoTodos, setDescartandoTodos] = useState(false);
  const [eliminandoGrupo, setEliminandoGrupo] = useState(false);

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
  const conjuntosPlano = consultasConjuntos
    .flatMap((consulta) => consulta.data ?? [])
    .filter(
      (conjunto) =>
        conjunto.plano_id === planoSeleccionadoId &&
        conjunto.estado_gobernanza !== "descartado",
    );
  const conjuntoFuenteSeleccionado =
    conjuntosPlano.find((conjunto) => conjunto.id === conjuntoFuenteId) ?? null;
  const { data: escenarios, isLoading, isError } = useEscenariosProyecto(proyectoId);
  const { mutateAsync: generar, isPending: generando } =
    useGenerarEscenariosProyecto(proyectoId);
  const { mutateAsync: cambiarEstado, isPending: cambiandoEstado } =
    useCambiarEstadoEscenario(proyectoId);
  const { mutateAsync: eliminarEscenario, isPending: eliminandoEscenario } =
    useEliminarEscenario(proyectoId);
  const { mutateAsync: eliminarTodos, isPending: eliminandoTodos } =
    useEliminarEscenariosProyecto(proyectoId);
  const {
    data: comparacion,
    isLoading: cargandoComparacion,
    isError: errorComparacion,
  } = useComparacionEscenario(escenarioComparacionId);

  const puedeGenerar =
    Boolean(planoSeleccionado?.calibrado) &&
    conjuntoFuenteSeleccionado !== null &&
    !generando;

  const escenariosOrdenados = useMemo(
    () => [...(escenarios ?? [])].sort((a, b) => b.pct_cobertura - a.pct_cobertura),
    [escenarios],
  );
  const escenariosDescartables = useMemo(
    () =>
      escenariosOrdenados.filter(
        (escenario) => escenario.estado_gobernanza !== "descartado",
      ),
    [escenariosOrdenados],
  );
  const resumenEscenarios = useMemo(
    () =>
      escenariosOrdenados.reduce(
        (acc, escenario) => {
          acc.total += 1;
          if (escenario.estado_gobernanza === "pendiente_revision") {
            acc.pendientes += 1;
          }
          if (escenario.estado_gobernanza === "aprobado_interno") {
            acc.aprobados += 1;
          }
          if (escenario.estado_gobernanza === "publicado_cliente") {
            acc.publicados += 1;
          }
          if (escenario.estado_gobernanza === "descartado") {
            acc.descartados += 1;
          }
          return acc;
        },
        { total: 0, pendientes: 0, aprobados: 0, publicados: 0, descartados: 0 },
      ),
    [escenariosOrdenados],
  );
  const gruposEscenarios = useMemo(
    () => _agruparEscenariosPorFuente(escenariosOrdenados),
    [escenariosOrdenados],
  );

  const handleToggleBanda = (banda: "2.4" | "5") => {
    setForm((prev) => {
      const bandas = prev.bandas.includes(banda)
        ? prev.bandas.filter((item) => item !== banda)
        : [...prev.bandas, banda];
      return { ...prev, bandas: bandas.length > 0 ? bandas : [banda] };
    });
  };

  const handleGenerar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!planoSeleccionado?.calibrado) {
      toast.error("Seleccione un plano calibrado antes de generar la recomendación IA.");
      return;
    }
    if (!conjuntoFuenteSeleccionado) {
      toast.error("Seleccione un conjunto de APs completo para IA.");
      return;
    }
    try {
      const respuesta = await generar({
        ...form,
        plano_id: planoSeleccionado.id,
        fuente_entrada: {
          tipo: "CONJUNTO_EXISTENTE",
          nombre: conjuntoFuenteSeleccionado.nombre,
          proposito: conjuntoFuenteSeleccionado.proposito,
          ap_ids: [],
          bssids: [],
          conjunto_id: conjuntoFuenteSeleccionado.id,
        },
      });
      toast.exito(`${respuesta.escenarios.length} recomendación IA generada.`);
    } catch (error) {
      toast.error(
        _detalleError(
          error,
          "No se pudo generar la recomendación IA. Revise plano, conjunto y mediciones.",
        ),
      );
    }
  };

  const handleEstado = async (
    escenario: EscenarioOptimizadoOut,
    estadoGobernanza: EstadoGobernanzaEscenario,
  ) => {
    try {
      await cambiarEstado({ escenarioId: escenario.id, estadoGobernanza });
      toast.exito(`Escenario "${escenario.nombre}" actualizado.`);
    } catch {
      toast.error("No se pudo cambiar el estado del escenario.");
    }
  };

  const handleDescartarTodos = async () => {
    if (escenariosDescartables.length === 0) {
      setConfirmarDescartarTodos(false);
      return;
    }
    setDescartandoTodos(true);
    try {
      for (const escenario of escenariosDescartables) {
        await cambiarEstado({
          escenarioId: escenario.id,
          estadoGobernanza: "descartado",
        });
      }
      toast.exito(`${escenariosDescartables.length} escenario(s) descartado(s).`);
      setConfirmarDescartarTodos(false);
    } catch {
      toast.error("No se pudieron descartar todos los escenarios IA.");
    } finally {
      setDescartandoTodos(false);
    }
  };

  const handleEliminarTodos = async () => {
    try {
      const respuesta = await eliminarTodos();
      toast.exito(`${respuesta.eliminados} recomendación(es) eliminada(s).`);
      setConfirmarEliminarTodos(false);
    } catch {
      toast.error("No se pudieron eliminar permanentemente las recomendaciones IA.");
    }
  };

  const handleEliminarGrupo = async () => {
    if (!grupoEliminar) return;
    setEliminandoGrupo(true);
    try {
      for (const escenario of grupoEliminar.escenarios) {
        await eliminarEscenario(escenario.id);
      }
      toast.exito(
        `${grupoEliminar.escenarios.length} recomendación(es) eliminada(s).`,
      );
      setGrupoEliminar(null);
    } catch {
      toast.error("No se pudo eliminar el grupo de recomendaciones IA.");
    } finally {
      setEliminandoGrupo(false);
    }
  };

  return (
    <div>
      <div className={styles.intro}>
        <div>
          <h2>Generación y revisión de escenarios IA</h2>
          <p>
            Las recomendaciones nacen como resultados internos y solo pasan al cliente
            desde la publicación del proyecto.
          </p>
        </div>
      </div>

      <form className={styles.panelGeneracion} onSubmit={handleGenerar}>
        <div className={styles.panelHeader}>
          <div>
            <h3>Preparación de entrada</h3>
            <p>
              {planoSeleccionado?.nombre ?? "Sin mapa"} ·{" "}
              {conjuntoFuenteSeleccionado
                ? `${conjuntoFuenteSeleccionado.nombre} · ${conjuntoFuenteSeleccionado.cantidad_aps} APs`
                : "sin conjunto seleccionado"}
            </p>
          </div>
          <Button type="submit" isLoading={generando} disabled={!puedeGenerar}>
            <Sparkles size={16} aria-hidden="true" />
            Generar recomendación
          </Button>
        </div>

        <div className={styles.generacionGrid}>
          <div className={styles.columnaFuente}>
            <section className={styles.banda}>
              <div className={styles.seccionHeader}>
                <MapIcon size={18} aria-hidden="true" />
                <h2>Mapa base</h2>
              </div>
              {cargandoPlanos ? (
                <div className={styles.skeleton} />
              ) : errorPlanos ? (
                <EmptyState mensaje="No se pudieron cargar los planos del proyecto." />
              ) : planosOrdenados.length === 0 ? (
                <EmptyState mensaje="El proyecto todavía no tiene planos importados." />
              ) : (
                <div className={styles.planosGrid}>
                  {planosOrdenados.map((plano) => (
                    <button
                      type="button"
                      key={plano.id}
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
                        {plano.calibrado ? "Calibrado" : "Sin calibrar"} ·{" "}
                        {plano.cantidad_puntos} puntos
                      </small>
                    </button>
                  ))}
                </div>
              )}
            </section>

            <section className={styles.banda}>
              <div className={styles.seccionHeader}>
                <RadioTower size={18} aria-hidden="true" />
                <h2>Conjunto completo de entrada</h2>
              </div>
              {planoSeleccionadoId === null ? (
                <EmptyState mensaje="Seleccione un mapa para ver sus conjuntos." />
              ) : conjuntosPlano.length === 0 ? (
                <EmptyState mensaje="Este mapa todavía no tiene conjuntos de APs disponibles para IA." />
              ) : (
                <div className={styles.conjuntosGrid}>
                  {conjuntosPlano.map((conjunto) => (
                    <button
                      type="button"
                      key={conjunto.id}
                      className={`${styles.conjuntoCard} ${
                        conjunto.id === conjuntoFuenteId ? styles.conjuntoActivo : ""
                      }`}
                      onClick={() => setConjuntoFuenteId(conjunto.id)}
                    >
                      <span>{conjunto.nombre}</span>
                      <small>
                        {conjunto.proposito} · {conjunto.cantidad_aps} APs ·{" "}
                        {_labelEstadoGobernanza(conjunto.estado_gobernanza)}
                      </small>
                    </button>
                  ))}
                </div>
              )}
            </section>
          </div>

          <section className={`${styles.banda} ${styles.panelParametros}`}>
            <div className={styles.seccionHeader}>
              <Sparkles size={18} aria-hidden="true" />
              <h2>Parámetros IA</h2>
            </div>
            {conjuntoFuenteSeleccionado && (
              <div className={styles.detalleConjunto}>
                <strong>{conjuntoFuenteSeleccionado.nombre}</strong>
                <span>
                  {conjuntoFuenteSeleccionado.cantidad_aps} APs serán evaluados como
                  conjunto completo para mostrar las mejores recomendaciones.
                </span>
              </div>
            )}

            <div className={styles.formulario}>
              <fieldset className={styles.campoBandas}>
                <legend>Bandas a optimizar</legend>
                <label>
                  <input
                    type="checkbox"
                    checked={form.bandas.includes("2.4")}
                    onChange={() => handleToggleBanda("2.4")}
                  />
                  2,4 GHz
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={form.bandas.includes("5")}
                    onChange={() => handleToggleBanda("5")}
                  />
                  5 GHz
                </label>
              </fieldset>

              <label>
                Umbral RSSI objetivo
                <input
                  type="number"
                  min={-90}
                  max={-50}
                  value={form.umbral_objetivo_dbm}
                  onChange={(e) =>
                    setForm((prev) => ({
                      ...prev,
                      umbral_objetivo_dbm: Number(e.target.value),
                    }))
                  }
                />
              </label>

              <label>
                Cantidad de recomendaciones
                <input
                  type="number"
                  min={1}
                  max={5}
                  value={form.cantidad_recomendaciones}
                  onChange={(e) =>
                    setForm((prev) => ({
                      ...prev,
                      cantidad_recomendaciones: Number(e.target.value),
                    }))
                  }
                />
              </label>

              <label>
                Resolución
                <select
                  value={form.resolucion}
                  onChange={(e) =>
                    setForm((prev) => ({ ...prev, resolucion: Number(e.target.value) }))
                  }
                >
                  <option value={32}>32</option>
                  <option value={64}>64</option>
                  <option value={128}>128</option>
                </select>
              </label>
            </div>
          </section>
        </div>
      </form>

      <section className={styles.resultados}>
        <div className={styles.resultadosHeader}>
          <div>
            <h2>Recomendaciones IA</h2>
            <p>
              {resumenEscenarios.total} total · {resumenEscenarios.pendientes} pendientes ·{" "}
              {resumenEscenarios.aprobados} aprobados · {resumenEscenarios.publicados} publicados ·{" "}
              {resumenEscenarios.descartados} descartados
            </p>
          </div>
          <div className={styles.accionesMasivas}>
            <Button
              type="button"
              variante="secondary"
              tamano="sm"
              disabled={
                escenariosDescartables.length === 0 ||
                cambiandoEstado ||
                descartandoTodos ||
                eliminandoTodos
              }
              onClick={() => setConfirmarDescartarTodos(true)}
            >
              <XCircle size={14} aria-hidden="true" />
              Descartar todos
            </Button>
            <Button
              type="button"
              variante="danger"
              tamano="sm"
              disabled={
                escenariosOrdenados.length === 0 ||
                eliminandoTodos ||
                eliminandoEscenario ||
                eliminandoGrupo
              }
              onClick={() => setConfirmarEliminarTodos(true)}
            >
              <Trash2 size={14} aria-hidden="true" />
              Borrar todo
            </Button>
          </div>
        </div>

        {isLoading ? (
          <div className={styles.skeleton} />
        ) : isError ? (
          <EmptyState mensaje="No se pudieron cargar los escenarios IA." />
        ) : escenariosOrdenados.length === 0 ? (
          <EmptyState mensaje="Aún no hay recomendaciones IA para este proyecto." />
        ) : (
          <div className={styles.grupos}>
            {gruposEscenarios.map((grupo) => (
              <section key={grupo.id} className={styles.grupo}>
                <div className={styles.grupoHeader}>
                  <div>
                    <h3>{grupo.nombre}</h3>
                    <p>
                      {grupo.tipo} · {grupo.escenarios.length} recomendación(es) ·{" "}
                      {grupo.cantidadAps > 0
                        ? `${grupo.cantidadAps} APs de entrada`
                        : "APs de entrada registrados en la fuente"}
                    </p>
                  </div>
                  <Button
                    type="button"
                    variante="danger"
                    tamano="sm"
                    disabled={eliminandoEscenario || eliminandoGrupo || eliminandoTodos}
                    onClick={() => setGrupoEliminar(grupo)}
                  >
                    <Trash2 size={14} aria-hidden="true" />
                    Borrar grupo
                  </Button>
                </div>

                <div className={styles.lista}>
                  {grupo.escenarios.map((escenario) => (
                    <article key={escenario.id} className={styles.escenario}>
                      <div className={styles.escenarioHeader}>
                        <div>
                          <h2>{escenario.nombre}</h2>
                          <p>
                            Plano #{escenario.plano_id} · {_fuenteEscenario(escenario)} ·{" "}
                            {escenario.resumen}
                          </p>
                        </div>
                        <Badge
                          variante="en_progreso"
                          etiqueta={_labelEstadoGobernanza(escenario.estado_gobernanza)}
                        />
                      </div>

                      <div className={styles.metricas}>
                        <span>{escenario.pct_cobertura_actual.toFixed(1)}% actual</span>
                        <span>{escenario.pct_cobertura.toFixed(1)}% proyectada</span>
                        <span>{escenario.cantidad_aps} APs</span>
                        <span>Confianza {escenario.confianza}</span>
                        <span>{escenario.bandas.join(" / ")} GHz</span>
                      </div>

                      <VistaHeatmapsEscenario
                        escenario={escenario}
                        planos={planosOrdenados}
                      />

                      <div className={styles.recomendacionesCompactas}>
                        {escenario.recomendaciones.map((rec) => (
                          <div key={rec.id} className={styles.recomendacionCompacta}>
                            <RadioTower size={16} aria-hidden="true" />
                            <span>
                              <strong>AP sugerido {rec.orden}</strong>
                              <small>
                                {_labelAccion(rec.accion)} · {rec.banda} GHz · RSSI{" "}
                                {rec.rssi_proyectado.toFixed(1)} dBm
                              </small>
                            </span>
                          </div>
                        ))}
                      </div>

                      <div className={styles.accionesEscenario}>
                        <Button
                          variante="ghost"
                          tamano="sm"
                          onClick={() => setEscenarioComparacionId(escenario.id)}
                        >
                          <GitCompareArrows size={14} aria-hidden="true" />
                          Ampliar comparación
                        </Button>
                        <Button
                          variante="secondary"
                          tamano="sm"
                          disabled={cambiandoEstado}
                          onClick={() => handleEstado(escenario, "aprobado_interno")}
                        >
                          <CheckCircle2 size={14} aria-hidden="true" />
                          Aprobar
                        </Button>
                        <Button
                          variante="secondary"
                          tamano="sm"
                          disabled={cambiandoEstado}
                          onClick={() => handleEstado(escenario, "publicado_cliente")}
                        >
                          <Send size={14} aria-hidden="true" />
                          Publicar
                        </Button>
                        <Button
                          variante="ghost"
                          tamano="sm"
                          disabled={cambiandoEstado}
                          onClick={() => handleEstado(escenario, "descartado")}
                        >
                          <XCircle size={14} aria-hidden="true" />
                          Descartar
                        </Button>
                      </div>
                    </article>
                  ))}
                </div>
              </section>
            ))}
          </div>
        )}
      </section>
      {escenarioComparacionId && (
        <section className={styles.comparacion}>
          <div className={styles.resultadosHeader}>
            <div>
              <h2>Comparación actual y proyectada</h2>
              <p>La evidencia observada permanece separada de la proyección IA.</p>
            </div>
            <Button
              variante="ghost"
              tamano="sm"
              onClick={() => setEscenarioComparacionId(null)}
            >
              Cerrar
            </Button>
          </div>
          {cargandoComparacion ? (
            <div className={styles.skeleton} />
          ) : errorComparacion || !comparacion ? (
            <EmptyState mensaje="No se pudo cargar la comparación del escenario." />
          ) : (
            <>
              <div className={styles.comparacionMetricas}>
                <span>{comparacion.escenario.pct_cobertura_actual.toFixed(1)}% actual</span>
                <span>{comparacion.escenario.pct_cobertura.toFixed(1)}% proyectada</span>
                <span>{comparacion.resumen.delta_pct_cobertura.toFixed(1)} pp</span>
                <span>{comparacion.resumen.cantidad_cambios} cambios</span>
              </div>
              <div className={styles.heatmapsComparacion}>
                <figure>
                  <figcaption>Heatmap actual observado</figcaption>
                  <img
                    src={resolverUrlApi(comparacion.heatmap_actual.url_imagen)}
                    alt="Heatmap actual observado"
                  />
                </figure>
                <figure>
                  <figcaption>Heatmap proyectado por IA</figcaption>
                  <img
                    src={resolverUrlApi(comparacion.heatmap_proyectado.url_imagen)}
                    alt="Heatmap proyectado por IA"
                  />
                </figure>
              </div>
            </>
          )}
        </section>
      )}
      {confirmarDescartarTodos && (
        <ConfirmDialog
          titulo="¿Descartar todos los escenarios IA?"
          descripcion={`Se marcarán como descartados ${escenariosDescartables.length} escenario(s). Esta acción conserva los registros para auditoría.`}
          textoConfirmar="Descartar todos"
          cargando={descartandoTodos}
          onCancelar={() => setConfirmarDescartarTodos(false)}
          onConfirmar={handleDescartarTodos}
        />
      )}
      {confirmarEliminarTodos && (
        <ConfirmDialog
          titulo="¿Borrar permanentemente todas las recomendaciones IA?"
          descripcion={`Se eliminarán ${escenariosOrdenados.length} recomendación(es) y sus ubicaciones sugeridas. Use esta acción solo cuando quiera limpiar por completo los resultados generados.`}
          textoConfirmar="Borrar todo"
          cargando={eliminandoTodos}
          onCancelar={() => setConfirmarEliminarTodos(false)}
          onConfirmar={handleEliminarTodos}
        />
      )}
      {grupoEliminar && (
        <ConfirmDialog
          titulo={`¿Borrar "${grupoEliminar.nombre}"?`}
          descripcion={`Se eliminarán permanentemente ${grupoEliminar.escenarios.length} recomendación(es) de este grupo.`}
          textoConfirmar="Borrar grupo"
          cargando={eliminandoGrupo}
          onCancelar={() => setGrupoEliminar(null)}
          onConfirmar={handleEliminarGrupo}
        />
      )}
    </div>
  );
}

function VistaHeatmapsEscenario({
  escenario,
  planos,
}: {
  escenario: EscenarioOptimizadoOut;
  planos: PlanoOut[];
}) {
  const {
    data: comparacion,
    isLoading,
    isError,
  } = useComparacionEscenario(escenario.id);
  const plano = planos.find((item) => item.id === escenario.plano_id);

  if (isLoading) {
    return <div className={styles.skeletonHeatmap} />;
  }

  if (isError || !comparacion || !plano) {
    return (
      <div className={styles.heatmapNoDisponible}>
        No se pudo cargar la visualización del escenario.
      </div>
    );
  }

  return (
    <div className={styles.heatmapsEscenario}>
      <MapaCalorInteractivo
        mapa={comparacion.heatmap_actual}
        plano={plano}
        titulo="Cobertura actual observada"
        compacto
      />
      <MapaCalorInteractivo
        mapa={comparacion.heatmap_proyectado}
        plano={plano}
        titulo="Cobertura proyectada por IA"
        apHints={_hintsRecomendaciones(escenario)}
        compacto
      />
    </div>
  );
}

function _fuenteEscenario(escenario: EscenarioOptimizadoOut): string {
  const fuente = escenario.restricciones.fuente_entrada as
    | {
        tipo?: string;
        nombre?: string;
        ap_ids?: number[];
        bssids?: string[];
        conjunto_id?: number | null;
      }
    | undefined;
  if (fuente?.tipo === "CONJUNTO_EXISTENTE") {
    const cantidad = fuente.bssids?.length ?? escenario.cantidad_aps;
    return `${fuente.nombre ?? `Conjunto AP #${fuente.conjunto_id ?? escenario.conjunto_base_id}`} · ${cantidad} APs`;
  }
  if (fuente?.tipo === "SELECCION_APS_MAPA") {
    const cantidad = fuente.bssids?.length ?? fuente.ap_ids?.length ?? 0;
    return `${fuente.nombre ?? "Conjunto IA"} · ${cantidad} APs`;
  }
  return "fuente IA registrada";
}

function _hintsRecomendaciones(escenario: EscenarioOptimizadoOut) {
  return escenario.recomendaciones.map((rec) => ({
    titulo: `AP sugerido ${rec.orden}`,
    resumen: `${_labelAccion(rec.accion)} · ${rec.banda} GHz · RSSI ${rec.rssi_proyectado.toFixed(1)} dBm`,
    detalles: [
      `Acción: ${_labelAccion(rec.accion)}`,
      `Montaje: ${_capitalizar(rec.tipo_montaje)} · ${rec.altura_m.toFixed(1)} m`,
      `Banda: ${rec.banda} GHz`,
      `RSSI: ${rec.rssi_proyectado.toFixed(1)} dBm`,
    ],
  }));
}

function _labelAccion(accion: string): string {
  const mapa: Record<string, string> = {
    AGREGAR: "Agregar AP",
    MANTENER: "Mantener AP",
    MOVER: "Mover AP",
    RECONFIGURAR: "Reconfigurar AP",
    CAMBIAR_MODELO: "Cambiar modelo",
    RETIRAR: "Retirar AP",
  };
  return mapa[accion] ?? accion;
}

function _capitalizar(valor: string): string {
  const limpio = valor.replaceAll("_", " ").toLowerCase();
  return limpio.charAt(0).toUpperCase() + limpio.slice(1);
}

function _detalleError(error: unknown, alternativo: string): string {
  const detail = (error as { response?: { data?: { detail?: unknown } } })?.response
    ?.data?.detail;
  if (typeof detail === "string" && detail.trim().length > 0) {
    return detail;
  }
  if (Array.isArray(detail) && detail.length > 0) {
    return "La solicitud de generación IA tiene datos inválidos.";
  }
  if (error instanceof Error && error.message.trim().length > 0) {
    return error.message;
  }
  return alternativo;
}

function _labelEstadoGobernanza(estado: string): string {
  const mapa: Record<string, string> = {
    pendiente_revision: "Pendiente revisión",
    aprobado_interno: "Aprobado interno",
    publicado_cliente: "Publicado cliente",
    descartado: "Descartado",
  };
  return mapa[estado] ?? estado;
}

function _agruparEscenariosPorFuente(
  escenarios: EscenarioOptimizadoOut[],
): GrupoEscenarios[] {
  const grupos = new Map<string, GrupoEscenarios>();
  for (const escenario of escenarios) {
    const fuente = escenario.restricciones.fuente_entrada as
      | {
          tipo?: string;
          nombre?: string;
          conjunto_id?: number | null;
          bssids?: string[];
          ap_ids?: number[];
        }
      | undefined;
    const tipoFuente = fuente?.tipo ?? "FUENTE_IA";
    const conjuntoId = fuente?.conjunto_id ?? escenario.conjunto_base_id ?? null;
    const bssids = fuente?.bssids ?? [];
    const apIds = fuente?.ap_ids ?? [];
    const clave =
      conjuntoId !== null
        ? `${tipoFuente}:conjunto:${conjuntoId}`
        : `${tipoFuente}:seleccion:${bssids.join("|") || apIds.join("|") || escenario.plano_id}`;
    const nombre =
      fuente?.nombre ??
      (conjuntoId !== null
        ? `Conjunto AP #${conjuntoId}`
        : `Selección APs · Plano #${escenario.plano_id}`);
    const existente = grupos.get(clave);
    if (existente) {
      existente.escenarios.push(escenario);
      existente.cantidadAps = Math.max(
        existente.cantidadAps,
        _cantidadFuente(fuente, escenario),
      );
      continue;
    }
    grupos.set(clave, {
      id: clave,
      nombre,
      tipo: _labelTipoFuente(tipoFuente),
      cantidadAps: _cantidadFuente(fuente, escenario),
      escenarios: [escenario],
    });
  }
  return Array.from(grupos.values()).sort((a, b) => {
    const fechaA = a.escenarios[0]?.created_at ?? "";
    const fechaB = b.escenarios[0]?.created_at ?? "";
    return fechaA < fechaB ? 1 : -1;
  });
}

function _cantidadFuente(
  fuente:
    | { bssids?: string[]; ap_ids?: number[]; conjunto_id?: number | null }
    | undefined,
  escenario: EscenarioOptimizadoOut,
): number {
  return fuente?.bssids?.length ?? fuente?.ap_ids?.length ?? escenario.cantidad_aps;
}

function _labelTipoFuente(tipo: string): string {
  const mapa: Record<string, string> = {
    SELECCION_APS_MAPA: "Selección del mapa",
    INVENTARIO_RF: "Inventario RF",
    BASELINE_OBSERVADO: "Mediciones observadas",
    CONJUNTO_EXISTENTE: "Conjunto existente",
    FUENTE_IA: "Fuente IA",
  };
  return mapa[tipo] ?? tipo;
}
