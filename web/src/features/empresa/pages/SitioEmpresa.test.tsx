import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import SitioEmpresa from "./SitioEmpresa";
import { consultarChatbotEmpresa } from "../api/chatbotEmpresaApi";

vi.mock("../api/chatbotEmpresaApi", () => ({
  consultarChatbotEmpresa: vi.fn(),
}));

const consultarChatbotEmpresaMock = vi.mocked(consultarChatbotEmpresa);

describe("SitioEmpresa", () => {
  beforeEach(() => {
    consultarChatbotEmpresaMock.mockReset();
  });

  it("muestra identidad empresarial, producto, contacto y recursos oficiales", () => {
    render(<SitioEmpresa />);

    expect(screen.getByRole("heading", { name: /soluciones de software técnico/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Wireless HeatMapper" })).toBeInTheDocument();
    expect(screen.getByText("borysquiroga@gmail.com")).toBeInTheDocument();
    expect(screen.getByText("+591-77685777")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /facebook oficial/i })).toHaveAttribute(
      "href",
      "https://www.facebook.com/profile.php?id=61591962512748",
    );
    expect(screen.queryByText(/LinkedIn|Instagram|YouTube/i)).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: /abrir manual/i })).toHaveAttribute("href", "/manual/");
    expect(screen.getByRole("heading", { name: "APK Android" })).toBeInTheDocument();
  });

  it("consulta el chatbot empresarial mediante el endpoint Azure", async () => {
    const usuario = userEvent.setup();
    consultarChatbotEmpresaMock.mockResolvedValue({
      respuesta: "Respuesta generada por Azure OpenAI para Wireless HeatMapper.",
      origen: "azure_openai",
    });

    render(<SitioEmpresa />);
    await usuario.click(screen.getByRole("button", { name: /¿Qué significa RSSI < -90 dBm/i }));

    expect(consultarChatbotEmpresaMock).toHaveBeenCalledWith("¿Qué significa RSSI < -90 dBm?");
    expect(await screen.findByText(/Respuesta generada por Azure OpenAI/i)).toBeInTheDocument();
    expect(screen.getByText("Respuesta generada con Azure OpenAI")).toBeInTheDocument();
  });

  it("usa la respuesta local aprobada cuando Azure no responde", async () => {
    const usuario = userEvent.setup();
    consultarChatbotEmpresaMock.mockRejectedValue(new Error("sin conexión"));

    render(<SitioEmpresa />);
    await usuario.type(screen.getByLabelText("Consulta breve"), "¿Qué significa RSSI < -90 dBm?");
    await usuario.click(screen.getByRole("button", { name: /consultar/i }));

    expect(await screen.findByText(/RSSI menor a -90 dBm se interpreta como zona muerta/i)).toBeInTheDocument();
    expect(screen.getByText(/No se pudo consultar la IA/i)).toBeInTheDocument();
  });
});
