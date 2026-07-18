import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import SitioEmpresa from "./SitioEmpresa";

describe("SitioEmpresa", () => {
  it("muestra identidad empresarial, producto, contacto y recursos oficiales", () => {
    render(<SitioEmpresa />);

    expect(screen.getByRole("heading", { name: /soluciones de software técnico/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Wireless HeatMapper" })).toBeInTheDocument();
    expect(screen.getByText("borysquiroga@gmail.com")).toBeInTheDocument();
    expect(screen.getByText("+891-77685777")).toBeInTheDocument();
    expect(screen.getByText(/LinkedIn · pendiente/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /abrir manual/i })).toHaveAttribute("href", "/manual/");
    expect(screen.getByRole("heading", { name: "APK Android" })).toBeInTheDocument();
  });

  it("responde preguntas frecuentes desde la base local del chatbot", async () => {
    const usuario = userEvent.setup();

    render(<SitioEmpresa />);
    await usuario.click(screen.getByRole("button", { name: /¿Qué significa RSSI < -90 dBm/i }));

    expect(screen.getByText(/RSSI menor a -90 dBm se interpreta como zona muerta/i)).toBeInTheDocument();
  });
});
