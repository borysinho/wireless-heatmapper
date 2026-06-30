import { useMemo, useState } from "react";
import { Eye, Trash2 } from "lucide-react";
import { useOutletContext } from "react-router-dom";
import { Button, ConfirmDialog, EmptyState, useToast } from "@/shared/components";
import { ConjuntoAPPreviewModal } from "../components/ConjuntoAPPreviewModal";
import {
  useConjuntosPorPlanos,
  useEliminarConjuntoAP,
  useMapasPorPlanos,
  usePlanosProyecto,
} from "../hooks/useProyectosOrg";
import type { ConjuntoAPOut, MapaCalorOut, PlanoOut } from "../types";
import styles from "./ConjuntosAPProyecto.module.css";

type VistaPreviaConjunto = {
  conjunto: ConjuntoAPOut;
  plano: PlanoOut;
};

export default function ConjuntosAPProyecto() {
  const { proyectoId } = useOutletContext<{
    proyectoId: number;
    proyectoNombre: string;
  }>();
  const toast = useToast();
  const [vistaPrevia, setVistaPrevia] = useState<VistaPreviaConjunto | null>(null);
  const [conjuntoEliminar, setConjuntoEliminar] = useState<ConjuntoAPOut | null>(
    null,
  );

  const {
    data: planos,
    isLoading: cargandoPlanos,
    isError: errorPlanos,
  } = usePlanosProyecto(proyectoId);
  const planoIds = useMemo(() => (planos ?? []).map((plano) => plano.id), [planos]);
  const consultasConjuntos = useConjuntosPorPlanos(planoIds);
  const consultasMapas = useMapasPorPlanos(planoIds);

  const conjuntos = useMemo(
    () =>
      consultasConjuntos
        .flatMap((consulta) => consulta.data ?? [])
        .filter((conjunto) => conjunto.origen === "manual_movil")
        .sort((a, b) => (a.updated_at < b.updated_at ? 1 : -1)),
    [consultasConjuntos],
  );
  const planosPorId = useMemo(
    () => new Map((planos ?? []).map((plano) => [plano.id, plano])),
    [planos],
  );
  const mapas = useMemo(
    () => consultasMapas.flatMap((consulta) => consulta.data ?? []),
    [consultasMapas],
  );
  const mapasPorConjunto = useMemo(() => {
    const resultado = new Map<number, MapaCalorOut[]>();
    for (const mapa of mapas) {
      if (!mapa.conjunto_ap_id) continue;
      const lista = resultado.get(mapa.conjunto_ap_id) ?? [];
      lista.push(mapa);
      resultado.set(mapa.conjunto_ap_id, lista);
    }
    for (const lista of resultado.values()) {
      lista.sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
    }
    return resultado;
  }, [mapas]);
  const cargandoConjuntos = consultasConjuntos.some((consulta) => consulta.isLoading);
  const cargandoMapas = consultasMapas.some((consulta) => consulta.isLoading);
  const errorConjuntos = consultasConjuntos.some((consulta) => consulta.isError);
  const errorMapas = consultasMapas.some((consulta) => consulta.isError);
  const resumen = _resumenConjuntos(conjuntos);
  const { mutateAsync: eliminarConjunto, isPending: eliminandoConjunto } =
    useEliminarConjuntoAP();

  const handleEliminarConjunto = async () => {
    if (!conjuntoEliminar) return;
    try {
      await eliminarConjunto(conjuntoEliminar.id);
      toast.exito("Registro de campo eliminado.");
      setConjuntoEliminar(null);
      if (vistaPrevia?.conjunto.id === conjuntoEliminar.id) {
        setVistaPrevia(null);
      }
    } catch {
      toast.error("No se pudo eliminar el registro de campo.");
    }
  };

  if (cargandoPlanos || cargandoConjuntos || cargandoMapas) return <div className={styles.skeleton} />;
  if (errorPlanos || errorConjuntos || errorMapas) {
    return <EmptyState mensaje="No se pudieron cargar los datos de campo." />;
  }
  if (!planos || planos.length === 0) {
    return <EmptyState mensaje="El proyecto todavía no tiene planos." />;
  }

  return (
    <section className={styles.contenedor}>
      <div className={styles.encabezadoSeccion}>
        <div>
          <h2>Datos de campo relevados</h2>
          <p>
            Revise las lecturas reales capturadas por el técnico desde la aplicación móvil.
          </p>
        </div>
      </div>

      <div className={styles.resumen}>
        <ResumenItem etiqueta="Relevamientos móviles" valor={resumen.manual_movil} />
        <ResumenItem etiqueta="Registros disponibles" valor={conjuntos.length} />
      </div>

      {conjuntos.length === 0 ? (
        <EmptyState mensaje="No hay datos de campo relevados para este proyecto." />
      ) : (
        <div className={styles.tablaWrapper}>
          <table className={styles.tabla}>
            <thead>
              <tr>
                <th>Registro</th>
                <th>Plano</th>
                <th>Vista</th>
                <th>Origen</th>
                <th>Banda</th>
                <th>APs</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {conjuntos.map((conjunto) => {
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
                    <td>
                      <span className={styles.banda}>{conjunto.banda_objetivo} GHz</span>
                    </td>
                    <td>{conjunto.cantidad_aps}</td>
                    <td>
                      <Button
                        variante="danger"
                        tamano="sm"
                        disabled={eliminandoConjunto}
                        onClick={() => setConjuntoEliminar(conjunto)}
                      >
                        <Trash2 size={14} aria-hidden="true" />
                        Eliminar
                      </Button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {vistaPrevia && (
        <ConjuntoAPPreviewModal
          conjunto={vistaPrevia.conjunto}
          mapas={mapasPorConjunto.get(vistaPrevia.conjunto.id) ?? []}
          plano={vistaPrevia.plano}
          onCerrar={() => setVistaPrevia(null)}
        />
      )}

      {conjuntoEliminar && (
        <ConfirmDialog
          titulo={`¿Eliminar "${conjuntoEliminar.nombre}"?`}
          descripcion="Se eliminará el registro de campo seleccionado. Los mapas de calor asociados permanecerán como históricos sin registro fuente."
          textoConfirmar="Eliminar"
          cargando={eliminandoConjunto}
          onCancelar={() => setConjuntoEliminar(null)}
          onConfirmar={handleEliminarConjunto}
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
