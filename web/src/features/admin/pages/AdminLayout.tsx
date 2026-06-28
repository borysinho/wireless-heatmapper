/**
 * Layout del panel admin con navegación lateral responsive.
 * Protege rutas admin — redirige a login si no hay sesión admin.
 * Sprint 1 — PB-13, PB-18.
 */

import { useEffect, useState } from "react";
import { NavLink, Outlet, useNavigate, useLocation } from "react-router-dom";
import {
  Radio,
  Users,
  Building2,
  ClipboardList,
  LogOut,
  Menu,
  X,
  LayoutDashboard,
} from "lucide-react";
import { useAuth } from "@/features/auth/hooks/useAuth";
import { ToastContainer } from "@/shared/components";
import styles from "./AdminLayout.module.css";

const GRUPOS_NAV = [
  {
    titulo: "Centro RF",
    items: [
      { to: "/admin/inicio", etiqueta: "Inicio", Icono: LayoutDashboard },
    ],
  },
  {
    titulo: "Operación RF",
    items: [
      { to: "/admin/proyectos", etiqueta: "Proyectos RF", Icono: ClipboardList },
    ],
  },
  {
    titulo: "Administración",
    items: [
      { to: "/admin/usuarios", etiqueta: "Usuarios", Icono: Users },
      { to: "/admin/clientes", etiqueta: "Clientes", Icono: Building2 },
    ],
  },
];

function iniciales(nombre: string): string {
  return nombre
    .split(" ")
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase() ?? "")
    .join("");
}

export default function AdminLayout() {
  const { isAuthenticated, usuario, cerrarSesion, cargarSesion } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  // El drawer se abre "en" un pathname específico; si el pathname cambia, queda cerrado.
  const [menuAbiertoEn, setMenuAbiertoEn] = useState<string | null>(null);
  const menuAbierto = menuAbiertoEn === location.pathname;

  useEffect(() => {
    cargarSesion();
  }, [cargarSesion]);

  useEffect(() => {
    if (isAuthenticated && usuario?.rol !== "admin") {
      void cerrarSesion().finally(() => {
        navigate("/admin/login", { replace: true });
      });
      return;
    }

    if (!isAuthenticated) {
      const timer = setTimeout(() => {
        if (!useAuth.getState().isAuthenticated) {
          navigate("/admin/login", { replace: true });
        }
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [cerrarSesion, isAuthenticated, navigate, usuario?.rol]);

  const handleLogout = async () => {
    await cerrarSesion();
    navigate("/admin/login", { replace: true });
  };

  if (!isAuthenticated || usuario?.rol !== "admin") return null;

  const sidebar = (
    <nav className={styles.nav} aria-label="Navegación principal">
      <div className={styles.marca}>
        <Radio size={20} aria-hidden="true" />
        <span>HeatMapper Admin</span>
      </div>

      <ul className={styles.menu} role="list">
        {GRUPOS_NAV.map((grupo) => (
          <li key={grupo.titulo} className={styles.grupoNav}>
            <span className={styles.tituloGrupo}>{grupo.titulo}</span>
            <ul className={styles.submenu} role="list">
              {grupo.items.map(({ to, etiqueta, Icono }) => (
                <li key={to}>
                  <NavLink
                    to={to}
                    className={({ isActive }) =>
                      isActive ? `${styles.enlace} ${styles.activo}` : styles.enlace
                    }
                  >
                    <Icono size={16} aria-hidden="true" />
                    {etiqueta}
                  </NavLink>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>

      <div className={styles.perfil}>
        <div className={styles.avatar} aria-hidden="true">
          {iniciales(usuario?.nombre ?? "A")}
        </div>
        <span className={styles.nombreUsuario}>
          {usuario?.nombre ?? "Admin"}
        </span>
        <button
          onClick={handleLogout}
          className={styles.botonSalir}
          aria-label="Cerrar sesión"
        >
          <LogOut size={14} aria-hidden="true" />
          Cerrar sesión
        </button>
      </div>
    </nav>
  );

  return (
    <div className={styles.layout}>
      {/* Botón hamburguesa — visible solo en móvil */}
      <button
        className={styles.triggerMovil}
        onClick={() => setMenuAbiertoEn(location.pathname)}
        aria-label="Abrir menú"
        aria-expanded={menuAbierto}
      >
        <Menu size={22} />
      </button>

      {/* Overlay móvil */}
      {menuAbierto && (
        <div
          className={styles.overlay}
          onClick={() => setMenuAbiertoEn(null)}
          aria-hidden="true"
        />
      )}

      {/* Drawer móvil / Sidebar desktop */}
      <div
        className={`${styles.navWrapper} ${menuAbierto ? styles.navAbierto : ""}`}
      >
        <button
          className={styles.cerrarDrawer}
          onClick={() => setMenuAbiertoEn(null)}
          aria-label="Cerrar menú"
        >
          <X size={20} />
        </button>
        {sidebar}
      </div>

      <main className={styles.contenido}>
        <Outlet />
      </main>

      <ToastContainer />
    </div>
  );
}
