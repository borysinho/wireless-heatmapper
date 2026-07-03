/** Tipos TypeScript para el módulo admin. Sprint 1 — PB-13, PB-18, PB-19. */

export interface UsuarioOut {
  id: number;
  nombre: string;
  email: string;
  rol: "admin" | "tecnico";
  activo: boolean;
  created_at: string;
}

export interface UsuarioCreate {
  nombre: string;
  email: string;
  password: string;
  rol: "admin" | "tecnico";
}

export interface UsuarioUpdate {
  nombre?: string;
  email?: string;
  rol?: "admin" | "tecnico";
  activo?: boolean;
  password?: string;
}

export interface ClienteBasicoOut {
  id: number;
  nombre: string;
  email_referencia: string | null;
}

export interface ClienteOut {
  id: number;
  nombre: string;
  email_referencia: string | null;
  activo: boolean;
  created_at: string;
}

export interface ClienteCreate {
  nombre: string;
  email_referencia?: string | null;
}

export interface ClienteUpdate {
  nombre?: string;
  email_referencia?: string | null;
  activo?: boolean;
}

export interface TecnicoBasicoOut {
  id: number;
  nombre: string;
  email: string;
}

export interface ProyectoListOut {
  id: number;
  nombre: string;
  descripcion: string | null;
  cliente: ClienteBasicoOut | null;
  estado: "nuevo" | "en_progreso" | "completado" | "archivado";
  ultima_actividad: string;
  cantidad_puntos: number;
  tecnico: TecnicoBasicoOut;
  tecnicos: TecnicoBasicoOut[];
  created_at: string;
}

export interface ProyectosPageOut {
  items: ProyectoListOut[];
  total: number;
  page: number;
  page_size: number;
}

export interface ProyectosFilter {
  tecnico_id?: number;
  estado?: string;
  fecha_desde?: string;
  fecha_hasta?: string;
}

export interface ProyectoReasignarIn {
  tecnico_id: number;
}

export interface ProyectoAdminCreate {
  nombre: string;
  descripcion?: string | null;
  cliente_id?: number | null;
  tecnico_id: number;
  tecnico_ids?: number[];
  estado: "nuevo" | "en_progreso" | "completado" | "archivado";
}

export type ProyectoAdminUpdate = Partial<ProyectoAdminCreate>;

export interface PlanoOut {
  id: number;
  proyecto_id: number;
  nombre: string;
  descripcion: string | null;
  formato: "png" | "jpg" | "pdf";
  ancho_px: number;
  alto_px: number;
  tamano_bytes: number;
  url_firmada: string;
  calibrado: boolean;
  cantidad_puntos: number;
  escala_m_por_px: number | null;
  distancia_real_m: number | null;
  created_at: string;
  updated_at: string;
}

export interface APDisponibleOut {
  bssid: string;
  ssid: string;
  canal: number | null;
  frecuencia_mhz: number | null;
  rssi_promedio: number;
  pos_x: number;
  pos_y: number;
  cantidad_puntos: number;
  seleccionado: boolean;
}

export interface ConjuntoAPItemOut {
  bssid: string;
  ssid: string;
  canal: number | null;
  frecuencia_mhz: number | null;
  rssi_promedio: number | null;
  pos_x: number | null;
  pos_y: number | null;
  cantidad_puntos: number | null;
  accion_recomendada: string | null;
  justificacion: string | null;
  altura_m: number | null;
  tipo_montaje: string | null;
  banda: string | null;
  modelo_ap: string | null;
  costo_estimado: number | null;
  radios: Array<Record<string, unknown>> | null;
}

export interface ConjuntoAPOut {
  id: number;
  plano_id: number;
  conjunto_origen_id: number | null;
  nombre: string;
  proposito: string;
  descripcion: string | null;
  es_principal: boolean;
  banda_objetivo: "2.4" | "5" | string;
  origen: "manual_movil" | "manual_web" | "ia" | string;
  creado_por_id: number | null;
  resumen_ia: string | null;
  metricas_ia: Record<string, unknown> | null;
  restricciones_ia: Record<string, unknown> | null;
  version_motor_ia: string | null;
  cantidad_aps: number;
  items: ConjuntoAPItemOut[];
  created_at: string;
  updated_at: string;
}

export interface LecturaSimuladaIA {
  punto_medicion_id: number;
  pos_x: number;
  pos_y: number;
  banda: "2.4" | "5" | string;
  rssi_observado_dbm: number | null;
  rssi_proyectado_dbm: number;
  diferencia_db: number | null;
  radio_primaria: string;
  radio_secundaria: string | null;
  rssi_secundario_dbm: number | null;
  snr_proyectado_db: number | null;
  incertidumbre_db: number;
}

export interface FuenteEntradaIAIn {
  tipo: "CONJUNTO_EXISTENTE";
  conjunto_id: number;
}

export interface RestriccionesIAIn {
  plano_id?: number;
  fuente_entrada: FuenteEntradaIAIn;
  umbral_objetivo_dbm: number;
  resolucion: number;
  cantidad_aps_propuestos: number;
  cantidad_recomendaciones: number;
}

export interface ConjuntosIAGeneradosOut {
  conjunto_base_id: number;
  mapa_actual: MapaCalorResumenOut;
  conjuntos: ConjuntoAPOut[];
  mapas_proyectados: MapaCalorResumenOut[];
}

export interface PreparacionIAOut {
  plano_id: number;
  conjunto_id: number;
  mapa_actual_id: number;
  cantidad_puntos: number;
  preparado: boolean;
}

export interface ContenidoEnlaceIn {
  conjunto_ids?: number[];
  mapa_ids?: number[];
}

export interface EnlaceClienteOut {
  id: number;
  proyecto_id: number;
  url_publica: string;
  expira_en: string;
  revocado: boolean;
  accesos: number;
  ultimo_acceso: string | null;
  ip_ultimo_acceso: string | null;
  contenido: Required<ContenidoEnlaceIn>;
  created_at: string;
}

export interface EnlaceClienteCrearIn {
  expira_en_dias: number;
  contenido: ContenidoEnlaceIn;
  cliente_id?: number | null;
}

export interface EnlaceClienteEnviarCorreoIn {
  cliente_id: number;
}

export interface EnlaceClienteEnviarCorreoOut {
  enlace_id: number;
  destinatario: string;
  enviado: boolean;
}

export interface PortalProyectoOut {
  id: number;
  nombre: string;
  cliente: string | null;
  descripcion: string | null;
}

export interface MapaCalorPortalOut {
  id: number;
  plano_id: number;
  conjunto_ap_id: number | null;
  modo_generacion: string;
  algoritmo: string;
  resolucion: number;
  bssid: string;
  ssid: string;
  ap_pos_x: number;
  ap_pos_y: number;
  aps_interes: APDisponibleOut[];
  bssids_generacion: string[];
  url_imagen: string;
  matriz: number[][];
  escala: Array<{ desde: number; hasta: number; color: string; etiqueta: string }>;
  cantidad_puntos: number;
  rssi_min: number;
  rssi_max: number;
  rssi_promedio: number;
  puntos_lectura: Array<{
    punto_id: number;
    pos_x: number;
    pos_y: number;
    rssi: number;
    total_lecturas?: number;
    detalle_aps?: Array<{
      bssid: string;
      ssid: string | null;
      total_lecturas: number;
      lecturas_perdidas: number;
      rssi_promedio: number | null;
    }>;
  }>;
  poligono_interes: Array<{ x: number; y: number }>;
  advertencias: string[];
  created_at: string;
}

export type MapaCalorOut = MapaCalorPortalOut;

export interface MapaCalorResumenOut {
  id: number;
  plano_id: number;
  conjunto_ap_id: number | null;
  modo_generacion: string;
  algoritmo: string;
  resolucion: number;
  bssid: string;
  ssid: string;
  aps_interes: APDisponibleOut[];
  bssids_generacion: string[];
  url_imagen: string;
  cantidad_puntos: number;
  rssi_min: number;
  rssi_max: number;
  rssi_promedio: number;
  created_at: string;
}

export interface PortalClienteOut {
  proyecto: PortalProyectoOut;
  planos: PlanoOut[];
  conjuntos: ConjuntoAPOut[];
  heatmaps: MapaCalorPortalOut[];
}
