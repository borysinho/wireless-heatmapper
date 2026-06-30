import { useEffect, useRef, useState, type PointerEvent } from "react";
import { Layers3, MapPin, RadioTower, RotateCcw, ZoomIn, ZoomOut } from "lucide-react";
import { resolverUrlApi } from "@/shared/api/urlApi";
import type { MapaCalorOut, PlanoOut } from "../types";
import styles from "./MapaCalorInteractivo.module.css";

interface Props {
  mapa: MapaCalorOut;
  plano: PlanoOut;
  titulo: string;
  compacto?: boolean;
  apHints?: APHint[];
}

interface Posicion {
  x: number;
  y: number;
}

interface APHint {
  titulo: string;
  resumen: string;
  detalles: string[];
}

interface APHintActivo extends APHint {
  x: number;
  y: number;
}

export function MapaCalorInteractivo({
  mapa,
  plano,
  titulo,
  compacto = false,
  apHints,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const visorRef = useRef<HTMLDivElement | null>(null);
  const arrastreRef = useRef<Posicion | null>(null);
  const [zoom, setZoom] = useState(1);
  const [desplazamiento, setDesplazamiento] = useState<Posicion>({ x: 0, y: 0 });
  const [opacidad, setOpacidad] = useState(60);
  const [verHeatmap, setVerHeatmap] = useState(true);
  const [verPuntos, setVerPuntos] = useState(true);
  const [verAps, setVerAps] = useState(true);
  const [arrastrando, setArrastrando] = useState(false);
  const [detalle, setDetalle] = useState<string | null>(null);
  const [hintAp, setHintAp] = useState<APHintActivo | null>(null);
  const [rssiCursor, setRssiCursor] = useState<{ x: number; y: number; valor: number } | null>(null);
  const [tamanoLienzo, setTamanoLienzo] = useState<Posicion>({
    x: plano.ancho_px,
    y: plano.alto_px,
  });

  useEffect(() => {
    const visor = visorRef.current;
    if (!visor) return;

    const ajustarAlVisor = () => {
      const anchoDisponible = visor.clientWidth;
      const altoDisponible = visor.clientHeight;
      if (anchoDisponible <= 0 || altoDisponible <= 0) return;

      const escalaAjuste = Math.min(
        anchoDisponible / plano.ancho_px,
        altoDisponible / plano.alto_px,
      );
      setTamanoLienzo({
        x: plano.ancho_px * escalaAjuste,
        y: plano.alto_px * escalaAjuste,
      });
    };

    ajustarAlVisor();
    const observador = new ResizeObserver(ajustarAlVisor);
    observador.observe(visor);
    return () => observador.disconnect();
  }, [plano.alto_px, plano.ancho_px]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const contexto = canvas?.getContext("2d");
    const filas = mapa.matriz.length;
    const columnas = mapa.matriz[0]?.length ?? 0;
    if (!canvas || !contexto || filas === 0 || columnas === 0) return;

    canvas.width = columnas;
    canvas.height = filas;
    contexto.clearRect(0, 0, columnas, filas);
    mapa.matriz.forEach((fila, y) => {
      fila.forEach((rssi, x) => {
        contexto.fillStyle = colorRssi(rssi);
        contexto.fillRect(x, y, 1, 1);
      });
    });
  }, [mapa.matriz, verHeatmap]);

  const reiniciarVista = () => {
    setZoom(1);
    setDesplazamiento({ x: 0, y: 0 });
  };

  const iniciarArrastre = (event: PointerEvent<HTMLDivElement>) => {
    if (event.button !== 0) return;
    arrastreRef.current = { x: event.clientX, y: event.clientY };
    setArrastrando(true);
    setRssiCursor(null);
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const moverArrastre = (event: PointerEvent<HTMLDivElement>) => {
    const anterior = arrastreRef.current;
    if (!anterior) return;
    setDesplazamiento((actual) => ({
      x: actual.x + event.clientX - anterior.x,
      y: actual.y + event.clientY - anterior.y,
    }));
    arrastreRef.current = { x: event.clientX, y: event.clientY };
  };

  const inspeccionarRssi = (event: PointerEvent<HTMLDivElement>) => {
    moverArrastre(event);
    if (arrastreRef.current) return;
    const rect = event.currentTarget.getBoundingClientRect();
    const xNormalizada = (event.clientX - rect.left) / rect.width;
    const yNormalizada = (event.clientY - rect.top) / rect.height;
    const columna = Math.floor(xNormalizada * (mapa.matriz[0]?.length ?? 0));
    const fila = Math.floor(yNormalizada * mapa.matriz.length);
    const valor = mapa.matriz[fila]?.[columna];
    setRssiCursor(
      typeof valor === "number"
        ? { x: event.clientX - rect.left, y: event.clientY - rect.top, valor }
        : null,
    );
  };

  const cambiarZoom = (siguiente: number) => setZoom(Math.min(5, Math.max(0.5, siguiente)));

  return (
    <figure className={`${styles.contenedor} ${compacto ? styles.compacto : ""}`}>
      <figcaption className={styles.encabezado}>
        <div>
          <strong>{titulo}</strong>
          <span>{plano.nombre} · {_modoLegible(mapa.modo_generacion)}</span>
        </div>
        <div className={styles.controlesVista} aria-label="Controles del mapa">
          <button type="button" title="Alejar" onClick={() => cambiarZoom(zoom - 0.2)}><ZoomOut size={16} /></button>
          <span>{Math.round(zoom * 100)}%</span>
          <button type="button" title="Acercar" onClick={() => cambiarZoom(zoom + 0.2)}><ZoomIn size={16} /></button>
          <button type="button" title="Restablecer vista" onClick={reiniciarVista}><RotateCcw size={16} /></button>
        </div>
      </figcaption>

      <div className={styles.barraCapas}>
        <label><input type="checkbox" checked={verHeatmap} onChange={(e) => setVerHeatmap(e.target.checked)} /><Layers3 size={14} /> Heatmap</label>
        <label><input type="checkbox" checked={verPuntos} onChange={(e) => setVerPuntos(e.target.checked)} /><MapPin size={14} /> Mediciones</label>
        <label><input type="checkbox" checked={verAps} onChange={(e) => setVerAps(e.target.checked)} /><RadioTower size={14} /> APs</label>
        <label className={styles.opacidad}>Opacidad <input type="range" min="10" max="90" value={opacidad} disabled={!verHeatmap} onChange={(e) => setOpacidad(Number(e.target.value))} /><span>{opacidad}%</span></label>
      </div>

      <div
        ref={visorRef}
        className={`${styles.visor} ${arrastrando ? styles.arrastrando : ""}`}
        onPointerDown={iniciarArrastre}
        onPointerMove={moverArrastre}
        onPointerUp={(event) => { arrastreRef.current = null; setArrastrando(false); event.currentTarget.releasePointerCapture(event.pointerId); }}
        onPointerCancel={() => { arrastreRef.current = null; setArrastrando(false); }}
        onPointerLeave={() => { setRssiCursor(null); setHintAp(null); }}
      >
        <div
          className={styles.lienzo}
          style={{
            width: tamanoLienzo.x,
            height: tamanoLienzo.y,
            transform: `translate(${desplazamiento.x}px, ${desplazamiento.y}px) scale(${zoom})`,
          }}
          onPointerMove={inspeccionarRssi}
        >
          <img className={styles.plano} src={resolverUrlApi(plano.url_firmada)} alt={`Plano ${plano.nombre}`} draggable={false} />
          {verHeatmap && <canvas ref={canvasRef} className={styles.heatmap} style={{ opacity: opacidad / 100 }} />}
          <svg className={styles.marcadores} viewBox={`0 0 ${plano.ancho_px} ${plano.alto_px}`} preserveAspectRatio="none">
            {verPuntos && mapa.puntos_lectura.map((punto) => (
              <circle
                key={punto.punto_id}
                className={styles.punto}
                cx={punto.pos_x}
                cy={punto.pos_y}
                r={Math.max(plano.ancho_px, plano.alto_px) * 0.008}
                fill={colorRssi(punto.rssi)}
                onPointerDown={(event) => event.stopPropagation()}
                onClick={(event) => { event.stopPropagation(); setDetalle(`Medición #${punto.punto_id} · ${punto.rssi.toFixed(1)} dBm · (${punto.pos_x.toFixed(0)}, ${punto.pos_y.toFixed(0)}) px`); }}
              />
            ))}
          </svg>
          {verAps && (
            <div className={styles.capaAps} aria-label="Ubicación de APs">
              {mapa.aps_interes.map((ap, indice) => {
                const hint = apHints?.[indice];
                const detalleAp = hint
                  ? `${hint.titulo} · ${hint.resumen}`
                  : `${ap.ssid || "SSID oculto"} · ${ap.bssid} · ${ap.rssi_promedio.toFixed(1)} dBm · ${ap.canal ? `canal ${ap.canal}` : "canal s/d"} · ${ap.cantidad_puntos} puntos`;

                return (
                  <button
                    key={ap.bssid}
                    type="button"
                    className={styles.marcadorAp}
                    style={{
                      left: `${(ap.pos_x / plano.ancho_px) * 100}%`,
                      top: `${(ap.pos_y / plano.alto_px) * 100}%`,
                    }}
                    title={detalleAp}
                    aria-label={`AP ${indice + 1}: ${ap.ssid || "SSID oculto"}`}
                    onPointerDown={(event) => event.stopPropagation()}
                    onPointerMove={(event) => event.stopPropagation()}
                    onPointerEnter={() => {
                      if (!hint) return;
                      setHintAp({ ...hint, x: ap.pos_x, y: ap.pos_y });
                    }}
                    onPointerLeave={() => setHintAp(null)}
                    onClick={(event) => {
                      event.stopPropagation();
                      setDetalle(detalleAp);
                    }}
                  >
                    {indice + 1}
                  </button>
                );
              })}
            </div>
          )}
          {hintAp && !arrastrando && (
            <div
              className={styles.apHint}
              style={{
                left: `${(hintAp.x / plano.ancho_px) * 100}%`,
                top: `${(hintAp.y / plano.alto_px) * 100}%`,
              }}
            >
              <strong>{hintAp.titulo}</strong>
              <span>{hintAp.resumen}</span>
              <dl>
                {hintAp.detalles.map((detalleItem) => {
                  const [etiqueta, valor] = detalleItem.split(": ");
                  return (
                    <div key={detalleItem}>
                      <dt>{valor ? etiqueta : "Detalle"}</dt>
                      <dd>{valor ?? detalleItem}</dd>
                    </div>
                  );
                })}
              </dl>
            </div>
          )}
          {rssiCursor && !arrastrando && (
            <span className={styles.tooltip} style={{ left: rssiCursor.x + 12, top: rssiCursor.y + 12 }}>{rssiCursor.valor.toFixed(1)} dBm</span>
          )}
        </div>
      </div>

      <div className={styles.leyenda}>
        {mapa.escala.map((item) => <span key={`${item.desde}-${item.hasta}`}><i style={{ background: item.color }} />{item.etiqueta}</span>)}
      </div>

      {detalle && <button type="button" className={styles.detalle} onClick={() => setDetalle(null)}>{detalle}<span>×</span></button>}

      {!compacto && (
        <div className={styles.informacion}>
          <div className={styles.metricas}>
            <Metrica etiqueta="Muestras" valor={String(mapa.cantidad_puntos)} />
            <Metrica etiqueta="Mínimo" valor={`${mapa.rssi_min.toFixed(1)} dBm`} />
            <Metrica etiqueta="Promedio" valor={`${mapa.rssi_promedio.toFixed(1)} dBm`} />
            <Metrica etiqueta="Máximo" valor={`${mapa.rssi_max.toFixed(1)} dBm`} />
            <Metrica etiqueta="Algoritmo" valor={mapa.algoritmo} />
            <Metrica etiqueta="Resolución" valor={`${mapa.resolucion} × ${mapa.resolucion}`} />
          </div>
          <div className={styles.listaAps}>
            {mapa.aps_interes.map((ap) => <button type="button" key={ap.bssid} onClick={() => setDetalle(`${ap.ssid || "SSID oculto"} · ${ap.bssid} · ${ap.rssi_promedio.toFixed(1)} dBm · ${ap.cantidad_puntos} puntos`)}><RadioTower size={15} /><span><strong>{ap.ssid || "SSID oculto"}</strong><small>{ap.bssid} · {ap.rssi_promedio.toFixed(1)} dBm</small></span></button>)}
          </div>
          {mapa.advertencias.length > 0 && <ul className={styles.advertencias}>{mapa.advertencias.map((item) => <li key={item}>{item}</li>)}</ul>}
        </div>
      )}
    </figure>
  );
}

function Metrica({ etiqueta, valor }: { etiqueta: string; valor: string }) {
  return <div><span>{etiqueta}</span><strong>{valor}</strong></div>;
}

function _modoLegible(modo: string): string {
  return ({ INDIVIDUAL: "AP individual", SUBCONJUNTO: "Selección parcial", CONJUNTO_COMPLETO: "Mapa completo" } as Record<string, string>)[modo] ?? modo;
}

function colorRssi(rssi: number): string {
  if (rssi >= -70) return "#A7E84A";
  if (rssi >= -80) return "#F1E64A";
  if (rssi >= -85) return "#C7B84B";
  if (rssi >= -90) return "#7E8173";
  return "#1C1C1C";
}
