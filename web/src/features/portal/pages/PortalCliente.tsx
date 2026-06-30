import {
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type Dispatch,
  type PointerEvent,
  type ReactNode,
  type SetStateAction,
} from "react";
import {
  BarChart3,
  BrainCircuit,
  Building2,
  ChevronLeft,
  ChevronRight,
  Eye,
  EyeOff,
  FileImage,
  MapPinned,
  Minus,
  Plus,
  RadioTower,
  TrendingUp,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { resolverUrlApi } from "@/shared/api/urlApi";
import { obtenerPortalCliente } from "../api/shareClient";
import type {
  MapaCalorPortalOut,
  PlanoOut,
} from "@/features/admin/types";
import styles from "./PortalCliente.module.css";

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
  const [mapaActivoIndice, setMapaActivoIndice] = useState(0);
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

  const mapasConjuntoActivo = useMemo(
    () =>
      conjuntoActivo
        ? (data?.heatmaps ?? [])
            .filter((mapa) => mapa.conjunto_ap_id === conjuntoActivo.id)
            .sort((a, b) => (a.created_at < b.created_at ? 1 : -1))
        : [],
    [conjuntoActivo, data?.heatmaps],
  );
  const gruposParte = useMemo(
    () =>
      _agruparConjuntosPorPlano(
        data?.planos ?? [],
        conjuntosParte,
        data?.heatmaps ?? [],
      ),
    [conjuntosParte, data?.heatmaps, data?.planos],
  );
  const indiceMapaSeguro =
    mapasConjuntoActivo.length === 0
      ? 0
      : Math.min(mapaActivoIndice, mapasConjuntoActivo.length - 1);
  const mapaMostrado = mapasConjuntoActivo[indiceMapaSeguro] ?? null;
  const planoActivo = mapaMostrado
    ? data?.planos.find((plano) => plano.id === mapaMostrado.plano_id) ?? null
    : conjuntoActivo
      ? data?.planos.find((plano) => plano.id === conjuntoActivo.plano_id) ?? null
      : null;

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
          etiqueta="Datos de campo"
          valor={conjuntosRelevados.length}
        />
        <Indicador
          icono={<BrainCircuit size={18} />}
          etiqueta="Propuestas IA"
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
                  ? `${planoActivo?.nombre ?? "Plano"} · ${conjuntoActivo.nombre} · ${mapasConjuntoActivo.length} mapa(s) compartido(s)`
                  : "Seleccione contenido publicado para explorar el mapa."}
              </p>
            </div>
          </div>

          {conjuntoActivo && mapaMostrado ? (
            <CarruselMapasPortal
              conjuntoNombre={conjuntoActivo.nombre}
              indiceActivo={indiceMapaSeguro}
              mapas={mapasConjuntoActivo}
              onCambiarIndice={setMapaActivoIndice}
              planos={data.planos}
            />
          ) : (
            <div className={styles.vacio}>
              {conjuntoActivo
                ? "No hay mapas de calor compartidos para este contenido."
                : "Seleccione contenido publicado para revisar sus mapas compartidos."}
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
                  setMapaActivoIndice(0);
                }}
              >
                <BarChart3 size={16} aria-hidden="true" />
                <span>
                  <strong>Datos relevados</strong>
                  <small>{conjuntosRelevados.length} registro(s) de campo</small>
                </span>
              </button>
              <button
                type="button"
                className={parteVisible === "IA" ? styles.parteActiva : ""}
                onClick={() => {
                  setParteActiva("IA");
                  setConjuntoActivoId(conjuntosIA[0]?.id ?? null);
                  setMapaActivoIndice(0);
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
            <h2>{parteVisible === "IA" ? "Propuestas IA" : "Contenido publicado"}</h2>
            {conjuntosParte.length === 0 ? (
              <p>
                {parteVisible === "IA"
                  ? "No hay propuestas IA publicadas para este enlace."
                  : "No hay datos relevados publicados para este enlace."}
              </p>
            ) : (
              <div className={styles.formGenerador}>
                <div className={styles.gruposPlanoPortal}>
                  {gruposParte.map((grupo) => (
                    <section key={grupo.planoId}>
                      <header>
                        <strong>{grupo.nombre}</strong>
                        <small>
                          {grupo.conjuntos.length} contenido(s) · {grupo.mapas.length} mapa(s)
                        </small>
                      </header>
                      <div>
                        {grupo.conjuntos.map((conjunto) => (
                          <button
                            key={conjunto.id}
                            type="button"
                            className={
                              conjuntoActivo?.id === conjunto.id
                                ? styles.contenidoActivo
                                : ""
                            }
                            onClick={() => {
                              setConjuntoActivoId(conjunto.id);
                              setMapaActivoIndice(0);
                            }}
                          >
                            <span>{conjunto.nombre}</span>
                            <small>
                              {conjunto.cantidad_aps} APs ·{" "}
                              {grupo.mapasPorConjunto.get(conjunto.id)?.length ?? 0} mapa(s)
                            </small>
                          </button>
                        ))}
                      </div>
                    </section>
                  ))}
                </div>

                <dl>
                  <div>
                    <dt>Mapas compartidos</dt>
                    <dd>{mapasConjuntoActivo.length}</dd>
                  </div>
                  <div>
                    <dt>APs del contenido</dt>
                    <dd>{conjuntoActivo?.cantidad_aps ?? 0}</dd>
                  </div>
                </dl>

              </div>
            )}
          </section>
        </aside>
      </section>
    </main>
  );
}

function CarruselMapasPortal({
  conjuntoNombre,
  indiceActivo,
  mapas,
  onCambiarIndice,
  planos,
}: {
  conjuntoNombre: string;
  indiceActivo: number;
  mapas: MapaCalorPortalOut[];
  onCambiarIndice: (indice: number) => void;
  planos: PlanoOut[];
}) {
  const [verHeatmap, setVerHeatmap] = useState(true);
  const [verAps, setVerAps] = useState(true);
  const [verPuntos, setVerPuntos] = useState(true);
  const [exportando, setExportando] = useState<string | null>(null);
  const mapa = mapas[indiceActivo];
  if (!mapa) return null;
  const plano = planos.find((item) => item.id === mapa.plano_id) ?? null;
  const irAnterior = () => {
    if (mapas.length <= 1) return;
    onCambiarIndice(indiceActivo === 0 ? mapas.length - 1 : indiceActivo - 1);
  };
  const irSiguiente = () => {
    if (mapas.length <= 1) return;
    onCambiarIndice((indiceActivo + 1) % mapas.length);
  };
  const capasExportacion = { heatmap: verHeatmap, aps: verAps, puntos: verPuntos };
  const exportarMapaActual = async () => {
    const clave = "mapa-png";
    try {
      setExportando(clave);
      const canvas = await componerMapaCanvas({
        mapa,
        plano,
        capas: capasExportacion,
      });
      const nombre = nombreExportacionMapa({ conjuntoNombre, mapa, plano });
      await descargarCanvasPng(canvas, `${nombre}.png`);
    } catch (error) {
      console.error(error);
      window.alert("No se pudo exportar el mapa de calor.");
    } finally {
      setExportando(null);
    }
  };
  const exportarConjunto = async () => {
    const clave = "conjunto-png";
    try {
      setExportando(clave);
      const canvases = await Promise.all(
        mapas.map((mapaItem) =>
          componerMapaCanvas({
            mapa: mapaItem,
            plano: planos.find((item) => item.id === mapaItem.plano_id) ?? null,
            capas: capasExportacion,
          }),
        ),
      );
      const nombreBase = nombreArchivo(`contenido-${conjuntoNombre}`);
      await Promise.all(
        canvases.map((canvas, indice) => {
          const mapaItem = mapas[indice];
          const planoItem =
            planos.find((item) => item.id === mapaItem.plano_id) ?? null;
          return descargarCanvasPng(
            canvas,
            `${nombreBase}-${nombreExportacionMapa({
              conjuntoNombre,
              mapa: mapaItem,
              plano: planoItem,
            })}.png`,
          );
        }),
      );
    } catch (error) {
      console.error(error);
      window.alert("No se pudo exportar el contenido.");
    } finally {
      setExportando(null);
    }
  };

  return (
    <div className={styles.carruselHeatmaps}>
      <div className={styles.controlesCarrusel}>
        <button
          type="button"
          onClick={irAnterior}
          disabled={mapas.length <= 1}
          aria-label="Ver mapa anterior"
        >
          <ChevronLeft size={18} aria-hidden="true" />
        </button>
        <span>{indiceActivo + 1} / {mapas.length}</span>
        <button
          type="button"
          onClick={irSiguiente}
          disabled={mapas.length <= 1}
          aria-label="Ver mapa siguiente"
        >
          <ChevronRight size={18} aria-hidden="true" />
        </button>
      </div>

      <article className={styles.heatmapCard}>
        <header className={styles.heatmapCardHeader}>
          <div>
            <strong>{_labelModo(mapa.modo_generacion)}</strong>
            <span>{_formatearFechaMapa(mapa.created_at)}</span>
          </div>
          <div className={styles.exportarMapa} aria-label="Exportar vista">
            <button
              type="button"
              disabled={exportando !== null}
              onClick={exportarMapaActual}
              title="Descargar mapa visible como imagen"
            >
              <FileImage size={15} aria-hidden="true" />
              Mapa
            </button>
            <button
              type="button"
              disabled={exportando !== null || mapas.length === 0}
              onClick={exportarConjunto}
              title="Descargar contenido visible como imagen"
            >
              <FileImage size={15} aria-hidden="true" />
              Contenido
            </button>
          </div>
        </header>
        <HeatmapCanvas
          mapa={mapa}
          plano={plano}
          setVerAps={setVerAps}
          setVerHeatmap={setVerHeatmap}
          setVerPuntos={setVerPuntos}
          verAps={verAps}
          verHeatmap={verHeatmap}
          verPuntos={verPuntos}
        />
        <div className={styles.metricasMapa}>
          <span>{mapa.resolucion}px</span>
          <span>{mapa.cantidad_puntos} lectura(s)</span>
        </div>
      </article>

      {mapas.length > 1 && (
        <div className={styles.indicadoresCarrusel} aria-label="Seleccionar mapa">
          {mapas.map((mapaItem, indice) => (
            <button
              key={mapaItem.id}
              type="button"
              className={indice === indiceActivo ? styles.indicadorActivo : ""}
              onClick={() => onCambiarIndice(indice)}
              aria-label={`Ver mapa ${indice + 1}`}
            />
          ))}
        </div>
      )}
    </div>
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

function HeatmapCanvas({
  mapa,
  plano,
  setVerAps,
  setVerHeatmap,
  setVerPuntos,
  verAps,
  verHeatmap,
  verPuntos,
}: {
  mapa: MapaCalorPortalOut;
  plano: PlanoOut | null;
  setVerAps: Dispatch<SetStateAction<boolean>>;
  setVerHeatmap: Dispatch<SetStateAction<boolean>>;
  setVerPuntos: Dispatch<SetStateAction<boolean>>;
  verAps: boolean;
  verHeatmap: boolean;
  verPuntos: boolean;
}) {
  const dragRef = useRef<{ x: number; y: number } | null>(null);
  const [zoom, setZoom] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [hint, setHint] = useState<{
    x: number;
    y: number;
    titulo: string;
    lineas: string[];
  } | null>(null);
  const anchoReferencia = plano?.ancho_px ?? mapa.resolucion;
  const altoReferencia = plano?.alto_px ?? mapa.resolucion;
  const proporcionMapa = anchoReferencia / altoReferencia;
  const estiloVisor = {
    aspectRatio: `${anchoReferencia} / ${altoReferencia}`,
    width: `min(100%, calc(64vh * ${proporcionMapa}))`,
  } satisfies CSSProperties;

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
      <div className={styles.barraMapa}>
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
      </div>
      <div
        className={styles.heatmapImagen}
        style={estiloVisor}
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
                  mostrarHint(
                    event,
                    "Punto de lectura de datos",
                    lineasHintPunto(punto, mapa),
                  );
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
                aria-label={`AP ${indice + 1}: ${ap.ssid || "SSID oculto"}`}
                onPointerDown={(event) => event.stopPropagation()}
                onPointerMove={(event) => {
                  event.stopPropagation();
                  mostrarHint(event, `AP ${indice + 1} · ${ap.ssid || "SSID oculto"}`, [
                    `BSSID: ${ap.bssid}`,
                    `Señal promedio: ${ap.rssi_promedio.toFixed(1)} dBm · ${nivelCobertura(ap.rssi_promedio)}`,
                    `Lecturas asociadas: ${ap.cantidad_puntos}`,
                    _canalFrecuencia(ap),
                  ]);
                }}
                onPointerLeave={() => setHint(null)}
              >
                {indice + 1}
              </button>
            ))}
          </div>
        )}
        {hint && (
          <div className={styles.tooltip} style={{ left: hint.x + 12, top: hint.y + 12 }}>
            <strong>{hint.titulo}</strong>
            {hint.lineas.map((linea) => (
              <span key={linea}>{linea}</span>
            ))}
          </div>
        )}
      </div>
      <div className={styles.mapaInferior}>
        <div className={styles.leyenda}>
          {mapa.escala.map((item) => (
            <span key={`${item.desde}-${item.hasta}`}>
              <i style={{ background: item.color }} />
              {item.etiqueta}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

function _labelModo(modo: string): string {
  const labels: Record<string, string> = {
    INDIVIDUAL: "Un AP",
    SUBCONJUNTO: "Selección",
    CONJUNTO_COMPLETO: "Todos",
  };
  return labels[modo] ?? modo;
}

type CapasExportacion = {
  heatmap: boolean;
  aps: boolean;
  puntos: boolean;
};

async function componerMapaCanvas({
  mapa,
  plano,
  capas,
}: {
  mapa: MapaCalorPortalOut;
  plano: PlanoOut | null;
  capas: CapasExportacion;
}): Promise<HTMLCanvasElement> {
  const ancho = plano?.ancho_px ?? mapa.resolucion;
  const alto = plano?.alto_px ?? mapa.resolucion;
  const canvas = document.createElement("canvas");
  canvas.width = ancho;
  canvas.height = alto;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("No se pudo crear el canvas de exportación.");

  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, ancho, alto);
  if (plano) {
    const imgPlano = await cargarImagen(resolverUrlApi(plano.url_firmada));
    ctx.drawImage(imgPlano, 0, 0, ancho, alto);
  }
  if (capas.heatmap) {
    const imgHeatmap = await cargarImagen(resolverUrlApi(mapa.url_imagen));
    ctx.drawImage(imgHeatmap, 0, 0, ancho, alto);
  }
  if (capas.puntos) {
    dibujarPuntosLectura(ctx, mapa, ancho, alto);
  }
  if (capas.aps) {
    dibujarAps(ctx, mapa, ancho, alto);
  }
  return canvas;
}

function dibujarPuntosLectura(
  ctx: CanvasRenderingContext2D,
  mapa: MapaCalorPortalOut,
  ancho: number,
  alto: number,
) {
  const radio = Math.max(4, Math.min(9, Math.max(ancho, alto) * 0.006));
  for (const punto of mapa.puntos_lectura) {
    ctx.beginPath();
    ctx.arc(
      limitar(punto.pos_x, 0, ancho),
      limitar(punto.pos_y, 0, alto),
      radio,
      0,
      Math.PI * 2,
    );
    ctx.fillStyle = colorRssi(punto.rssi);
    ctx.globalAlpha = 0.78;
    ctx.fill();
    ctx.globalAlpha = 1;
    ctx.lineWidth = 2;
    ctx.strokeStyle = "#ffffff";
    ctx.stroke();
  }
}

function dibujarAps(
  ctx: CanvasRenderingContext2D,
  mapa: MapaCalorPortalOut,
  ancho: number,
  alto: number,
) {
  const radio = Math.max(14, Math.min(24, Math.max(ancho, alto) * 0.018));
  mapa.aps_interes.forEach((ap, indice) => {
    const x = limitar(ap.pos_x, 0, ancho);
    const y = limitar(ap.pos_y, 0, alto);
    ctx.beginPath();
    ctx.arc(x, y, radio + 4, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(15, 23, 42, 0.86)";
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x, y, radio, 0, Math.PI * 2);
    ctx.fillStyle = "#176b9f";
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#ffffff";
    ctx.stroke();
    ctx.fillStyle = "#ffffff";
    ctx.font = `700 ${Math.max(12, radio)}px Arial`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(String(indice + 1), x, y + 0.5);
  });
}

function cargarImagen(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`No se pudo cargar la imagen ${src}`));
    img.src = src;
  });
}

function descargarCanvasPng(canvas: HTMLCanvasElement, archivo: string): Promise<void> {
  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (!blob) {
        reject(new Error("No se pudo generar la imagen."));
        return;
      }
      descargarBlob(blob, archivo);
      resolve();
    }, "image/png");
  });
}

function descargarBlob(blob: Blob, archivo: string) {
  const url = URL.createObjectURL(blob);
  const enlace = document.createElement("a");
  enlace.href = url;
  enlace.download = archivo;
  enlace.click();
  URL.revokeObjectURL(url);
}

function nombreArchivo(valor: string): string {
  return valor
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function nombreExportacionMapa({
  conjuntoNombre,
  mapa,
  plano,
}: {
  conjuntoNombre: string;
  mapa: MapaCalorPortalOut;
  plano: PlanoOut | null;
}): string {
  const planoNombre = plano?.nombre.replace(/\.[^.]+$/, "") ?? `plano-${mapa.plano_id}`;
  const aps = mapa.aps_interes.length > 0
    ? mapa.aps_interes
        .map((ap, indice) => `ap-${indice + 1}-${ap.bssid.slice(-5)}`)
        .join("-")
    : (mapa.bssids_generacion.length > 0 ? mapa.bssids_generacion : [mapa.bssid])
        .map((bssid, indice) => `ap-${indice + 1}-${bssid.slice(-5)}`)
        .join("-");
  return nombreArchivo(`${planoNombre}-${conjuntoNombre}-${aps}`);
}

function _formatearFechaMapa(valor: string): string {
  return new Intl.DateTimeFormat("es-BO", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(valor));
}


function nivelCobertura(rssi: number): string {
  if (rssi >= -70) return "Óptimo";
  if (rssi >= -80) return "Aceptable";
  if (rssi >= -85) return "Pobre";
  if (rssi >= -90) return "Muy pobre";
  return "Zona muerta CWNA-107";
}

function colorRssi(rssi: number): string {
  if (rssi >= -70) return "#A7E84A";
  if (rssi >= -80) return "#F1E64A";
  if (rssi >= -85) return "#C7B84B";
  if (rssi >= -90) return "#7E8173";
  return "#1C1C1C";
}

function _canalFrecuencia(ap: MapaCalorPortalOut["aps_interes"][number]): string {
  const canal = ap.canal ? `Canal ${ap.canal}` : "Canal s/d";
  const frecuencia = ap.frecuencia_mhz ? `${ap.frecuencia_mhz} MHz` : "Frecuencia s/d";
  return `${canal} · ${frecuencia}`;
}

function _agruparConjuntosPorPlano(
  planos: PlanoOut[],
  conjuntos: Array<{ id: number; plano_id: number; nombre: string; cantidad_aps: number }>,
  mapas: MapaCalorPortalOut[],
) {
  const planosPorId = new Map(planos.map((plano) => [plano.id, plano]));
  const mapasPorPlano = new Map<number, MapaCalorPortalOut[]>();
  const mapasPorConjunto = new Map<number, MapaCalorPortalOut[]>();
  for (const mapa of mapas) {
    mapasPorPlano.set(mapa.plano_id, [...(mapasPorPlano.get(mapa.plano_id) ?? []), mapa]);
    if (typeof mapa.conjunto_ap_id === "number") {
      mapasPorConjunto.set(
        mapa.conjunto_ap_id,
        [...(mapasPorConjunto.get(mapa.conjunto_ap_id) ?? []), mapa],
      );
    }
  }
  const grupos = new Map<
    number,
    {
      planoId: number;
      nombre: string;
      conjuntos: typeof conjuntos;
      mapas: MapaCalorPortalOut[];
      mapasPorConjunto: Map<number, MapaCalorPortalOut[]>;
    }
  >();
  for (const conjunto of conjuntos) {
    const grupo = grupos.get(conjunto.plano_id) ?? {
      planoId: conjunto.plano_id,
      nombre: planosPorId.get(conjunto.plano_id)?.nombre ?? `Plano ${conjunto.plano_id}`,
      conjuntos: [],
      mapas: mapasPorPlano.get(conjunto.plano_id) ?? [],
      mapasPorConjunto,
    };
    grupo.conjuntos.push(conjunto);
    grupos.set(conjunto.plano_id, grupo);
  }
  return Array.from(grupos.values()).sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
}

function lineasHintPunto(
  punto: MapaCalorPortalOut["puntos_lectura"][number],
  mapa: MapaCalorPortalOut,
): string[] {
  const detalle = punto.detalle_aps ?? [];
  if (detalle.length === 0) {
    return [
      `Total lecturas: ${punto.total_lecturas ?? 0}`,
      `RSSI ref.: ${punto.rssi.toFixed(1)} dBm`,
    ];
  }
  const apsPorBssid = new Map(
    mapa.aps_interes.map((ap, indice) => [
      ap.bssid.toLowerCase(),
      {
        etiqueta: `AP ${indice + 1}`,
        bssidCorto: ap.bssid.slice(-5).toUpperCase(),
      },
    ]),
  );
  return [
    `Total lecturas: ${punto.total_lecturas ?? 0}`,
    ...detalle.map((ap, indice) => {
      const meta = apsPorBssid.get(ap.bssid.toLowerCase());
      const etiqueta = meta
        ? `${meta.etiqueta} (${meta.bssidCorto})`
        : `AP ${indice + 1} (${ap.bssid.slice(-5).toUpperCase()})`;
      const rssi =
        typeof ap.rssi_promedio === "number"
          ? `${ap.rssi_promedio.toFixed(1)} dBm`
          : "sin RSSI";
      return `${etiqueta}: ${porcentajeLecturas(ap.total_lecturas, punto.total_lecturas)} leídas · ${porcentajeLecturas(ap.lecturas_perdidas, punto.total_lecturas)} perdidas · ${rssi}`;
    }),
  ];
}

function porcentajeLecturas(cantidad: number, total?: number): string {
  if (!total || total <= 0) return "0%";
  return `${Math.round((cantidad / total) * 100)}%`;
}

function limitar(valor: number, minimo: number, maximo: number): number {
  return Math.min(maximo, Math.max(minimo, valor));
}
