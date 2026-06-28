/** ABM de proyectos de la organización y acceso al espacio RF. */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BrainCircuit,
  CalendarClock,
  Link2,
  Pencil,
  Plus,
  RadioTower,
  Trash2,
  UserCog,
} from "lucide-react";
import { useClientes } from "../hooks/useClientes";
import { useUsuarios } from "../hooks/useUsuarios";
import {
  useActualizarProyectoAdmin,
  useCrearProyectoAdmin,
  useEliminarProyectoAdmin,
  useProyectosOrg,
  useReasignarTecnico,
} from "../hooks/useProyectosOrg";
import type {
  ProyectoAdminCreate,
  ProyectoListOut,
  ProyectosFilter,
} from "../types";
import { Button, ConfirmDialog, EmptyState, useToast } from "@/shared/components";
import styles from "./ListadoProyectosOrg.module.css";

const formularioVacio: ProyectoAdminCreate = {
  nombre: "",
  descripcion: "",
  cliente_id: null,
  tecnico_id: 0,
  estado: "nuevo",
};

export default function ListadoProyectosOrg() {
  const navigate = useNavigate();
  const toast = useToast();
  const [page, setPage] = useState(1);
  const [filtros, setFiltros] = useState<ProyectosFilter>({});
  const [proyectoEliminar, setProyectoEliminar] = useState<ProyectoListOut | null>(null);
  const [proyectoReasignar, setProyectoReasignar] = useState<ProyectoListOut | null>(null);
  const [nuevoTecnicoId, setNuevoTecnicoId] = useState<number | "">("");
  const [proyectoEditar, setProyectoEditar] = useState<ProyectoListOut | "nuevo" | null>(null);
  const [formulario, setFormulario] = useState<ProyectoAdminCreate>(formularioVacio);
  const [errorModal, setErrorModal] = useState<string | null>(null);

  const { data, isLoading, isError, isFetching } = useProyectosOrg(page, 20, filtros);
  const { data: usuarios } = useUsuarios();
  const { data: clientes } = useClientes();
  const { mutateAsync: crear, isPending: creando } = useCrearProyectoAdmin();
  const { mutateAsync: actualizar, isPending: actualizando } = useActualizarProyectoAdmin();
  const { mutateAsync: eliminar, isPending: eliminando } = useEliminarProyectoAdmin();
  const { mutateAsync: reasignar, isPending: reasignando } = useReasignarTecnico();

  const tecnicos = (usuarios ?? []).filter((u) => u.activo && u.rol === "tecnico");
  const clientesDisponibles = (clientes ?? []).filter(
    (c) => c.activo || (proyectoEditar !== "nuevo" && proyectoEditar?.cliente?.id === c.id),
  );

  const abrirNuevo = () => {
    setFormulario({ ...formularioVacio, tecnico_id: tecnicos[0]?.id ?? 0 });
    setProyectoEditar("nuevo");
    setErrorModal(null);
  };

  const abrirEditar = (proyecto: ProyectoListOut) => {
    setFormulario({
      nombre: proyecto.nombre,
      descripcion: proyecto.descripcion ?? "",
      cliente_id: proyecto.cliente?.id ?? null,
      tecnico_id: proyecto.tecnico.id,
      estado: proyecto.estado,
    });
    setProyectoEditar(proyecto);
    setErrorModal(null);
  };

  const guardarProyecto = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formulario.nombre.trim() || formulario.tecnico_id <= 0) return;
    setErrorModal(null);
    const body = {
      ...formulario,
      nombre: formulario.nombre.trim(),
      descripcion: formulario.descripcion?.trim() || null,
    };
    try {
      if (proyectoEditar === "nuevo") {
        await crear(body);
        toast.exito(
          "Proyecto creado. El técnico recibirá el aviso si habilitó notificaciones.",
        );
      } else if (proyectoEditar) {
        await actualizar({ id: proyectoEditar.id, body });
        toast.exito("Proyecto actualizado correctamente.");
      }
      setProyectoEditar(null);
    } catch (error: unknown) {
      setErrorModal(_detalleError(error, "No se pudo guardar el proyecto."));
    }
  };

  const confirmarEliminar = async () => {
    if (!proyectoEliminar) return;
    try {
      await eliminar(proyectoEliminar.id);
      toast.exito(`Proyecto "${proyectoEliminar.nombre}" eliminado.`);
    } catch (error: unknown) {
      toast.error(_detalleError(error, "No se pudo eliminar el proyecto."));
    } finally {
      setProyectoEliminar(null);
    }
  };

  const confirmarReasignar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!proyectoReasignar || nuevoTecnicoId === "") return;
    setErrorModal(null);
    try {
      await reasignar({ id: proyectoReasignar.id, body: { tecnico_id: Number(nuevoTecnicoId) } });
      toast.exito(
        "Proyecto reasignado. El técnico recibirá el aviso si habilitó notificaciones.",
      );
      setProyectoReasignar(null);
    } catch (error: unknown) {
      setErrorModal(_detalleError(error, "No se pudo reasignar el proyecto."));
    }
  };

  const totalPaginas = data ? Math.max(1, Math.ceil(data.total / 20)) : 1;
  const proyectos = data?.items ?? [];
  const totalPuntos = proyectos.reduce((total, proyecto) => total + proyecto.cantidad_puntos, 0);
  const proyectosConDatos = proyectos.filter((proyecto) => proyecto.cantidad_puntos > 0).length;

  const navegarRF = (proyecto: ProyectoListOut, seccion = "conjuntos-ap") => {
    navigate(`/admin/proyectos/${proyecto.id}/rf/${seccion}`, {
      state: { proyectoNombre: proyecto.nombre },
    });
  };

  return (
    <div>
      <div className={styles.encabezado}>
        <div>
          <p className={styles.preTitulo}>Operación RF</p>
          <h1 className={styles.titulo}>Proyectos RF para publicación</h1>
          <p className={styles.subtitulo}>
            Selección de datos relevados, generación IA y publicación controlada para clientes de Bulldog Tech.
          </p>
        </div>
        <Button onClick={abrirNuevo} disabled={tecnicos.length === 0}>
          <Plus size={15} aria-hidden="true" /> Nuevo proyecto
        </Button>
      </div>

      <div className={styles.filtros}>
        <select
          value={filtros.tecnico_id ?? ""}
          onChange={(e) => {
            setFiltros((prev) => ({ ...prev, tecnico_id: e.target.value ? Number(e.target.value) : undefined }));
            setPage(1);
          }}
          className={styles.select}
          aria-label="Filtrar por técnico"
        >
          <option value="">Todos los técnicos</option>
          {tecnicos.map((tecnico) => <option key={tecnico.id} value={tecnico.id}>{tecnico.nombre}</option>)}
        </select>
        {isFetching && !isLoading && <span className={styles.actualizando}>Actualizando…</span>}
      </div>

      {isLoading ? (
        <div className={styles.skeletonWrapper}>{Array.from({ length: 5 }).map((_, i) => <div key={i} className={styles.skeleton} />)}</div>
      ) : isError ? (
        <EmptyState mensaje="Error al cargar los proyectos." />
      ) : !data || data.total === 0 ? (
        <EmptyState mensaje="No hay proyectos registrados aún." />
      ) : (
        <>
          <section className={styles.resumenFlujo} aria-label="Resumen del flujo RF">
            <article>
              <RadioTower size={18} aria-hidden="true" />
              <span>Datos relevados</span>
              <strong>{totalPuntos} punto(s)</strong>
            </article>
            <article>
              <BrainCircuit size={18} aria-hidden="true" />
              <span>Base para IA</span>
              <strong>{proyectosConDatos} proyecto(s)</strong>
            </article>
            <article>
              <Link2 size={18} aria-hidden="true" />
              <span>Entrega</span>
              <strong>Publicación explícita</strong>
            </article>
          </section>

          <section className={styles.listaProyectos} aria-label="Proyectos RF disponibles">
            {proyectos.map((proyecto) => (
              <article key={proyecto.id} className={styles.tarjetaProyecto}>
                <div className={styles.tarjetaHeader}>
                  <div>
                    <h2>{proyecto.nombre}</h2>
                    <p>{proyecto.cliente?.nombre ?? "Sin cliente asignado"}</p>
                  </div>
                  <span className={styles.actividad}>
                    <CalendarClock size={14} aria-hidden="true" />
                    {new Date(proyecto.ultima_actividad).toLocaleDateString("es-BO")}
                  </span>
                </div>

                <dl className={styles.detalles}>
                  <div>
                    <dt>Técnico</dt>
                    <dd>{proyecto.tecnico.nombre}</dd>
                  </div>
                  <div>
                    <dt>Datos relevados</dt>
                    <dd>{proyecto.cantidad_puntos} punto(s)</dd>
                  </div>
                  <div>
                    <dt>Cliente</dt>
                    <dd>{proyecto.cliente?.nombre ?? "Pendiente"}</dd>
                  </div>
                </dl>

                <div className={styles.flujoRF} aria-label={`Flujo RF de ${proyecto.nombre}`}>
                  <Button variante="secondary" tamano="sm" onClick={() => navegarRF(proyecto, "conjuntos-ap")}>
                    <RadioTower size={14} /> Seleccionar datos
                  </Button>
                  <Button variante="secondary" tamano="sm" onClick={() => navegarRF(proyecto, "escenarios-ia")}>
                    <BrainCircuit size={14} /> Generar IA
                  </Button>
                  <Button variante="secondary" tamano="sm" onClick={() => navegarRF(proyecto, "publicacion")}>
                    <Link2 size={14} /> Publicar al cliente
                  </Button>
                </div>

                <div className={styles.acciones}>
                  <Button variante="ghost" tamano="sm" onClick={() => abrirEditar(proyecto)}><Pencil size={14} /> Editar</Button>
                  <Button variante="ghost" tamano="sm" onClick={() => { setProyectoReasignar(proyecto); setNuevoTecnicoId(""); setErrorModal(null); }}><UserCog size={14} /> Reasignar</Button>
                  <Button variante="danger" tamano="sm" onClick={() => setProyectoEliminar(proyecto)}><Trash2 size={14} /> Eliminar</Button>
                </div>
              </article>
            ))}
          </section>
          {totalPaginas > 1 && <div className={styles.paginacion}>
            <Button variante="secondary" tamano="sm" onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1}>‹ Anterior</Button>
            <span className={styles.infoPag}>Página {page} de {totalPaginas} — {data.total} proyectos</span>
            <Button variante="secondary" tamano="sm" onClick={() => setPage((p) => Math.min(totalPaginas, p + 1))} disabled={page === totalPaginas}>Siguiente ›</Button>
          </div>}
        </>
      )}

      {proyectoEliminar && <ConfirmDialog titulo={`¿Eliminar "${proyectoEliminar.nombre}"?`} descripcion="Se eliminarán también sus datos dependientes." textoConfirmar="Eliminar" cargando={eliminando} onCancelar={() => setProyectoEliminar(null)} onConfirmar={confirmarEliminar} />}

      {proyectoEditar && (
        <div className={styles.overlay} role="dialog" aria-modal="true" aria-labelledby="modal-proyecto">
          <div className={`${styles.modal} ${styles.modalAmplio}`}>
            <h2 id="modal-proyecto" className={styles.modalTitulo}>{proyectoEditar === "nuevo" ? "Nuevo proyecto" : "Editar proyecto"}</h2>
            <p className={styles.modalSubtitulo}>El técnico recibirá una notificación cuando se le asigne el proyecto.</p>
            <form onSubmit={guardarProyecto}>
              <div className={styles.grillaFormulario}>
                <label className={styles.campo}><span>Nombre *</span><input autoFocus required maxLength={200} value={formulario.nombre} onChange={(e) => setFormulario((f) => ({ ...f, nombre: e.target.value }))} /></label>
                <label className={styles.campo}><span>Técnico *</span><select required value={formulario.tecnico_id || ""} onChange={(e) => setFormulario((f) => ({ ...f, tecnico_id: Number(e.target.value) }))}><option value="">Seleccione…</option>{tecnicos.map((t) => <option key={t.id} value={t.id}>{t.nombre}</option>)}</select></label>
                <label className={styles.campo}><span>Cliente</span><select value={formulario.cliente_id ?? ""} onChange={(e) => setFormulario((f) => ({ ...f, cliente_id: e.target.value ? Number(e.target.value) : null }))}><option value="">Sin cliente</option>{clientesDisponibles.map((c) => <option key={c.id} value={c.id}>{c.nombre}{c.activo ? "" : " (inactivo)"}</option>)}</select></label>
                <label className={`${styles.campo} ${styles.campoCompleto}`}><span>Descripción</span><textarea rows={3} maxLength={500} value={formulario.descripcion ?? ""} onChange={(e) => setFormulario((f) => ({ ...f, descripcion: e.target.value }))} /></label>
              </div>
              {errorModal && <p className={styles.modalError} role="alert">{errorModal}</p>}
              <div className={styles.modalAcciones}><Button variante="secondary" type="button" onClick={() => setProyectoEditar(null)}>Cancelar</Button><Button type="submit" isLoading={creando || actualizando} disabled={!formulario.nombre.trim() || formulario.tecnico_id <= 0}>Guardar</Button></div>
            </form>
          </div>
        </div>
      )}

      {proyectoReasignar && (
        <div className={styles.overlay} role="dialog" aria-modal="true" aria-labelledby="modal-reasignar">
          <div className={styles.modal}>
            <h2 id="modal-reasignar" className={styles.modalTitulo}>Reasignar técnico</h2>
            <p className={styles.modalSubtitulo}>Proyecto: <strong>{proyectoReasignar.nombre}</strong><br />Técnico actual: <strong>{proyectoReasignar.tecnico.nombre}</strong></p>
            <form onSubmit={confirmarReasignar}>
              <label className={styles.modalLabel} htmlFor="select-tecnico">Nuevo técnico</label>
              <select id="select-tecnico" className={styles.modalSelect} value={nuevoTecnicoId} onChange={(e) => setNuevoTecnicoId(e.target.value ? Number(e.target.value) : "")} required><option value="">Seleccione…</option>{tecnicos.filter((t) => t.id !== proyectoReasignar.tecnico.id).map((t) => <option key={t.id} value={t.id}>{t.nombre} ({t.email})</option>)}</select>
              {errorModal && <p className={styles.modalError} role="alert">{errorModal}</p>}
              <div className={styles.modalAcciones}><Button variante="secondary" type="button" onClick={() => setProyectoReasignar(null)}>Cancelar</Button><Button type="submit" isLoading={reasignando} disabled={nuevoTecnicoId === ""}>Confirmar</Button></div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function _detalleError(error: unknown, alternativo: string): string {
  return (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? alternativo;
}
