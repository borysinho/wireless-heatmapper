import { useMemo, useState, type ReactNode } from "react";
import { Copy, ExternalLink, Link2, Mail, RotateCcw, XCircle } from "lucide-react";
import { useOutletContext } from "react-router-dom";
import { Button, EmptyState, useToast } from "@/shared/components";
import {
  useActualizarEnlaceCliente,
  useConjuntosPorPlanos,
  useCrearEnlaceCliente,
  useEnlacesCliente,
  useEnviarCorreoEnlaceCliente,
  usePlanosProyecto,
} from "../hooks/useProyectosOrg";
import { useClientes } from "../hooks/useClientes";
import type { ConjuntoAPOut } from "../types";
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
  const [clientesEnvioPorEnlace, setClientesEnvioPorEnlace] = useState<
    Record<number, number | "">
  >({});
  const [conjuntosSeleccionados, setConjuntosSeleccionados] = useState<Set<number>>(
    () => new Set(),
  );

  const { data: planos, isLoading: cargandoPlanos, isError: errorPlanos } =
    usePlanosProyecto(proyectoId);
  const planoIds = useMemo(() => (planos ?? []).map((plano) => plano.id), [planos]);
  const consultasConjuntos = useConjuntosPorPlanos(planoIds);
  const { data: clientes, isLoading: cargandoClientes, isError: errorClientes } =
    useClientes();
  const { data: enlacesCliente, isLoading: cargandoEnlaces } =
    useEnlacesCliente(proyectoId);
  const { mutateAsync: crearEnlace, isPending: creandoEnlace } =
    useCrearEnlaceCliente(proyectoId);
  const { mutateAsync: actualizarEnlace, isPending: actualizandoEnlace } =
    useActualizarEnlaceCliente(proyectoId);
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
  const cargandoConjuntos = consultasConjuntos.some((consulta) => consulta.isLoading);
  const errorConjuntos = consultasConjuntos.some((consulta) => consulta.isError);
  const cargando =
    cargandoPlanos ||
    cargandoConjuntos ||
    cargandoClientes;
  const error =
    errorPlanos ||
    errorConjuntos ||
    errorClientes;
  const clientesActivos = useMemo(
    () => (clientes ?? []).filter((cliente) => cliente.activo),
    [clientes],
  );
  const clienteDestino =
    clientesActivos.find((cliente) => cliente.id === clienteDestinoId) ?? null;

  const conjuntosSeleccionadosPublicados = useMemo(
    () =>
      conjuntosPublicables.filter((conjunto) =>
        conjuntosSeleccionados.has(conjunto.id),
      ),
    [conjuntosPublicables, conjuntosSeleccionados],
  );
  const totalSeleccionado = conjuntosSeleccionadosPublicados.length;

  const handleCrearEnlace = async () => {
    if (totalSeleccionado === 0) {
      toast.error("Seleccione al menos un conjunto para el cliente.");
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

  const handleActualizarEnlace = async (enlaceId: number, revocado: boolean) => {
    try {
      await actualizarEnlace({ enlaceId, revocado });
      toast.exito(revocado ? "Enlace revocado." : "Enlace reactivado.");
    } catch {
      toast.error("No se pudo actualizar el enlace.");
    }
  };

  const handleEnviarCorreo = async (enlaceId: number) => {
    const clienteId = clientesEnvioPorEnlace[enlaceId];
    if (typeof clienteId !== "number") {
      toast.error("Seleccione un cliente con correo de referencia.");
      return;
    }
    const cliente = clientesActivos.find((item) => item.id === clienteId);
    if (!cliente?.email_referencia) {
      toast.error("El cliente seleccionado no tiene correo de referencia registrado.");
      return;
    }
    try {
      await enviarCorreoEnlace({ enlaceId, clienteId });
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

  if (cargando) return <div className={styles.skeleton} />;
  if (error) return <EmptyState mensaje="No se pudo cargar el contenido publicable." />;

  return (
    <section className={styles.contenedor}>
      <div className={styles.encabezadoSeccion}>
        <div>
          <h2>Publicación al cliente</h2>
          <p>El enlace incluye los conjuntos seleccionados, sean relevados en campo o propuestos por IA.</p>
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
              {clientesActivos.map((cliente) => (
                <option
                  key={cliente.id}
                  value={cliente.id}
                  disabled={!cliente.email_referencia}
                >
                  {cliente.nombre}
                  {cliente.email_referencia
                    ? ` · ${cliente.email_referencia}`
                    : " · sin correo de referencia"}
                </option>
              ))}
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
      </div>

      <div className={styles.selectorGrid}>
        <PanelSeleccion
          titulo="Conjuntos disponibles"
          vacio="No hay conjuntos disponibles para este proyecto."
        >
          {conjuntosPublicables.map((conjunto) => (
            <SeleccionConjunto
              key={conjunto.id}
              conjunto={conjunto}
              seleccionado={conjuntosSeleccionados.has(conjunto.id)}
              onToggle={() =>
                setConjuntosSeleccionados((prev) =>
                  _toggleSet(prev, conjunto.id),
                )
              }
            />
          ))}
        </PanelSeleccion>

        <PanelSeleccion
          titulo="Criterio de publicación"
          vacio="Seleccione conjuntos específicos para crear el enlace."
        />
      </div>

      {ultimoEnlace && <p className={styles.enlaceReciente}>{ultimoEnlace}</p>}

      <section className={styles.enlaces}>
        <h2>Enlaces generados</h2>
        {cargandoEnlaces ? (
          <div className={styles.skeletonMini} />
        ) : !enlacesCliente || enlacesCliente.length === 0 ? (
          <EmptyState mensaje="Todavía no hay enlaces de cliente para este proyecto." />
        ) : (
          <div className={styles.enlacesLista}>
            {enlacesCliente.map((enlace) => {
              const clienteEnvioId = clientesEnvioPorEnlace[enlace.id] ?? "";
              return (
                <div key={enlace.id} className={styles.enlaceRow}>
                  <div>
                    <strong>
                      {enlace.revocado ? "Revocado" : "Activo"} · vence{" "}
                      {_fechaCorta(enlace.expira_en)}
                    </strong>
                    <small>
                      {enlace.accesos} acceso(s) ·{" "}
                      {enlace.contenido.conjunto_ids.length} conjunto(s)
                    </small>
                  </div>
                  <div className={styles.enlaceAcciones}>
                    <select
                      className={styles.selectorCorreo}
                      value={clienteEnvioId}
                      disabled={enlace.revocado || enviandoCorreo}
                      aria-label="Cliente destino para correo"
                      onChange={(event) =>
                        setClientesEnvioPorEnlace((prev) => ({
                          ...prev,
                          [enlace.id]: event.target.value
                            ? Number(event.target.value)
                            : "",
                        }))
                      }
                    >
                      <option value="">Cliente</option>
                      {clientesActivos.map((cliente) => (
                        <option
                          key={cliente.id}
                          value={cliente.id}
                          disabled={!cliente.email_referencia}
                        >
                          {cliente.nombre}
                          {cliente.email_referencia
                            ? ` · ${cliente.email_referencia}`
                            : " · sin correo"}
                        </option>
                      ))}
                    </select>
                    <Button
                      type="button"
                      variante="secondary"
                      tamano="sm"
                      disabled={
                        enlace.revocado ||
                        typeof clienteEnvioId !== "number" ||
                        enviandoCorreo
                      }
                      isLoading={enviandoCorreo}
                      onClick={() => handleEnviarCorreo(enlace.id)}
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
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </section>
  );
}

function PanelSeleccion({
  titulo,
  vacio,
  children,
}: {
  titulo: string;
  vacio: string;
  children?: ReactNode;
}) {
  const items = Array.isArray(children) ? children.filter(Boolean) : children;
  const estaVacio = Array.isArray(items) ? items.length === 0 : !items;
  return (
    <section className={styles.panelSeleccion}>
      <h2>{titulo}</h2>
      {estaVacio ? <p className={styles.vacio}>{vacio}</p> : <div>{items}</div>}
    </section>
  );
}

function SeleccionConjunto({
  conjunto,
  seleccionado,
  onToggle,
}: {
  conjunto: ConjuntoAPOut;
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
