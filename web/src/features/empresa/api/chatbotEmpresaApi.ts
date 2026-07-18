import axios from "axios";

interface ChatbotEmpresaRespuesta {
  respuesta: string;
  origen: "azure_openai";
}

const empresaClient = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

export async function consultarChatbotEmpresa(pregunta: string): Promise<ChatbotEmpresaRespuesta> {
  const { data } = await empresaClient.post<ChatbotEmpresaRespuesta>("/empresa/chatbot", { pregunta });
  return data;
}
