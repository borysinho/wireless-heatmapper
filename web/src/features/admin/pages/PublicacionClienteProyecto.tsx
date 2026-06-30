import { useMemo, useState, type ReactNode } from "react";
import {
  CheckSquare,
  Copy,
  ExternalLink,
  Link2,
  Mail,
  RotateCcw,
  Trash2,
  XCircle,
} from "lucide-react";
import { useOutletContext } from "react-router-dom";
import { Button, ConfirmDialog, EmptyState, useToast } from "@/shared/components";
import {
  useActualizarEnlaceCliente,
  useConjuntosPorPlanos,
  useCrearEnlaceCliente,
  useEliminarEnlaceCliente,
  useEliminarEnlacesClienteProyecto,
  useEnlacesCliente,
  useEnviarCorreoEnlaceCliente,
  useMapasPorPlanos,
  usePlanosProyecto,
  useProyectoAdmin,
} from "../hooks/useProyectosOrg";
import type { ConjuntoAPOut, MapaCalorOut, PlanoOut } from "../types";
import styles from "./PublicacionClienteProyecto.module.css";

export default function PublicacionClienteProyecto() {
  const { proyectoId } = useOutletContext<{
    proyectoId: number;
    proyectoNombre: string;
  }>();
  const toast = useToast();
  const [diasEnlace, setDiasEnlace] = useState(7);
  const [clienteDestinoId, setClienteDestinoId] = useState<number | null>(null);
  const [ultimoEnlace, setUltimoEnlace] = useState<string | null>(null);
  const [enlaceEliminarId, setEnlaceEliminarId] = useState<number | null>(null);
  const [confirmarEliminarTodos, setConfirmarEliminarTodos] = useState(false);
  const [conjuntosSeleccionados, setConjuntosSeleccionados] = useState<Set<number>>(
    () => new Set(),
  );

  const { data: planos, isLoading: cargandoPlanos, isError: errorPlanos } =
    usePlanosProyecto(proyectoId);
  const planoIds = useMemo(() => (planos ?? []).map((plano) => plano.id), [planos]);
  const consultasConjuntos = useConjuntosPorPlanos(planoIds);
  const consultasMapas = useMapasPorPlanos(planoIds);
  const { data: proyecto, isLoading: cargandoProyecto, isError: errorProyecto } =
    useProyectoAdmin(proyectoId);
  const { data: enlacesCliente, isLoading: cargandoEnlaces } =
    useEnlacesCliente(proyectoId);
  const { mutateAsync: crearEnlace, isPending: creandoEnlace } =
    useCrearEnlaceCliente(proyectoId);
  const { mutateAsync: actualizarEnlace, isPending: actualizandoEnlace } =
    useActualizarEnlaceCliente(proyectoId);
  const { mutateAsync: eliminarEnlace, isPending: eliminandoEnlace } =
    useEliminarEnlaceCliente(proyectoId);
  const { mutateAsync: eliminarTodosEnlaces, isPending: eliminandoTodosEnlaces } =
    useEliminarEnlacesClienteProyecto(proyectoId);
  const { mutateAsync: enviarCorreoEnlace, isPending: enviandoCorreo } =
    useEnviarCorreoEnlaceCliente(proyectoId);

  const conjuntos = useMemo(
    () =>
      consultasConjuntos
        .flatMap((consulta) => consulta.data ?? [])
        .sort((a, b) => (a.updated_at < b.updated_at ? 1 : -1)),
    [consultasConjuntos],
  );
  const conjuntosPublicables = useMemo(
    () =>
      conjuntos
        .sort((a, b) => (a.updated_at < b.updated_at ? 1 : -1)),
    [conjuntos],
  );
  const mapas = useMemo(
    () => consultasMapas.flatMap((consulta) => consulta.data ?? []),
    [consultasMapas],
  );
  const cargandoConjuntos = consultasConjuntos.some((consulta) => consulta.isLoading);
  const errorConjuntos = consultasConjuntos.some((consulta) => consulta.isError);
  const cargandoMapas = consultasMapas.some((consulta) => consulta.isLoading);
  const errorMapas = consultasMapas.some((consulta) => consulta.isError);
  const cargando =
    cargandoPlanos ||
    cargandoConjuntos ||
    cargandoMapas ||
    cargandoProyecto;
  const error =
    errorPlanos ||
    errorConjuntos ||
    errorMapas ||
    errorProyecto;
  const clienteProyecto = proyecto?.cliente ?? null;
  const clienteProyectoConCorreo =
    clienteProyecto?.email_referencia ? clienteProyecto : null;
  const clienteDestino =
    clienteProyectoConCorreo?.id === clienteDestinoId
      ? clienteProyectoConCorreo
      : null;

  const conjuntosSeleccionadosPublicados = useMemo(
    () =>
      conjuntosPublicables.filter((conjunto) =>
        conjuntosSeleccionados.has(conjunto.id),
      ),
    [conjuntosPublicables, conjuntosSeleccionados],
  );
  const totalSeleccionado = conjuntosSeleccionadosPublicados.length;
  const todosSeleccionados =
    conjuntosPublicables.length > 0 &&
    conjuntosPublicables.every((conjunto) =>
      conjuntosSeleccionados.has(conjunto.id),
    );
  const mapasSeleccionadosPublicados = useMemo(() => {
    const conjuntoIds = new Set(
      conjuntosSeleccionadosPublicados.map((conjunto) => conjunto.id),
    );
    return mapas.filter(
      (mapa) =>
        typeof mapa.conjunto_ap_id === "number" &&
        conjuntoIds.has(mapa.conjunto_ap_id),
    );
  }, [conjuntosSeleccionadosPublicados, mapas]);
  const gruposPorPlano = useMemo(
    () => _agruparContenidoPorPlano(planos ?? [], conjuntosPublicables, mapas),
    [planos, conjuntosPublicables, mapas],
  );

  const handleCrearEnlace = async () => {
    if (totalSeleccionado === 0) {
      toast.error("Seleccione al menos un contenido para el cliente.");
      return;
    }
    if (clienteDestinoId !== null && !clienteDestino?.email_referencia) {
      toast.error("El cliente seleccionado no tiene correo de referencia registrado.");
      return;
    }
    try {
      const enlace = await crearEnlace({
        expira_en_dias: diasEnlace,
        cliente_id: clienteDestinoId,
        contenido: {
          conjunto_ids: conjuntosSeleccionadosPublicados.map((item) => item.id),
          mapa_ids: mapasSeleccionadosPublicados.map((item) => item.id),
        },
      });
      const url = `${window.location.origin}${enlace.url_publica}`;
      setUltimoEnlace(url);
      const copiado = await _copiar(url);
      toast.exito(
        clienteDestino
          ? "Enlace creado y enviado al cliente."
          : copiado
            ? "Enlace de cliente creado y copiado."
            : "Enlace de cliente creado.",
      );
    } catch {
      toast.error("No se pudo crear el enlace de cliente.");
    }
  };

  const handleToggleTodosConjuntos = () => {
    setConjuntosSeleccionados((prev) => {
      if (todosSeleccionados) return new Set();
      return new Set([
        ...prev,
        ...conjuntosPublicables.map((conjunto) => conjunto.id),
      ]);
    });
  };

  const handleActualizarEnlace = async (enlaceId: number, revocado: boolean) => {
    try {
      await actualizarEnlace({ enlaceId, revocado });
      toast.exito(revocado ? "Enlace revocado." : "Enlace reactivado.");
    } catch {
      toast.error("No se pudo actualizar el enlace.");
    }
  };

  const handleEnviarCorreo = async (enlaceId: number) => {
    if (!clienteProyectoConCorreo) {
      toast.error("El cliente del proyecto no tiene correo de referencia registrado.");
      return;
    }
    try {
      await enviarCorreoEnlace({
        enlaceId,
        clienteId: clienteProyectoConCorreo.id,
      });
      toast.exito("Correo enviado al cliente.");
    } catch {
      toast.error("No se pudo enviar el correo del enlace.");
    }
  };

  const handleCopiar = async (urlPublica: string) => {
    const url = `${window.location.origin}${urlPublica}`;
    setUltimoEnlace(url);
    const copiado = await _copiar(url);
    toast.exito(copiado ? "Enlace copiado." : "Enlace disponible en pantalla.");
  };

  const handleEliminarEnlace = async () => {
    if (enlaceEliminarId === null) return;
    try {
      await eliminarEnlace(enlaceEliminarId);
      toast.exito("Enlace eliminado.");
      setEnlaceEliminarId(null);
    } catch {
      toast.error("No se pudo eliminar el enlace.");
    }
  };

  const handleEliminarTodosEnlaces = async () => {
    try {
      await eliminarTodosEnlaces();
      toast.exito("Enlaces eliminados.");
      setConfirmarEliminarTodos(false);
    } catch {
      toast.error("No se pudieron eliminar los enlaces.");
    }
  };

  if (cargando) return <div className={styles.skeleton} />;
  if (error) return <EmptyState mensaje="No se pudo cargar el contenido publicable." />;

  return (
    <section className={styles.contenedor}>
      <div className={styles.encabezadoSeccion}>
        <div>
          <h2>Publicación al cliente</h2>
          <p>El enlace incluye los datos seleccionados, sean relevados en campo o propuestos por IA.</p>
        </div>
      </div>

      <div className={styles.publicacionGrid}>
        <PanelSeleccion
          titulo="Contenido disponible"
          vacio="No hay contenido disponible para este proyecto."
          acciones={
            <Button
              type="button"
              variante="secondary"
              tamano="sm"
              disabled={conjuntosPublicables.length === 0}
              onClick={handleToggleTodosConjuntos}
            >
              <CheckSquare size={14} aria-hidden="true" />
              {todosSeleccionados ? "Quitar selección" : "Seleccionar todos"}
            </Button>
          }
        >
          {gruposPorPlano.map((grupo) => (
            <div key={grupo.planoId} className={styles.grupoPlano}>
              <div className={styles.grupoPlanoHeader}>
                <div>
                  <strong>{grupo.nombre}</strong>
                  <small>
                    {grupo.conjuntos.length} contenido(s) · {grupo.mapas.length} mapa(s)
                  </small>
                </div>
              </div>
              {grupo.conjuntos.map((conjunto) => (
                <SeleccionConjunto
                  key={conjunto.id}
                  conjunto={conjunto}
                  mapas={grupo.mapasPorConjunto.get(conjunto.id) ?? []}
                  seleccionado={conjuntosSeleccionados.has(conjunto.id)}
                  onToggle={() =>
                    setConjuntosSeleccionados((prev) =>
                      _toggleSet(prev, conjunto.id),
                    )
                  }
                />
              ))}
            </div>
          ))}
        </PanelSeleccion>

        <section className={styles.panelGeneracion}>
          <div className={styles.panelGeneracionHeader}>
            <h2>Enlace de cliente</h2>
            <span>
              {totalSeleccionado} contenido(s) · {mapasSeleccionadosPublicados.length} mapa(s)
            </span>
          </div>
          <div className={styles.generador}>
            <label>
              Vigencia
              <select
                value={diasEnlace}
                onChange={(event) => setDiasEnlace(Number(event.target.value))}
              >
                <option value={1}>1 día</option>
                <option value={7}>7 días</option>
                <option value={30}>30 días</option>
                <option value={90}>90 días</option>
              </select>
            </label>
            <label className={styles.clienteDestino}>
              Cliente
              <select
                value={clienteDestinoId ?? ""}
                onChange={(event) =>
                  setClienteDestinoId(event.target.value ? Number(event.target.value) : null)
                }
              >
                <option value="">Solo generar enlace</option>
                {clienteProyectoConCorreo && (
                  <option
                    value={clienteProyectoConCorreo.id}
                  >
                    {clienteProyectoConCorreo.nombre} ·{" "}
                    {clienteProyectoConCorreo.email_referencia}
                  </option>
                )}
              </select>
            </label>
            <Button
              type="button"
              disabled={totalSeleccionado === 0}
              isLoading={creandoEnlace}
              onClick={handleCrearEnlace}
            >
              {clienteDestino ? (
                <Mail size={16} aria-hidden="true" />
              ) : (
                <Link2 size={16} aria-hidden="true" />
              )}
              {clienteDestino ? "Enviar enlace" : "Generar enlace"}
            </Button>
          </div>
          {ultimoEnlace && <p className={styles.enlaceReciente}>{ultimoEnlace}</p>}
        </section>
      </div>

      <section className={styles.enlaces}>
        <div className={styles.enlacesHeader}>
          <h2>Enlaces generados</h2>
          <Button
            type="button"
            variante="danger"
            tamano="sm"
            disabled={
              !enlacesCliente ||
              enlacesCliente.length === 0 ||
              eliminandoTodosEnlaces
            }
            isLoading={eliminandoTodosEnlaces}
            onClick={() => setConfirmarEliminarTodos(true)}
          >
            <Trash2 size={14} aria-hidden="true" />
            Eliminar todos
          </Button>
        </div>
        {cargandoEnlaces ? (
          <div className={styles.skeletonMini} />
        ) : !enlacesCliente || enlacesCliente.length === 0 ? (
          <EmptyState mensaje="Todavía no hay enlaces de cliente para este proyecto." />
        ) : (
          <div className={styles.enlacesLista}>
            {enlacesCliente.map((enlace) => (
                <div key={enlace.id} className={styles.enlaceRow}>
                  <div>
                    <strong>
                      {enlace.revocado ? "Revocado" : "Activo"} · vence{" "}
                      {_fechaCorta(enlace.expira_en)}
                    </strong>
                    <small>
                      {enlace.accesos} acceso(s) ·{" "}
                      {enlace.contenido.conjunto_ids.length} contenido(s) ·{" "}
                      {enlace.contenido.mapa_ids.length} mapa(s)
                    </small>
                  </div>
                  <div className={styles.enlaceAcciones}>
                    <Button
                      type="button"
                      variante="secondary"
                      tamano="sm"
                      disabled={
                        enlace.revocado ||
                        !clienteProyectoConCorreo ||
                        enviandoCorreo
                      }
                      isLoading={enviandoCorreo}
                      onClick={() => handleEnviarCorreo(enlace.id)}
                      title={
                        clienteProyectoConCorreo
                          ? `Enviar a ${clienteProyectoConCorreo.email_referencia}`
                          : "El cliente no tiene correo de referencia"
                      }
                    >
                      <Mail size={14} aria-hidden="true" />
                      Enviar
                    </Button>
                    <Button
                      type="button"
                      variante="ghost"
                      tamano="sm"
                      onClick={() => handleCopiar(enlace.url_publica)}
                    >
                      <Copy size={14} aria-hidden="true" />
                      Copiar
                    </Button>
                    <a
                      className={styles.abrirEnlace}
                      href={enlace.url_publica}
                      target="_blank"
                      rel="noreferrer"
                      aria-label="Abrir enlace"
                    >
                      <ExternalLink size={14} aria-hidden="true" />
                    </a>
                    <Button
                      type="button"
                      variante={enlace.revocado ? "secondary" : "danger"}
                      tamano="sm"
                      disabled={actualizandoEnlace}
                      onClick={() =>
                        handleActualizarEnlace(enlace.id, !enlace.revocado)
                      }
                    >
                      {enlace.revocado ? (
                        <RotateCcw size={14} aria-hidden="true" />
                      ) : (
                        <XCircle size={14} aria-hidden="true" />
                      )}
                      {enlace.revocado ? "Reactivar" : "Revocar"}
                    </Button>
                    <Button
                      type="button"
                      variante="danger"
                      tamano="sm"
                      disabled={eliminandoEnlace}
                      onClick={() => setEnlaceEliminarId(enlace.id)}
                    >
                      <Trash2 size={14} aria-hidden="true" />
                      Eliminar
                    </Button>
                  </div>
                </div>
              ))}
          </div>
        )}
      </section>

      {enlaceEliminarId !== null && (
        <ConfirmDialog
          titulo="¿Eliminar enlace?"
          descripcion="Se eliminará el registro del enlace generado y dejará de estar disponible para el cliente."
          textoConfirmar="Eliminar"
          cargando={eliminandoEnlace}
          onCancelar={() => setEnlaceEliminarId(null)}
          onConfirmar={handleEliminarEnlace}
        />
      )}

      {confirmarEliminarTodos && (
        <ConfirmDialog
          titulo="¿Eliminar todos los enlaces?"
          descripcion="Se eliminarán todos los enlaces generados para este proyecto. El contenido y los mapas publicados no serán modificados."
          textoConfirmar="Eliminar todos"
          cargando={eliminandoTodosEnlaces}
          onCancelar={() => setConfirmarEliminarTodos(false)}
          onConfirmar={handleEliminarTodosEnlaces}
        />
      )}
    </section>
  );
}

function PanelSeleccion({
  titulo,
  vacio,
  children,
  acciones,
}: {
  titulo: string;
  vacio: string;
  children?: ReactNode;
  acciones?: ReactNode;
}) {
  const items = Array.isArray(children) ? children.filter(Boolean) : children;
  const estaVacio = Array.isArray(items) ? items.length === 0 : !items;
  return (
    <section className={styles.panelSeleccion}>
      <div className={styles.panelSeleccionHeader}>
        <h2>{titulo}</h2>
        {acciones}
      </div>
      {estaVacio ? <p className={styles.vacio}>{vacio}</p> : <div>{items}</div>}
    </section>
  );
}

function SeleccionConjunto({
  conjunto,
  mapas,
  seleccionado,
  onToggle,
}: {
  conjunto: ConjuntoAPOut;
  mapas: MapaCalorOut[];
  seleccionado: boolean;
  onToggle: () => void;
}) {
  return (
    <label className={styles.itemSeleccion}>
      <input type="checkbox" checked={seleccionado} onChange={onToggle} />
      <span>
        <strong>{conjunto.nombre}</strong>
        <small>
          {_labelOrigen(conjunto.origen)} · {conjunto.cantidad_aps} APs
        </small>
        <span className={styles.itemMeta}>
          <span>{mapas.length} mapa(s) generados</span>
          <span>{conjunto.banda_objetivo} GHz</span>
        </span>
      </span>
    </label>
  );
}

function _toggleSet(prev: Set<number>, id: number): Set<number> {
  const siguiente = new Set(prev);
  if (siguiente.has(id)) {
    siguiente.delete(id);
  } else {
    siguiente.add(id);
  }
  return siguiente;
}

async function _copiar(texto: string): Promise<boolean> {
  if (!navigator.clipboard?.writeText) return false;
  try {
    await navigator.clipboard.writeText(texto);
    return true;
  } catch {
    return false;
  }
}

function _fechaCorta(valor: string): string {
  return new Intl.DateTimeFormat("es-BO", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(valor));
}

function _labelOrigen(origen: string): string {
  const mapa: Record<string, string> = {
    manual_movil: "Móvil",
    manual_web: "Web",
    ia: "IA",
  };
  return mapa[origen] ?? origen;
}

function _agruparContenidoPorPlano(
  planos: PlanoOut[],
  conjuntos: ConjuntoAPOut[],
  mapas: MapaCalorOut[],
) {
  const planosPorId = new Map(planos.map((plano) => [plano.id, plano]));
  const mapasPorPlano = new Map<number, MapaCalorOut[]>();
  const mapasPorConjunto = new Map<number, MapaCalorOut[]>();
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
      conjuntos: ConjuntoAPOut[];
      mapas: MapaCalorOut[];
      mapasPorConjunto: Map<number, MapaCalorOut[]>;
    }
  >();
  for (const conjunto of conjuntos) {
    const plano = planosPorId.get(conjunto.plano_id);
    const grupo = grupos.get(conjunto.plano_id) ?? {
      planoId: conjunto.plano_id,
      nombre: plano?.nombre ?? `Plano ${conjunto.plano_id}`,
      conjuntos: [],
      mapas: mapasPorPlano.get(conjunto.plano_id) ?? [],
      mapasPorConjunto,
    };
    grupo.conjuntos.push(conjunto);
    grupos.set(conjunto.plano_id, grupo);
  }
  return Array.from(grupos.values()).sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
}
