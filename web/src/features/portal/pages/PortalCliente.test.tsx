import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import type { MapaCalorPortalOut, PortalClienteOut } from "@/features/admin/types";
import PortalCliente from "./PortalCliente";

vi.mock("@tanstack/react-query", () => ({ useQuery: vi.fn() }));
vi.mock("react-router-dom", () => ({ useParams: vi.fn() }));

const portal: PortalClienteOut = {
  proyecto: {
    id: 1,
    nombre: "Cobertura oficinas Bulldog",
    cliente: "Bulldog Tech.",
    descripcion: null,
  },
  planos: [
    {
      id: 2,
      proyecto_id: 1,
      nombre: "Planta alta",
      descripcion: null,
      formato: "png",
      ancho_px: 1000,
      alto_px: 700,
      tamano_bytes: 1024,
      url_firmada: "/planos/planta-alta.png",
      calibrado: true,
      cantidad_puntos: 8,
      escala_m_por_px: null,
      distancia_real_m: null,
      created_at: "2026-06-20T10:00:00Z",
      updated_at: "2026-06-20T10:00:00Z",
    },
  ],
  conjuntos: [
    {
      id: 10,
      plano_id: 2,
      conjunto_origen_id: null,
      nombre: "APs planta alta",
      proposito: "Validar cobertura del área administrativa",
      descripcion: "Selección compartida por Bulldog Tech.",
      es_principal: true,
      banda_objetivo: "5",
      origen: "manual_web",
      creado_por_id: 3,
      resumen_ia: null,
      metricas_ia: null,
      restricciones_ia: null,
      version_motor_ia: null,
      cantidad_aps: 1,
      items: [
        {
          bssid: "aa:bb:cc:dd:ee:01",
          ssid: "Bulldog-Admin",
          canal: 44,
          frecuencia_mhz: 5220,
          rssi_promedio: -62,
          pos_x: 120,
          pos_y: 80,
          cantidad_puntos: 8,
          accion_recomendada: null,
          justificacion: null,
          altura_m: null,
          tipo_montaje: null,
          banda: null,
          modelo_ap: null,
          costo_estimado: null,
          radios: null,
        },
      ],
      created_at: "2026-06-20T10:00:00Z",
      updated_at: "2026-06-20T10:00:00Z",
    },
  ],
  heatmaps: [],
};

const mapaPortal: MapaCalorPortalOut = {
  id: 30,
  plano_id: 2,
  conjunto_ap_id: 10,
  modo_generacion: "CONJUNTO_COMPLETO",
  algoritmo: "IDW",
  resolucion: 64,
  bssid: "aa:bb:cc:dd:ee:01",
  ssid: "Bulldog-Admin",
  ap_pos_x: 120,
  ap_pos_y: 80,
  aps_interes: [
    {
      bssid: "aa:bb:cc:dd:ee:01",
      ssid: "Bulldog-Admin",
      canal: 44,
      frecuencia_mhz: 5220,
      rssi_promedio: -62,
      pos_x: 120,
      pos_y: 80,
      cantidad_puntos: 8,
      seleccionado: true,
    },
  ],
  bssids_generacion: ["aa:bb:cc:dd:ee:01"],
  url_imagen: "/heatmaps/planta-alta.png",
  matriz: [[-62, -64], [-68, -72]],
  escala: [{ desde: -70, hasta: -30, color: "#A7E84A", etiqueta: "Óptimo" }],
  cantidad_puntos: 1,
  rssi_min: -72,
  rssi_max: -62,
  rssi_promedio: -66,
  puntos_lectura: [
    {
      punto_id: 7,
      pos_x: 220,
      pos_y: 160,
      rssi: -62,
      total_lecturas: 1,
      detalle_aps: [],
    },
  ],
  poligono_interes: [],
  advertencias: [],
  created_at: "2026-06-20T10:05:00Z",
};

describe("PortalCliente", () => {
  it("muestra el detalle del contenido publicado", () => {
    vi.mocked(useParams).mockReturnValue({ token: "token-publico" });
    vi.mocked(useQuery).mockReturnValue({
      data: portal,
      isLoading: false,
      isError: false,
    } as ReturnType<typeof useQuery>);
    render(<PortalCliente />);

    expect(screen.getByRole("heading", { name: "Áreas de análisis" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "Contenido publicado" })).toBeVisible();
    expect(screen.getByText("Planta alta")).toBeVisible();
    expect(screen.getByRole("button", { name: /APs planta alta/i })).toBeVisible();
    expect(screen.getByText("No hay mapas de calor compartidos para este contenido.")).toBeVisible();
    expect(screen.queryByRole("button", { name: /Generar heatmap/i })).toBeNull();
    expect(screen.queryByRole("heading", { name: "Datos reales relevados en sitio" })).toBeNull();
    expect(screen.queryByRole("heading", { name: "Propuestas IA" })).toBeNull();
  });

  it("mantiene el tamaño visual de los APs al acercar el mapa", async () => {
    vi.mocked(useParams).mockReturnValue({ token: "token-publico" });
    vi.mocked(useQuery).mockReturnValue({
      data: { ...portal, heatmaps: [mapaPortal] },
      isLoading: false,
      isError: false,
    } as ReturnType<typeof useQuery>);
    const { container } = render(<PortalCliente />);

    expect(container.querySelectorAll('circle[fill="#A7E84A"]').length).toBe(1);
    fireEvent.click(screen.getByRole("button", { name: "Acercar mapa" }));

    await waitFor(() => {
      expect(screen.getByRole("button", { name: /AP 1: Bulldog-Admin/i })).toHaveStyle({
        transform: "translate(-50%, -50%) scale(0.8333333333333334)",
      });
    });
  });

  it("permite arrastrar el mapa después de acercarlo", async () => {
    vi.mocked(useParams).mockReturnValue({ token: "token-publico" });
    vi.mocked(useQuery).mockReturnValue({
      data: { ...portal, heatmaps: [mapaPortal] },
      isLoading: false,
      isError: false,
    } as ReturnType<typeof useQuery>);
    render(<PortalCliente />);

    const visor = screen.getByRole("region", { name: "Mapa de calor interactivo" });
    vi.spyOn(visor, "getBoundingClientRect").mockReturnValue({
      x: 0,
      y: 0,
      top: 0,
      left: 0,
      right: 1000,
      bottom: 700,
      width: 1000,
      height: 700,
      toJSON: () => undefined,
    });

    fireEvent.click(screen.getByRole("button", { name: "Acercar mapa" }));
    await waitFor(() => expect(screen.getByText("120%")).toBeVisible());

    dispararPointer(visor, "pointerdown", { button: 0, clientX: 500, clientY: 350, pointerId: 1 });
    dispararPointer(visor, "pointermove", { clientX: 400, clientY: 280, pointerId: 1 });
    dispararPointer(visor, "pointerup", { clientX: 400, clientY: 280, pointerId: 1 });

    await waitFor(() => {
      expect(screen.getByAltText("Heatmap generado").parentElement).toHaveStyle({
        transform: "translate(-100px, -70px) scale(1.2)",
      });
    });
  });

  it("incluye puntos de lectura al exportar el mapa como PNG", async () => {
    const contexto = {
      beginPath: vi.fn(),
      arc: vi.fn(),
      fill: vi.fn(),
      fillRect: vi.fn(),
      restore: vi.fn(),
      save: vi.fn(),
      stroke: vi.fn(),
      drawImage: vi.fn(),
      fillText: vi.fn(),
      fillStyle: "",
      font: "",
      globalAlpha: 1,
      lineWidth: 1,
      strokeStyle: "",
      textAlign: "start",
      textBaseline: "alphabetic",
    } as unknown as CanvasRenderingContext2D;
    const getContext = vi
      .spyOn(HTMLCanvasElement.prototype, "getContext")
      .mockReturnValue(contexto);
    const toBlob = vi
      .spyOn(HTMLCanvasElement.prototype, "toBlob")
      .mockImplementation((callback) => callback(new Blob(["png"], { type: "image/png" })));
    const clickEnlace = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => {});
    Object.defineProperty(URL, "createObjectURL", {
      configurable: true,
      value: vi.fn(() => "blob:portal-exportacion"),
    });
    Object.defineProperty(URL, "revokeObjectURL", {
      configurable: true,
      value: vi.fn(),
    });
    const ImagenOriginal = globalThis.Image;

    class ImagenMock {
      crossOrigin = "";
      onerror: (() => void) | null = null;
      onload: (() => void) | null = null;

      set src(_valor: string) {
        queueMicrotask(() => this.onload?.());
      }
    }

    vi.stubGlobal("Image", ImagenMock);

    try {
      vi.mocked(useParams).mockReturnValue({ token: "token-publico" });
      vi.mocked(useQuery).mockReturnValue({
        data: { ...portal, heatmaps: [mapaPortal] },
        isLoading: false,
        isError: false,
      } as ReturnType<typeof useQuery>);
      render(<PortalCliente />);

      fireEvent.click(screen.getByRole("button", { name: "Mapa" }));
      await waitFor(() => {
        expect(contexto.arc).toHaveBeenCalledWith(220, 160, expect.any(Number), 0, Math.PI * 2);
      });
    } finally {
      vi.stubGlobal("Image", ImagenOriginal);
      getContext.mockRestore();
      toBlob.mockRestore();
      clickEnlace.mockRestore();
      Reflect.deleteProperty(URL, "createObjectURL");
      Reflect.deleteProperty(URL, "revokeObjectURL");
    }

    expect(contexto.fill).toHaveBeenCalled();
    expect(contexto.stroke).toHaveBeenCalled();
  });
});

function dispararPointer(
  elemento: Element,
  tipo: "pointerdown" | "pointermove" | "pointerup",
  datos: Record<string, number>,
) {
  const evento = new Event(tipo, { bubbles: true, cancelable: true });
  Object.assign(evento, datos);
  fireEvent(elemento, evento);
}
