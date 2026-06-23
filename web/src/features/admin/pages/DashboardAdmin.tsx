import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  Activity,
  ArrowRight,
  Building2,
  ClipboardList,
  Plus,
  RadioTower,
  Users,
} from "lucide-react";
import { Button, EmptyState } from "@/shared/components";
import { useClientes } from "../hooks/useClientes";
import { useProyectosOrg } from "../hooks/useProyectosOrg";
import { useUsuarios } from "../hooks/useUsuarios";
import styles from "./DashboardAdmin.module.css";

export default function DashboardAdmin() {
  const navigate = useNavigate();
  const { data: proyectos, isLoading, isError } = useProyectosOrg(1, 100);
  const { data: usuarios } = useUsuarios();
  const { data: clientes } = useClientes();

  const resumen = useMemo(() => {
    const items = proyectos?.items ?? [];
    return {
      totalProyectos: proyectos?.total ?? 0,
      proyectosActivos: items.filter((p) => p.estado === "nuevo" || p.estado === "en_progreso").length,
      puntosCapturados: items.reduce((total, p) => total + p.cantidad_puntos, 0),
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
          <Plus size={15} aria-hidden="true" /> Nuevo relevamiento
        </Button>
      </header>

      <section className={styles.metricas} aria-label="Resumen operativo">
        <article className={styles.metrica}>
          <ClipboardList size={20} aria-hidden="true" />
          <span>Proyectos</span>
          <strong>{resumen.totalProyectos}</strong>
        </article>
        <article className={styles.metrica}>
          <Activity size={20} aria-hidden="true" />
          <span>Activos</span>
          <strong>{resumen.proyectosActivos}</strong>
        </article>
        <article className={styles.metrica}>
          <RadioTower size={20} aria-hidden="true" />
          <span>Puntos WiFi</span>
          <strong>{resumen.puntosCapturados}</strong>
        </article>
        <article className={styles.metrica}>
          <Users size={20} aria-hidden="true" />
          <span>Técnicos</span>
          <strong>{resumen.tecnicos}</strong>
        </article>
        <article className={styles.metrica}>
          <Building2 size={20} aria-hidden="true" />
          <span>Clientes</span>
          <strong>{resumen.clientes}</strong>
        </article>
      </section>

      <div className={styles.grilla}>
        <section className={styles.panel}>
          <div className={styles.panelHeader}>
            <div>
              <h2>Relevamientos recientes</h2>
              <p>Proyectos con actividad registrada en la organización.</p>
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
              {resumen.recientes.map((proyecto) => (
                <button
                  key={proyecto.id}
                  type="button"
                  className={styles.itemReciente}
                  onClick={() =>
                    navigate(`/admin/proyectos/${proyecto.id}/rf`, {
                      state: { proyectoNombre: proyecto.nombre },
                    })
                  }
                >
                  <span>
                    <strong>{proyecto.nombre}</strong>
                    <small>{proyecto.cliente?.nombre ?? "Sin cliente"} · {proyecto.tecnico.nombre}</small>
                  </span>
                  <span className={styles.puntos}>{proyecto.cantidad_puntos} puntos</span>
                </button>
              ))}
            </div>
          )}
        </section>

        <section className={styles.panel}>
          <div className={styles.panelHeader}>
            <div>
              <h2>Accesos de operación</h2>
              <p>Entrada directa al flujo principal del sistema.</p>
            </div>
          </div>
          <div className={styles.acciones}>
            <button type="button" onClick={() => navigate("/admin/proyectos")}>
              <ClipboardList size={18} aria-hidden="true" />
              <span>
                <strong>Pipeline de proyectos</strong>
                <small>Asignación, estado y actividad RF.</small>
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
