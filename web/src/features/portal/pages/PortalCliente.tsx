import { useMemo, useRef, useState, type PointerEvent, type ReactNode } from "react";
import {
  BarChart3,
  BrainCircuit,
  Building2,
  Eye,
  EyeOff,
  Layers3,
  Loader2,
  MapPinned,
  Minus,
  Plus,
  RadioTower,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { resolverUrlApi } from "@/shared/api/urlApi";
import { generarHeatmapPortal, obtenerPortalCliente } from "../api/shareClient";
import type {
  MapaCalorPortalOut,
  PlanoOut,
  PortalClienteOut,
} from "@/features/admin/types";
import styles from "./PortalCliente.module.css";

type ModoGeneracion = "INDIVIDUAL" | "SUBCONJUNTO" | "CONJUNTO_COMPLETO";
type PartePortal = "RELEVAMIENTO" | "IA";

export default function PortalCliente() {
  const { token = "" } = useParams();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["portal-cliente", token],
    queryFn: () => obtenerPortalCliente(token),
    enabled: token.length > 0,
    retry: false,
  });
  const [conjuntoActivoId, setConjuntoActivoId] = useState<number | null>(null);
  const [modo, setModo] = useState<ModoGeneracion>("CONJUNTO_COMPLETO");
  const [bssidsSeleccionados, setBssidsSeleccionados] = useState<Set<string>>(
    () => new Set(),
  );
  const [mapaActivo, setMapaActivo] = useState<MapaCalorPortalOut | null>(null);
  const [parteActiva, setParteActiva] = useState<PartePortal>("RELEVAMIENTO");

  const conjuntosRelevados = useMemo(
    () => data?.conjuntos.filter((conjunto) => conjunto.origen !== "ia") ?? [],
    [data?.conjuntos],
  );
  const conjuntosIA = useMemo(
    () => data?.conjuntos.filter((conjunto) => conjunto.origen === "ia") ?? [],
    [data?.conjuntos],
  );
  const hayContenidoIA = conjuntosIA.length > 0;
  const parteVisible =
    parteActiva === "RELEVAMIENTO" && conjuntosRelevados.length === 0 && hayContenidoIA
      ? "IA"
      : parteActiva;
  const conjuntosParte = parteVisible === "IA" ? conjuntosIA : conjuntosRelevados;

  const conjuntoActivo = useMemo(
    () =>
      conjuntosParte.find((conjunto) => conjunto.id === conjuntoActivoId) ??
      conjuntosParte[0] ??
      null,
    [conjuntoActivoId, conjuntosParte],
  );

  const mapaConjuntoActivo = useMemo(
    () =>
      conjuntoActivo
        ? data?.heatmaps.find((mapa) => mapa.conjunto_ap_id === conjuntoActivo.id) ??
          null
        : null,
    [conjuntoActivo, data?.heatmaps],
  );
  const mapaMostrado = mapaActivo ?? mapaConjuntoActivo;

  const bssidsEfectivos = useMemo(() => {
    if (!conjuntoActivo) return new Set<string>();
    const bssids = conjuntoActivo.items.map((ap) => ap.bssid);
    if (modo === "CONJUNTO_COMPLETO") {
      return new Set(bssids);
    }
    const seleccionDisponibles = Array.from(bssidsSeleccionados).filter((bssid) =>
      bssids.includes(bssid),
    );
    if (modo === "INDIVIDUAL") {
      return new Set(
        seleccionDisponibles.length > 0
          ? seleccionDisponibles.slice(0, 1)
          : bssids.slice(0, 1),
      );
    }
    return new Set(
      seleccionDisponibles.length > 0
        ? seleccionDisponibles
        : bssids.slice(0, Math.min(2, bssids.length)),
    );
  }, [bssidsSeleccionados, conjuntoActivo, modo]);

  const generarHeatmap = useMutation({
    mutationFn: () => {
      if (!conjuntoActivo) throw new Error("Conjunto requerido.");
      const bssids = Array.from(bssidsEfectivos);
      return generarHeatmapPortal(token, conjuntoActivo.id, {
        modo,
        bssids: modo === "CONJUNTO_COMPLETO" ? undefined : bssids,
        algoritmo: "IDW",
        resolucion: 128,
      });
    },
    onSuccess: (mapa) => setMapaActivo(mapa),
  });

  const seleccionValida =
    !!conjuntoActivo &&
    (modo === "CONJUNTO_COMPLETO" ||
      (modo === "INDIVIDUAL" && bssidsEfectivos.size === 1) ||
      (modo === "SUBCONJUNTO" && bssidsEfectivos.size > 0));

  if (isLoading) {
    return <div className={styles.estado}>Cargando publicación...</div>;
  }

  if (isError || !data) {
    return (
      <div className={styles.estado}>
        <h1>Enlace no disponible</h1>
        <p>La publicación no existe, expiró o fue revocada por Bulldog Tech.</p>
      </div>
    );
  }

  return (
    <main className={styles.portal}>
      <header className={styles.encabezado}>
        <div>
          <span className={styles.marca}>Bulldog Tech.</span>
          <h1>{data.proyecto.nombre}</h1>
          <p>{data.proyecto.cliente ?? "Cliente"} · Portal ejecutivo de cobertura WiFi</p>
        </div>
      </header>

      <section className={styles.tableroEjecutivo} aria-label="Resumen ejecutivo">
        <Indicador icono={<Building2 size={18} />} etiqueta="Planos" valor={data.planos.length} />
        <Indicador
          icono={<RadioTower size={18} />}
          etiqueta="Conjuntos reales"
          valor={conjuntosRelevados.length}
        />
        <Indicador
          icono={<BrainCircuit size={18} />}
          etiqueta="Subconjuntos IA"
          valor={conjuntosIA.length}
        />
        <Indicador
          icono={<TrendingUp size={18} />}
          etiqueta="Heatmaps"
          valor={data.heatmaps.length}
        />
      </section>

      <section className={styles.layout}>
        <div className={styles.panelMapa}>
          <div className={styles.panelHeader}>
            <MapPinned size={18} aria-hidden="true" />
            <div>
              <h2>{parteVisible === "IA" ? "Vista del modelo IA" : "Vista del relevamiento en sitio"}</h2>
              <p>
                {conjuntoActivo
                  ? `${conjuntoActivo.nombre} · ${_labelModo(modo)}`
                  : "Seleccione un conjunto publicado para explorar el mapa."}
              </p>
            </div>
          </div>

          {mapaMostrado ? (
            <>
              <div className={styles.mapaResumen}>
                <strong>{_labelModo(mapaMostrado.modo_generacion)}</strong>
                <span>
                  {mapaMostrado.cantidad_puntos} puntos ·{" "}
                  {mapaMostrado.rssi_promedio.toFixed(1)} dBm promedio
                </span>
              </div>
              <HeatmapCanvas
                mapa={mapaMostrado}
                plano={
                  data.planos.find((plano) => plano.id === mapaMostrado.plano_id) ??
                  null
                }
              />
            </>
          ) : (
            <div className={styles.vacio}>
              {parteVisible === "IA"
                ? "Seleccione una propuesta IA y genere o revise su heatmap proyectado."
                : "Seleccione una parte, elija un conjunto y genere el heatmap interactivo."}
            </div>
          )}
        </div>

        <aside className={styles.panelLateral}>
          <section className={styles.resumen}>
            <h2>Áreas de análisis</h2>
            <div className={styles.selectorPartes}>
              <button
                type="button"
                className={parteVisible === "RELEVAMIENTO" ? styles.parteActiva : ""}
                onClick={() => {
                  setParteActiva("RELEVAMIENTO");
                  setConjuntoActivoId(conjuntosRelevados[0]?.id ?? null);
                  setBssidsSeleccionados(new Set());
                  setMapaActivo(null);
                }}
              >
                <BarChart3 size={16} aria-hidden="true" />
                <span>
                  <strong>Datos relevados</strong>
                  <small>{conjuntosRelevados.length} conjunto(s) de campo</small>
                </span>
              </button>
              <button
                type="button"
                className={parteVisible === "IA" ? styles.parteActiva : ""}
                onClick={() => {
                  setParteActiva("IA");
                  setConjuntoActivoId(conjuntosIA[0]?.id ?? null);
                  setBssidsSeleccionados(new Set());
                  setMapaActivo(null);
                }}
              >
                <BrainCircuit size={16} aria-hidden="true" />
                <span>
                  <strong>Modelo IA</strong>
                  <small>{conjuntosIA.length} propuesta(s) publicadas</small>
                </span>
              </button>
            </div>
          </section>
          <section className={styles.resumen}>
            <h2>{parteVisible === "IA" ? "Propuestas IA" : "Generación"}</h2>
            {conjuntosParte.length === 0 ? (
              <p>
                {parteVisible === "IA"
                  ? "No hay propuestas IA publicadas para este enlace."
                  : "No hay conjuntos relevados publicados para este enlace."}
              </p>
            ) : (
              <div className={styles.formGenerador}>
                <label>
                  Conjunto
                  <select
                    value={conjuntoActivo?.id ?? ""}
                    onChange={(event) => {
                      setConjuntoActivoId(Number(event.target.value));
                      setBssidsSeleccionados(new Set());
                      setMapaActivo(null);
                    }}
                  >
                    {conjuntosParte.map((conjunto) => (
                      <option key={conjunto.id} value={conjunto.id}>
                        {conjunto.nombre}
                      </option>
                    ))}
                  </select>
                </label>

                <div className={styles.modosHeatmap}>
                  {(["CONJUNTO_COMPLETO", "SUBCONJUNTO", "INDIVIDUAL"] as ModoGeneracion[]).map(
                    (modoItem) => (
                      <button
                        key={modoItem}
                        type="button"
                        className={modo === modoItem ? styles.modoActivo : ""}
                        onClick={() => {
                          setModo(modoItem);
                          setBssidsSeleccionados(new Set());
                          setMapaActivo(null);
                        }}
                      >
                        {_labelModo(modoItem)}
                      </button>
                    ),
                  )}
                </div>

                {conjuntoActivo && (
                  <div className={styles.apSelectorPortal}>
                    {conjuntoActivo.items.map((ap) => (
                      <label key={ap.bssid}>
                        <input
                          type={modo === "INDIVIDUAL" ? "radio" : "checkbox"}
                          name="ap-portal"
                          checked={bssidsEfectivos.has(ap.bssid)}
                          disabled={modo === "CONJUNTO_COMPLETO"}
                          onChange={() =>
                            setBssidsSeleccionados(
                              _toggleBssid(new Set(bssidsEfectivos), ap.bssid, modo),
                            )
                          }
                        />
                        <span>
                          <strong>{ap.ssid || "SSID oculto"}</strong>
                          <small>{ap.bssid}</small>
                        </span>
                      </label>
                    ))}
                  </div>
                )}

                <button
                  type="button"
                  className={styles.botonGenerar}
                  disabled={!seleccionValida || generarHeatmap.isPending}
                  onClick={() => generarHeatmap.mutate()}
                >
                  {generarHeatmap.isPending ? (
                    <Loader2 size={16} aria-hidden="true" />
                  ) : (
                    <RadioTower size={16} aria-hidden="true" />
                  )}
                  Generar heatmap
                </button>
                {generarHeatmap.isError && (
                  <p className={styles.errorGeneracion}>
                    No se pudo generar el heatmap con la selección actual.
                  </p>
                )}
              </div>
            )}
          </section>
        </aside>
      </section>

      <section className={styles.partes}>
        <BloqueConjuntos
          titulo="Datos reales relevados en sitio"
          descripcion="Subconjuntos publicados desde las mediciones capturadas por el equipo técnico."
          icono={<Layers3 size={18} aria-hidden="true" />}
          conjuntos={conjuntosRelevados}
          conjuntoActivoId={conjuntoActivo?.id ?? null}
          onSeleccionar={(id) => {
            setParteActiva("RELEVAMIENTO");
            setConjuntoActivoId(id);
            setBssidsSeleccionados(new Set());
            setMapaActivo(null);
          }}
        />

        <section className={styles.bloque}>
          <div className={styles.panelHeader}>
            <BrainCircuit size={18} aria-hidden="true" />
            <div>
                  <h2>Conjuntos propuestos por IA</h2>
              <p>Conjuntos propuestos por IA a partir de un conjunto relevado en campo.</p>
            </div>
          </div>

          {conjuntosIA.length === 0 ? (
            <div className={styles.vacio}>No hay resultados IA publicados en este enlace.</div>
          ) : (
            <div className={styles.iaGrid}>
              {conjuntosIA.map((conjunto) => (
                <button
                  key={conjunto.id}
                  type="button"
                  className={`${styles.conjunto} ${
                    conjunto.id === conjuntoActivo?.id ? styles.conjuntoActivo : ""
                  }`}
                  onClick={() => {
                    setParteActiva("IA");
                    setConjuntoActivoId(conjunto.id);
                    setBssidsSeleccionados(new Set());
                    setMapaActivo(null);
                  }}
                >
                  <span className={styles.etiquetaIA}>
                    <Sparkles size={14} aria-hidden="true" />
                    Subconjunto IA
                  </span>
                  <span>
                    <h3>{conjunto.nombre}</h3>
                    <small>{conjunto.resumen_ia ?? conjunto.proposito}</small>
                    {conjunto.descripcion && <small>{conjunto.descripcion}</small>}
                  </span>
                  <span className={styles.apsConjunto}>
                    {conjunto.items.map((ap) => (
                      <i key={ap.bssid}>
                        {ap.ssid || "SSID oculto"} · {ap.bssid}
                      </i>
                    ))}
                  </span>
                </button>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

function Indicador({
  icono,
  etiqueta,
  valor,
}: {
  icono: ReactNode;
  etiqueta: string;
  valor: number;
}) {
  return (
    <div className={styles.indicador}>
      {icono}
      <span>{etiqueta}</span>
      <strong>{valor}</strong>
    </div>
  );
}

function BloqueConjuntos({
  titulo,
  descripcion,
  icono,
  conjuntos,
  conjuntoActivoId,
  onSeleccionar,
}: {
  titulo: string;
  descripcion: string;
  icono: ReactNode;
  conjuntos: PortalClienteOut["conjuntos"];
  conjuntoActivoId: number | null;
  onSeleccionar: (id: number) => void;
}) {
  return (
    <section className={styles.bloque}>
      <div className={styles.panelHeader}>
        {icono}
        <div>
          <h2>{titulo}</h2>
          <p>{descripcion}</p>
        </div>
      </div>
      {conjuntos.length === 0 ? (
        <div className={styles.vacio}>No hay conjuntos publicados en esta parte.</div>
      ) : (
        <div className={styles.conjuntos}>
          {conjuntos.map((conjunto) => (
            <button
              key={conjunto.id}
              type="button"
              className={`${styles.conjunto} ${
                conjunto.id === conjuntoActivoId ? styles.conjuntoActivo : ""
              }`}
              onClick={() => onSeleccionar(conjunto.id)}
            >
              <span>
                <h3>{conjunto.nombre}</h3>
                <small>{conjunto.proposito}</small>
                {conjunto.descripcion && <small>{conjunto.descripcion}</small>}
              </span>
              <span className={styles.apsConjunto}>
                {conjunto.items.map((ap) => (
                  <i key={ap.bssid}>
                    {ap.ssid || "SSID oculto"} · {ap.bssid}
                  </i>
                ))}
              </span>
            </button>
          ))}
        </div>
      )}
    </section>
  );
}

function HeatmapCanvas({
  mapa,
  plano,
}: {
  mapa: MapaCalorPortalOut;
  plano: PlanoOut | null;
}) {
  const dragRef = useRef<{ x: number; y: number } | null>(null);
  const [zoom, setZoom] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [verHeatmap, setVerHeatmap] = useState(true);
  const [verAps, setVerAps] = useState(true);
  const [verPuntos, setVerPuntos] = useState(true);
  const [hint, setHint] = useState<{
    x: number;
    y: number;
    titulo: string;
    lineas: string[];
  } | null>(null);
  const anchoReferencia = plano?.ancho_px ?? mapa.resolucion;
  const altoReferencia = plano?.alto_px ?? mapa.resolucion;

  const actualizarTooltip = (event: PointerEvent<HTMLDivElement>) => {
    const rect = event.currentTarget.getBoundingClientRect();
    const filas = mapa.matriz.length;
    const columnas = mapa.matriz[0]?.length ?? 0;
    if (filas === 0 || columnas === 0) return;

    const xLocal = event.clientX - rect.left;
    const yLocal = event.clientY - rect.top;
    const col = Math.floor(((xLocal - offset.x) / zoom / rect.width) * columnas);
    const row = Math.floor(((yLocal - offset.y) / zoom / rect.height) * filas);
    const valor = mapa.matriz[row]?.[col];
    setHint(
      typeof valor === "number"
        ? {
            x: xLocal,
            y: yLocal,
            titulo: "RSSI estimado",
            lineas: [`${valor.toFixed(1)} dBm`, nivelCobertura(valor)],
          }
        : null,
    );
  };

  const mostrarHint = (
    event: PointerEvent<Element>,
    titulo: string,
    lineas: string[],
  ) => {
    const rect = event.currentTarget
      .closest(`.${styles.heatmapImagen}`)
      ?.getBoundingClientRect();
    if (!rect) return;
    setHint({
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
      titulo,
      lineas,
    });
  };

  return (
    <div className={styles.canvasWrap}>
      <div className={styles.capasMapa} aria-label="Capas del heatmap">
        <button
          type="button"
          className={verHeatmap ? styles.capaActiva : ""}
          onClick={() => setVerHeatmap((prev) => !prev)}
          title={verHeatmap ? "Ocultar heatmap" : "Mostrar heatmap"}
        >
          {verHeatmap ? <Eye size={15} aria-hidden="true" /> : <EyeOff size={15} aria-hidden="true" />}
          Heatmap
        </button>
        <button
          type="button"
          className={verAps ? styles.capaActiva : ""}
          onClick={() => setVerAps((prev) => !prev)}
          title={verAps ? "Ocultar APs" : "Mostrar APs"}
        >
          {verAps ? <Eye size={15} aria-hidden="true" /> : <EyeOff size={15} aria-hidden="true" />}
          APs
        </button>
        <button
          type="button"
          className={verPuntos ? styles.capaActiva : ""}
          onClick={() => setVerPuntos((prev) => !prev)}
          title={verPuntos ? "Ocultar puntos" : "Mostrar puntos"}
        >
          {verPuntos ? <Eye size={15} aria-hidden="true" /> : <EyeOff size={15} aria-hidden="true" />}
          Puntos
        </button>
      </div>
      <div className={styles.toolbarMapa}>
        <button type="button" onClick={() => setZoom((prev) => Math.max(prev - 0.2, 0.6))}>
          <Minus size={16} aria-hidden="true" />
        </button>
        <span>{Math.round(zoom * 100)}%</span>
        <button type="button" onClick={() => setZoom((prev) => Math.min(prev + 0.2, 2.6))}>
          <Plus size={16} aria-hidden="true" />
        </button>
      </div>
      <div
        className={styles.heatmapImagen}
        style={{
          aspectRatio: plano
            ? `${plano.ancho_px} / ${plano.alto_px}`
            : `${mapa.resolucion} / ${mapa.resolucion}`,
        }}
        onPointerDown={(event) => {
          dragRef.current = { x: event.clientX, y: event.clientY };
          event.currentTarget.setPointerCapture(event.pointerId);
        }}
        onPointerLeave={() => setHint(null)}
        onPointerMove={(event) => {
          if (dragRef.current) {
            setOffset((prev) => ({
              x: prev.x + event.clientX - dragRef.current!.x,
              y: prev.y + event.clientY - dragRef.current!.y,
            }));
            dragRef.current = { x: event.clientX, y: event.clientY };
          }
          if (!dragRef.current) actualizarTooltip(event);
        }}
        onPointerUp={(event) => {
          dragRef.current = null;
          event.currentTarget.releasePointerCapture(event.pointerId);
        }}
        onPointerCancel={() => {
          dragRef.current = null;
        }}
      >
        {plano && (
          <img
            className={styles.planoHeatmap}
            src={resolverUrlApi(plano.url_firmada)}
            alt={`Plano ${plano.nombre}`}
            draggable={false}
            style={{
              transform: `translate(${offset.x}px, ${offset.y}px) scale(${zoom})`,
            }}
          />
        )}
        {verHeatmap && (
          <img
            className={styles.capaHeatmap}
            src={resolverUrlApi(mapa.url_imagen)}
            alt="Heatmap generado"
            draggable={false}
            style={{
              transform: `translate(${offset.x}px, ${offset.y}px) scale(${zoom})`,
            }}
          />
        )}
        <svg
          className={styles.puntosLectura}
          viewBox={`0 0 ${anchoReferencia} ${altoReferencia}`}
          preserveAspectRatio="none"
          style={{
            transform: `translate(${offset.x}px, ${offset.y}px) scale(${zoom})`,
          }}
        >
          {verPuntos &&
            mapa.puntos_lectura.map((punto) => (
              <circle
                key={punto.punto_id}
                className={styles.puntoLectura}
                cx={limitar(punto.pos_x, 0, anchoReferencia)}
                cy={limitar(punto.pos_y, 0, altoReferencia)}
                r={Math.max(anchoReferencia, altoReferencia) * 0.006}
                fill={colorRssi(punto.rssi)}
                onPointerDown={(event) => event.stopPropagation()}
                onPointerMove={(event) => {
                  event.stopPropagation();
                  mostrarHint(event, `Punto #${punto.punto_id}`, [
                    `${punto.rssi.toFixed(1)} dBm`,
                    nivelCobertura(punto.rssi),
                    `Posición ${punto.pos_x.toFixed(0)}, ${punto.pos_y.toFixed(0)} px`,
                  ]);
                }}
                onPointerLeave={() => setHint(null)}
              />
            ))}
        </svg>
        {verAps && (
          <div
            className={styles.capaApsMapa}
            style={{
              transform: `translate(${offset.x}px, ${offset.y}px) scale(${zoom})`,
            }}
            aria-label="Ubicación de APs"
          >
            {mapa.aps_interes.map((ap, indice) => (
              <button
                key={ap.bssid}
                type="button"
                className={styles.marcadorApMapa}
                style={{
                  left: `${(limitar(ap.pos_x, 0, anchoReferencia) / anchoReferencia) * 100}%`,
                  top: `${(limitar(ap.pos_y, 0, altoReferencia) / altoReferencia) * 100}%`,
                }}
                title={`${indice + 1}. ${ap.ssid || "SSID oculto"} · ${ap.bssid}`}
                aria-label={`AP ${indice + 1}: ${ap.ssid || "SSID oculto"}`}
                onPointerDown={(event) => event.stopPropagation()}
                onPointerMove={(event) => {
                  event.stopPropagation();
                  mostrarHint(event, ap.ssid || "SSID oculto", [
                    ap.bssid,
                    `${ap.rssi_promedio.toFixed(1)} dBm promedio`,
                    nivelCobertura(ap.rssi_promedio),
                    ap.canal ? `Canal ${ap.canal}` : "Canal s/d",
                    ap.frecuencia_mhz ? `${ap.frecuencia_mhz} MHz` : "Frecuencia s/d",
                    `${ap.cantidad_puntos} punto(s) asociados`,
                  ]);
                }}
                onPointerLeave={() => setHint(null)}
              >
                {indice + 1}
              </button>
            ))}
          </div>
        )}
      </div>
      {hint && (
        <div className={styles.tooltip} style={{ left: hint.x + 12, top: hint.y + 12 }}>
          <strong>{hint.titulo}</strong>
          {hint.lineas.map((linea) => (
            <span key={linea}>{linea}</span>
          ))}
        </div>
      )}
      <div className={styles.leyenda}>
        {mapa.escala.map((item) => (
          <span key={`${item.desde}-${item.hasta}`}>
            <i style={{ background: item.color }} />
            {item.etiqueta}
          </span>
        ))}
      </div>
    </div>
  );
}

function _toggleBssid(
  previo: Set<string>,
  bssid: string,
  modo: ModoGeneracion,
): Set<string> {
  if (modo === "INDIVIDUAL") return new Set([bssid]);
  if (modo === "CONJUNTO_COMPLETO") return new Set(previo);
  const siguiente = new Set(previo);
  if (siguiente.has(bssid)) {
    siguiente.delete(bssid);
  } else {
    siguiente.add(bssid);
  }
  return siguiente;
}

function _labelModo(modo: string): string {
  const labels: Record<string, string> = {
    INDIVIDUAL: "Un AP",
    SUBCONJUNTO: "Subconjunto",
    CONJUNTO_COMPLETO: "Todos",
  };
  return labels[modo] ?? modo;
}


function nivelCobertura(rssi: number): string {
  if (rssi >= -60) return "Excelente";
  if (rssi >= -67) return "Muy buena";
  if (rssi >= -70) return "Objetivo CWNA-107";
  if (rssi >= -80) return "Aceptable";
  if (rssi >= -90) return "Débil";
  return "Zona muerta CWNA-107";
}

function colorRssi(rssi: number): string {
  if (rssi >= -60) return "#0B7A3B";
  if (rssi >= -67) return "#57B65A";
  if (rssi >= -70) return "#A7C957";
  if (rssi >= -75) return "#F4D35E";
  if (rssi >= -80) return "#F08A24";
  if (rssi >= -90) return "#D95D39";
  return "#D7263D";
}

function limitar(valor: number, minimo: number, maximo: number): number {
  return Math.min(maximo, Math.max(minimo, valor));
}
