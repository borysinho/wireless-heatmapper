import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  Building2,
  CheckCircle2,
  ClipboardList,
  Clock3,
  Link2,
  RadioTower,
  Users,
} from "lucide-react";
import { Button, EmptyState } from "@/shared/components";
import { useClientes } from "../hooks/useClientes";
import { useProyectosOrg } from "../hooks/useProyectosOrg";
import { useUsuarios } from "../hooks/useUsuarios";
import type { ProyectoListOut } from "../types";
import styles from "./DashboardAdmin.module.css";

function formatearFecha(fecha: string) {
  return new Date(fecha).toLocaleDateString("es-BO", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function etiquetaEstado(estado: ProyectoListOut["estado"]) {
  const etiquetas = {
    nuevo: "Creado",
    en_progreso: "En campo",
    completado: "Listo para entrega",
    archivado: "Archivado",
  };
  return etiquetas[estado];
}

function etapaOperativa(proyecto: ProyectoListOut) {
  if (proyecto.estado === "archivado") return "Archivado";
  if (proyecto.estado === "completado") return "Pendiente de publicación";
  if (proyecto.cantidad_puntos > 0) return "Con mediciones RF";
  if (!proyecto.cliente) return "Requiere cliente";
  return "Pendiente de captura";
}

export default function DashboardAdmin() {
  const navigate = useNavigate();
  const { data: proyectos, isLoading, isError } = useProyectosOrg(1, 100);
  const { data: usuarios } = useUsuarios();
  const { data: clientes } = useClientes();

  const resumen = useMemo(() => {
    const items = proyectos?.items ?? [];
    const activos = items.filter((p) => p.estado !== "archivado");
    const sinCliente = activos.filter((p) => !p.cliente).length;
    const pendientesMedicion = activos.filter((p) => p.cantidad_puntos === 0).length;
    const completados = activos.filter((p) => p.estado === "completado").length;

    return {
      proyectosActivos: activos.length,
      proyectosConDatos: items.filter((p) => p.cantidad_puntos > 0).length,
      puntosCapturados: items.reduce((total, p) => total + p.cantidad_puntos, 0),
      sinCliente,
      pendientesMedicion,
      completados,
      tecnicos: (usuarios ?? []).filter((u) => u.activo && u.rol === "tecnico").length,
      clientes: (clientes ?? []).filter((c) => c.activo).length,
      recientes: [...items]
        .sort((a, b) => new Date(b.ultima_actividad).getTime() - new Date(a.ultima_actividad).getTime())
        .slice(0, 5),
    };
  }, [clientes, proyectos, usuarios]);

  return (
    <div>
      <header className={styles.encabezado}>
        <div>
          <p className={styles.preTitulo}>Centro de operación RF</p>
          <h1 className={styles.titulo}>Wireless HeatMapper</h1>
          <p className={styles.subtitulo}>
            Seguimiento operativo de relevamientos WiFi, técnicos, clientes y publicación de resultados.
          </p>
        </div>
        <Button onClick={() => navigate("/admin/proyectos")}>
          <ClipboardList size={15} aria-hidden="true" /> Ver proyectos RF
        </Button>
      </header>

      <section className={styles.metricas} aria-label="Resumen operativo">
        <article className={styles.metrica}>
          <ClipboardList size={20} aria-hidden="true" />
          <span>Proyectos activos</span>
          <strong>{resumen.proyectosActivos}</strong>
        </article>
        <article className={styles.metrica}>
          <AlertTriangle size={20} aria-hidden="true" />
          <span>Sin cliente</span>
          <strong>{resumen.sinCliente}</strong>
        </article>
        <article className={styles.metrica}>
          <RadioTower size={20} aria-hidden="true" />
          <span>Puntos WiFi</span>
          <strong>{resumen.puntosCapturados}</strong>
        </article>
        <article className={styles.metrica}>
          <Activity size={20} aria-hidden="true" />
          <span>Con mediciones RF</span>
          <strong>{resumen.proyectosConDatos}</strong>
        </article>
        <article className={styles.metrica}>
          <CheckCircle2 size={20} aria-hidden="true" />
          <span>Listos para entrega</span>
          <strong>{resumen.completados}</strong>
        </article>
      </section>

      <section className={styles.alertas} aria-label="Alertas operativas">
        <article>
          <AlertTriangle size={18} aria-hidden="true" />
          <span>
            <strong>{resumen.pendientesMedicion} proyecto(s) sin mediciones RF</strong>
            <small>Los técnicos deben capturar puntos desde la app móvil en línea.</small>
          </span>
        </article>
        <article>
          <Building2 size={18} aria-hidden="true" />
          <span>
            <strong>{resumen.sinCliente} proyecto(s) requieren cliente</strong>
            <small>Asignar cliente permite preparar la publicación posterior.</small>
          </span>
        </article>
        <article>
          <Users size={18} aria-hidden="true" />
          <span>
            <strong>{resumen.tecnicos} técnico(s) activo(s)</strong>
            <small>{resumen.clientes} cliente(s) disponibles para nuevos proyectos RF.</small>
          </span>
        </article>
      </section>

      <div className={styles.grilla}>
        <section className={styles.panel}>
          <div className={styles.panelHeader}>
            <div>
              <h2>Seguimiento de relevamientos</h2>
              <p>Proyectos ordenados por actividad reciente y etapa operativa.</p>
            </div>
            <Button variante="ghost" tamano="sm" onClick={() => navigate("/admin/proyectos")}>
              Ver todos <ArrowRight size={14} aria-hidden="true" />
            </Button>
          </div>

          {isLoading ? (
            <div className={styles.listaSkeleton}>
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className={styles.skeleton} />
              ))}
            </div>
          ) : isError ? (
            <EmptyState mensaje="No se pudo cargar el resumen de proyectos." />
          ) : resumen.recientes.length === 0 ? (
            <EmptyState mensaje="No hay relevamientos registrados aún." />
          ) : (
            <div className={styles.listaRecientes}>
              <div className={styles.cabeceraTabla} aria-hidden="true">
                <span>Proyecto</span>
                <span>Etapa</span>
                <span>Datos RF</span>
                <span>Actividad</span>
                <span />
              </div>
              {resumen.recientes.map((proyecto) => (
                <div key={proyecto.id} className={styles.itemReciente}>
                  <div>
                    <strong>{proyecto.nombre}</strong>
                    <small>{proyecto.cliente?.nombre ?? "Sin cliente"} · {proyecto.tecnico.nombre}</small>
                  </div>
                  <span className={styles.etapa}>
                    {etapaOperativa(proyecto)}
                    <small>{etiquetaEstado(proyecto.estado)}</small>
                  </span>
                  <span className={styles.puntos}>{proyecto.cantidad_puntos} puntos</span>
                  <span className={styles.fechaActividad}>
                    <Clock3 size={14} aria-hidden="true" />
                    {formatearFecha(proyecto.ultima_actividad)}
                  </span>
                  <Button
                    variante="secondary"
                    tamano="sm"
                    onClick={() =>
                      navigate(`/admin/proyectos/${proyecto.id}/rf`, {
                        state: { proyectoNombre: proyecto.nombre },
                      })
                    }
                  >
                    Ver RF <ArrowRight size={13} aria-hidden="true" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className={styles.panel}>
          <div className={styles.panelHeader}>
            <div>
              <h2>Gestión operativa</h2>
              <p>Entrada directa al flujo principal del sistema.</p>
            </div>
          </div>
          <div className={styles.acciones}>
            <button type="button" onClick={() => navigate("/admin/proyectos")}>
              <ClipboardList size={18} aria-hidden="true" />
              <span>
                <strong>Proyectos RF</strong>
                <small>Datos relevados, escenarios IA y publicación al cliente.</small>
              </span>
            </button>
            <button type="button" onClick={() => navigate("/admin/proyectos")}>
              <Link2 size={18} aria-hidden="true" />
              <span>
                <strong>Publicación cliente</strong>
                <small>Selección explícita de resultados visibles por enlace.</small>
              </span>
            </button>
            <button type="button" onClick={() => navigate("/admin/usuarios")}>
              <Users size={18} aria-hidden="true" />
              <span>
                <strong>Técnicos y administradores</strong>
                <small>Cuentas que operan la plataforma.</small>
              </span>
            </button>
            <button type="button" onClick={() => navigate("/admin/clientes")}>
              <Building2 size={18} aria-hidden="true" />
              <span>
                <strong>Clientes</strong>
                <small>Organizaciones receptoras del relevamiento.</small>
              </span>
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}
