import { useState } from "react";
import { ChevronLeft, ChevronRight, Layers3, Trash2, X } from "lucide-react";
import { resolverUrlApi } from "@/shared/api/urlApi";
import { ConfirmDialog, useToast } from "@/shared/components";
import {
  useEliminarMapaCalor,
  useGenerarHeatmapsFaltantesConjunto,
} from "../hooks/useProyectosOrg";
import type { ConjuntoAPOut, MapaCalorOut, PlanoOut } from "../types";
import styles from "../pages/ConjuntosAPProyecto.module.css";

type Props = {
  conjunto: ConjuntoAPOut;
  mapas: MapaCalorOut[];
  plano: PlanoOut;
  onCerrar: () => void;
};

export function ConjuntoAPPreviewModal({
  conjunto,
  mapas,
  plano,
  onCerrar,
}: Props) {
  const mapasObjetivo = _filtrarMapasObjetivo(conjunto, mapas);
  const [mapaActivoIndice, setMapaActivoIndice] = useState(0);
  const [mapaAEliminar, setMapaAEliminar] = useState<MapaCalorOut | null>(null);
  const toast = useToast();
  const { mutateAsync: eliminarMapa, isPending: eliminandoMapa } = useEliminarMapaCalor();
  const {
    mutateAsync: generarFaltantes,
    isPending: generandoFaltantes,
  } = useGenerarHeatmapsFaltantesConjunto();
  const apsConUbicacion = conjunto.items.filter(
    (ap) => typeof ap.pos_x === "number" && typeof ap.pos_y === "number",
  );
  const indiceSeguro =
    mapasObjetivo.length === 0 ? 0 : Math.min(mapaActivoIndice, mapasObjetivo.length - 1);
  const mapaActivo = mapasObjetivo[indiceSeguro];
  const cantidadFaltante = mapaActivo
    ? _cantidadMapasObjetivoFaltantes(conjunto, mapasObjetivo, mapaActivo)
    : 0;
  const irMapaAnterior = () => {
    if (mapasObjetivo.length <= 1) return;
    setMapaActivoIndice((indice) => (indice === 0 ? mapasObjetivo.length - 1 : indice - 1));
  };
  const irMapaSiguiente = () => {
    if (mapasObjetivo.length <= 1) return;
    setMapaActivoIndice((indice) => (indice + 1) % mapasObjetivo.length);
  };
  const confirmarEliminarMapa = async () => {
    if (!mapaAEliminar) return;
    try {
      await eliminarMapa(mapaAEliminar.id);
      setMapaAEliminar(null);
      setMapaActivoIndice((indice) => Math.max(0, indice - 1));
      toast.exito("Mapa de calor eliminado.");
    } catch {
      toast.error("No se pudo eliminar el mapa de calor.");
    }
  };
  const handleGenerarFaltantes = async () => {
    try {
      const generados = await generarFaltantes({
        conjuntoId: conjunto.id,
        body: {
          algoritmo: "IDW",
          resolucion: _resolucionSoportada(mapaActivo?.resolucion ?? 64),
          actualizar_existentes: true,
          reemplazar_existentes: mapasObjetivo.length > 0,
        },
      });
      toast.exito(
        generados.length === 0
          ? "No se generaron cambios en los mapas."
          : `${generados.length} mapa(s) actualizado(s).`,
      );
    } catch (error) {
      toast.error(_detalleError(error, "No se pudieron generar los mapas."));
    }
  };

  return (
    <div className={styles.overlay} role="dialog" aria-modal="true" aria-labelledby="vista-conjunto-titulo">
      <div className={styles.modalVista}>
        <header className={styles.modalHeader}>
          <div>
            <p>{plano.nombre}</p>
            <h2 id="vista-conjunto-titulo">{conjunto.nombre}</h2>
            <span>
              {_labelOrigen(conjunto.origen)} · {conjunto.banda_objetivo} GHz ·{" "}
              {conjunto.cantidad_aps} AP(s)
            </span>
          </div>
          <button type="button" className={styles.cerrarVista} onClick={onCerrar} aria-label="Cerrar vista previa">
            <X size={18} aria-hidden="true" />
          </button>
        </header>

        <section className={styles.seccionGaleria} aria-label="Galería de mapas de calor">
          <div className={styles.tituloGaleria}>
            <h3>Mapas de calor generados</h3>
            <div className={styles.accionesGaleria}>
              <span>{mapasObjetivo.length} mapa(s)</span>
              {mapasObjetivo.length === 0 && apsConUbicacion.length > 0 && (
                <button
                  type="button"
                  className={styles.generarFaltantes}
                  onClick={handleGenerarFaltantes}
                  disabled={generandoFaltantes}
                  title="Generar mapa global e individuales con IDW"
                >
                  <Layers3 size={15} aria-hidden="true" />
                  <span>{generandoFaltantes ? "Generando" : "Generar"}</span>
                </button>
              )}
            </div>
          </div>

          {mapasObjetivo.length === 0 ? (
            <VistaUbicacionesAP plano={plano} aps={apsConUbicacion} />
          ) : mapaActivo ? (
            <div className={styles.carruselHeatmaps}>
              <div className={styles.controlesCarrusel}>
                <button
                  type="button"
                  onClick={irMapaAnterior}
                  disabled={mapasObjetivo.length <= 1}
                  aria-label="Ver mapa anterior"
                >
                  <ChevronLeft size={18} aria-hidden="true" />
                </button>
                <span>
                  {indiceSeguro + 1} / {mapasObjetivo.length}
                </span>
                <button
                  type="button"
                  onClick={irMapaSiguiente}
                  disabled={mapasObjetivo.length <= 1}
                  aria-label="Ver mapa siguiente"
                >
                  <ChevronRight size={18} aria-hidden="true" />
                </button>
              </div>
              <HeatmapCarruselItem
                apsFallback={apsConUbicacion}
                indice={indiceSeguro}
                mapa={mapaActivo}
                cantidadFaltante={cantidadFaltante}
                generandoFaltantes={generandoFaltantes}
                onGenerarFaltantes={handleGenerarFaltantes}
                onEliminar={() => setMapaAEliminar(mapaActivo)}
                plano={plano}
              />
              {mapasObjetivo.length > 1 && (
                <div className={styles.indicadoresCarrusel} aria-label="Seleccionar mapa">
                  {mapasObjetivo.map((mapa, indice) => (
                    <button
                      key={mapa.id}
                      type="button"
                      className={indice === indiceSeguro ? styles.indicadorActivo : ""}
                      onClick={() => setMapaActivoIndice(indice)}
                      aria-label={`Ver mapa ${indice + 1}`}
                    />
                  ))}
                </div>
              )}
            </div>
          ) : null}
        </section>

        {apsConUbicacion.length > 0 && (
          <div className={styles.listaApsPreview}>
            {apsConUbicacion.map((ap, indice) => (
              <article key={`${ap.bssid}-detalle-${indice}`}>
                <strong>{indice + 1}. {ap.ssid || "SSID oculto"}</strong>
                <span>{ap.bssid}</span>
                <small>
                  {typeof ap.rssi_promedio === "number" ? `${ap.rssi_promedio.toFixed(1)} dBm` : "RSSI s/d"}
                  {" · "}
                  {ap.canal ? `canal ${ap.canal}` : "canal s/d"}
                </small>
              </article>
            ))}
          </div>
        )}
      </div>
      {mapaAEliminar && (
        <ConfirmDialog
          titulo="¿Eliminar este mapa de calor?"
          descripcion={`Se eliminará el mapa ${_labelModo(mapaAEliminar.modo_generacion)} generado con algoritmo ${_labelAlgoritmo(mapaAEliminar.algoritmo)}. El registro fuente no será eliminado.`}
          textoConfirmar="Eliminar mapa"
          cargando={eliminandoMapa}
          onCancelar={() => setMapaAEliminar(null)}
          onConfirmar={confirmarEliminarMapa}
        />
      )}
    </div>
  );
}

function VistaUbicacionesAP({
  plano,
  aps,
}: {
  plano: PlanoOut;
  aps: ConjuntoAPOut["items"];
}) {
  return (
    <div className={styles.sinMapasWrapper}>
      <p className={styles.sinUbicaciones}>Este registro todavía no tiene mapas de calor generados.</p>
      {aps.length > 0 && (
        <div className={styles.mapaPreview}>
          <div
            className={styles.planoPreview}
            style={{
              aspectRatio: `${plano.ancho_px} / ${plano.alto_px}`,
              width: `min(100%, calc(46vh * ${plano.ancho_px / plano.alto_px}))`,
            }}
          >
            <img className={styles.planoBase} src={resolverUrlApi(plano.url_firmada)} alt={`Plano ${plano.nombre}`} />
            <div className={styles.capaMarcadores} aria-label="Ubicación de APs del registro">
              {aps.map((ap, indice) => (
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
      )}
    </div>
  );
}

function HeatmapCarruselItem({
  apsFallback,
  cantidadFaltante,
  generandoFaltantes,
  indice,
  mapa,
  onGenerarFaltantes,
  onEliminar,
  plano,
}: {
  apsFallback: ConjuntoAPOut["items"];
  cantidadFaltante: number;
  generandoFaltantes: boolean;
  indice: number;
  mapa: MapaCalorOut;
  onGenerarFaltantes: () => void;
  onEliminar: () => void;
  plano: PlanoOut;
}) {
  const apsMapa = mapa.aps_interes.length > 0 ? mapa.aps_interes : apsFallback;
  return (
    <article className={styles.heatmapCard}>
      <header className={styles.heatmapCardHeader}>
        <div>
          <strong>{_labelModo(mapa.modo_generacion)}</strong>
          <span>{_formatearFechaMapa(mapa.created_at)}</span>
        </div>
        <span className={styles.algoritmoBadge}>
          Algoritmo {_labelAlgoritmo(mapa.algoritmo)}
        </span>
        <div className={styles.accionesMapa}>
          <button
            type="button"
            className={styles.generarFaltantes}
            onClick={onGenerarFaltantes}
            disabled={generandoFaltantes}
            aria-label="Generar o actualizar mapas"
            title={
              cantidadFaltante === 0
                ? "Actualizar mapa global e individuales con IDW"
                : "Generar faltantes y actualizar mapas con IDW"
            }
          >
            <Layers3 size={15} aria-hidden="true" />
            <span>
              {generandoFaltantes
                ? "Generando"
                : cantidadFaltante === 0
                  ? "Actualizar"
                  : "Faltantes"}
            </span>
          </button>
          <button
            type="button"
            className={styles.eliminarMapa}
            onClick={onEliminar}
            aria-label="Eliminar mapa de calor"
            title="Eliminar mapa de calor"
          >
            <Trash2 size={16} aria-hidden="true" />
          </button>
        </div>
      </header>

      <div className={styles.mapaPreview}>
        <div
          className={styles.planoPreview}
          style={{
            aspectRatio: `${plano.ancho_px} / ${plano.alto_px}`,
            width: `min(100%, calc(72vh * ${plano.ancho_px / plano.alto_px}))`,
          }}
        >
          <img
            className={styles.planoBase}
            src={resolverUrlApi(plano.url_firmada)}
            alt=""
          />
          <img
            className={styles.heatmapCapa}
            src={resolverUrlApi(mapa.url_imagen)}
            alt={`Mapa de calor ${indice + 1}`}
          />
          <div className={styles.capaMarcadores} aria-label="Ubicación de APs del mapa de calor">
            {apsMapa
              .filter((ap) => typeof ap.pos_x === "number" && typeof ap.pos_y === "number")
              .map((ap, indiceAp) => (
                <span
                  key={`${mapa.id}-${ap.bssid}-${indiceAp}`}
                  className={styles.marcadorAp}
                  style={{
                    left: `${((ap.pos_x ?? 0) / plano.ancho_px) * 100}%`,
                    top: `${((ap.pos_y ?? 0) / plano.alto_px) * 100}%`,
                  }}
                  title={`${indiceAp + 1}. ${ap.ssid || "SSID oculto"} · ${ap.bssid}`}
                >
                  {indiceAp + 1}
                </span>
              ))}
          </div>
        </div>
      </div>

      <div className={styles.metricasMapa}>
        <span>{mapa.resolucion}px</span>
        <span>{mapa.cantidad_puntos} lectura(s)</span>
        <span>RSSI prom. {mapa.rssi_promedio.toFixed(1)} dBm</span>
      </div>
    </article>
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

function _filtrarMapasObjetivo(
  conjunto: ConjuntoAPOut,
  mapas: MapaCalorOut[],
): MapaCalorOut[] {
  const clavesObjetivo = _clavesMapasObjetivo(conjunto);
  const bssidsConjunto = conjunto.items.map((item) => item.bssid.toLowerCase());
  const claveConjuntoCompleto = _claveBssids(bssidsConjunto);
  const ordenAps = new Map(bssidsConjunto.map((bssid, indice) => [bssid, indice]));

  return mapas
    .filter((mapa) =>
      clavesObjetivo.has(_claveBssids(_bssidsMapa(mapa))),
    )
    .sort((a, b) =>
      _compararMapasGaleria(a, b, claveConjuntoCompleto, ordenAps),
    );
}

function _compararMapasGaleria(
  a: MapaCalorOut,
  b: MapaCalorOut,
  claveConjuntoCompleto: string,
  ordenAps: Map<string, number>,
): number {
  const bssidsA = _bssidsMapa(a);
  const bssidsB = _bssidsMapa(b);
  const prioridadA = _prioridadMapaGaleria(a, bssidsA, claveConjuntoCompleto);
  const prioridadB = _prioridadMapaGaleria(b, bssidsB, claveConjuntoCompleto);
  if (prioridadA !== prioridadB) return prioridadA - prioridadB;

  if (prioridadA === 1) {
    const ordenA = ordenAps.get(bssidsA[0]?.toLowerCase() ?? "") ?? Number.MAX_SAFE_INTEGER;
    const ordenB = ordenAps.get(bssidsB[0]?.toLowerCase() ?? "") ?? Number.MAX_SAFE_INTEGER;
    if (ordenA !== ordenB) return ordenA - ordenB;
  }

  return b.created_at.localeCompare(a.created_at);
}

function _prioridadMapaGaleria(
  mapa: MapaCalorOut,
  bssids: string[],
  claveConjuntoCompleto: string,
): number {
  const claveMapa = _claveBssids(bssids);
  if (
    claveMapa === claveConjuntoCompleto ||
    mapa.modo_generacion === "CONJUNTO_COMPLETO" ||
    mapa.modo_generacion === "PROYECTADO"
  ) {
    return 0;
  }
  if (mapa.modo_generacion === "INDIVIDUAL" || bssids.length === 1) return 1;
  return 2;
}

function _bssidsMapa(mapa: MapaCalorOut): string[] {
  return mapa.bssids_generacion.length > 0 ? mapa.bssids_generacion : [mapa.bssid];
}

function _cantidadMapasObjetivoFaltantes(
  conjunto: ConjuntoAPOut,
  mapas: MapaCalorOut[],
  mapaActivo: MapaCalorOut,
): number {
  const objetivos = Array.from(_clavesMapasObjetivo(conjunto));
  const existentes = new Set(
    mapas
      .filter(
        (mapa) =>
          mapa.algoritmo.toUpperCase() === mapaActivo.algoritmo.toUpperCase() &&
          mapa.resolucion === mapaActivo.resolucion,
      )
      .map((mapa) => _claveBssids(mapa.bssids_generacion.length > 0 ? mapa.bssids_generacion : [mapa.bssid])),
  );
  return objetivos.filter((objetivo) => !existentes.has(objetivo)).length;
}

function _clavesMapasObjetivo(conjunto: ConjuntoAPOut): Set<string> {
  const bssids = conjunto.items.map((item) => item.bssid.toLowerCase());
  return new Set([bssids, ...bssids.map((bssid) => [bssid])].map(_claveBssids));
}

function _claveBssids(bssids: string[]): string {
  return [...bssids].map((bssid) => bssid.toLowerCase()).sort().join("|");
}

function _resolucionSoportada(resolucion: number): 64 | 128 | 256 {
  return resolucion === 128 || resolucion === 256 ? resolucion : 64;
}

function _detalleError(error: unknown, alternativo: string): string {
  return (
    (error as { response?: { data?: { detail?: string } } })?.response?.data
      ?.detail ?? alternativo
  );
}

function _labelModo(modo: string): string {
  return (
    ({
      CONJUNTO_COMPLETO: "Mapa completo",
      INDIVIDUAL: "AP individual",
      SUBCONJUNTO: "Selección parcial",
      PROYECTADO: "Proyección IA",
    } as Record<string, string>)[modo] ?? modo
  );
}

function _labelAlgoritmo(algoritmo: string): string {
  const normalizado = algoritmo.toUpperCase();
  if (normalizado === "IDW") return "IDW";
  return normalizado;
}

function _formatearFechaMapa(fecha: string): string {
  return new Intl.DateTimeFormat("es-BO", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(fecha));
}
