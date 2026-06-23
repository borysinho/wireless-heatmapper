/**
 * Hook de autenticación admin (Zustand).
 * Sp1-08 — PB-09 / PB-13.
 */

import { create } from "zustand";
import { login as apiLogin, logout as apiLogout } from "../api/authApi";
import type { AuthState, UsuarioOut } from "../types";
import { STORAGE_ACCESS, STORAGE_REFRESH } from "@/shared/api/client";

const MENSAJE_SOLO_ADMIN =
  "Solo usuarios administradores pueden ingresar al panel web.";

interface AuthStore extends AuthState {
  iniciarSesion: (email: string, password: string) => Promise<void>;
  cerrarSesion: () => Promise<void>;
  /** Carga el usuario desde localStorage si hay un token activo. */
  cargarSesion: () => void;
}

export const useAuth = create<AuthStore>((set) => ({
  usuario: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  cargarSesion: () => {
    // El token existe: se verifica mediante el interceptor en la primera petición
    // Para el usuario, no hay un endpoint /me en Sprint 1 — se carga desde localStorage
    const raw = localStorage.getItem("usuario");
    const tieneToken = !!localStorage.getItem(STORAGE_REFRESH);
    if (raw && tieneToken) {
      try {
        const usuario: UsuarioOut = JSON.parse(raw);
        if (usuario.rol !== "admin") {
          _limpiarSesionWeb();
          set({ usuario: null, isAuthenticated: false });
          return;
        }
        set({ usuario, isAuthenticated: true });
      } catch {
        _limpiarSesionWeb();
      }
    } else if (raw && !tieneToken) {
      // Sesión inconsistente: hay perfil guardado pero los tokens expiraron o
      // fueron eliminados. Limpiar para evitar el bucle login ↔ usuarios.
      _limpiarSesionWeb();
    }
  },

  iniciarSesion: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const data = await apiLogin({ email, password });
      if (data.usuario.rol !== "admin") {
        _limpiarSesionWeb();
        set({
          usuario: null,
          isAuthenticated: false,
          isLoading: false,
          error: MENSAJE_SOLO_ADMIN,
        });
        throw new Error(MENSAJE_SOLO_ADMIN);
      }
      localStorage.setItem("usuario", JSON.stringify(data.usuario));
      set({
        usuario: data.usuario,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (err: unknown) {
      const mensaje = _extraerMensajeError(err);
      set({ isLoading: false, error: mensaje, isAuthenticated: false });
      throw err;
    }
  },

  cerrarSesion: async () => {
    const refreshToken = localStorage.getItem(STORAGE_REFRESH) ?? "";
    try {
      if (refreshToken) await apiLogout(refreshToken);
    } finally {
      _limpiarSesionWeb();
      set({ usuario: null, isAuthenticated: false, error: null });
    }
  },
}));

function _limpiarSesionWeb() {
  localStorage.removeItem(STORAGE_ACCESS);
  localStorage.removeItem(STORAGE_REFRESH);
  localStorage.removeItem("usuario");
}

function _extraerMensajeError(err: unknown): string {
  if (
    typeof err === "object" &&
    err !== null &&
    "response" in err &&
    typeof (err as { response?: { data?: { detail?: string } } }).response?.data
      ?.detail === "string"
  ) {
    return (err as { response: { data: { detail: string } } }).response.data
      .detail;
  }
  if (err instanceof Error && err.message === MENSAJE_SOLO_ADMIN) {
    return MENSAJE_SOLO_ADMIN;
  }
  return "Error al iniciar sesión. Verifique su conexión e intente nuevamente.";
}
