import { useCallback, useMemo, useState } from "react";
import type { FormEvent } from "react";
import {
  ArrowRight,
  Bot,
  Building2,
  CheckCircle2,
  Cloud,
  Code2,
  Download,
  ExternalLink,
  FileText,
  Loader2,
  LockKeyhole,
  Mail,
  MapPin,
  MessageSquare,
  Phone,
  Send,
  ShieldCheck,
  Smartphone,
  Sparkles,
  Users,
  Wifi,
} from "lucide-react";
import styles from "./SitioEmpresa.module.css";
import logoTeam24 from "@/assets/empresa/team-24-software-logo.svg";
import heroEmpresa from "@/assets/empresa/hero-empresa.png";
import productoHeatmapper from "@/assets/empresa/producto-heatmapper.png";
import soporteDevops from "@/assets/empresa/soporte-devops.png";
import { consultarChatbotEmpresa } from "../api/chatbotEmpresaApi";

type Icono = typeof Building2;

interface Servicio {
  titulo: string;
  descripcion: string;
  beneficio: string;
  entregable: string;
  icono: Icono;
}

interface PreguntaChatbot {
  pregunta: string;
  respuesta: string;
}

type EstadoChatbot = "listo" | "consultando" | "respaldo";

const urlPublica = "https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/";
const correoContacto = "borysquiroga@gmail.com";
const telefonoContacto = "+891-77685777";
const whatsappContacto = "https://wa.me/89177685777";
const facebookEmpresa = "https://www.facebook.com/profile.php?id=61591962512748";

const navegacion = [
  ["Empresa", "#empresa"],
  ["Servicios", "#servicios"],
  ["Producto", "#producto"],
  ["Descargas", "#descargas"],
  ["Soporte", "#soporte"],
  ["Contacto", "#contacto"],
  ["Políticas", "#politicas"],
] as const;

const servicios: Servicio[] = [
  {
    titulo: "Desarrollo de software web",
    descripcion: "Sistemas administrativos, portales de cliente, dashboards y aplicaciones SPA.",
    beneficio: "Operación centralizada con interfaces verificables y mantenibles.",
    entregable: "Paneles React, módulos CRUD, reportes y flujos de revisión.",
    icono: Code2,
  },
  {
    titulo: "Desarrollo móvil Android",
    descripcion: "Aplicaciones de campo con cliente delgado, consumo REST y experiencia orientada a técnicos.",
    beneficio: "Registro operativo sin duplicar datos de dominio en el dispositivo.",
    entregable: "APK Android, autenticación, captura guiada y publicación controlada.",
    icono: Smartphone,
  },
  {
    titulo: "Backend y APIs",
    descripcion: "APIs REST con autenticación JWT, persistencia centralizada y documentación OpenAPI.",
    beneficio: "Servicios integrables, auditables y preparados para despliegue en nube.",
    entregable: "FastAPI, PostgreSQL, contratos OpenAPI, pruebas y contenedores.",
    icono: Cloud,
  },
  {
    titulo: "Consultoría WiFi",
    descripcion: "Herramientas para relevamiento, interpretación de RSSI, mapas de calor y evidencia técnica.",
    beneficio: "Decisiones de cobertura basadas en mediciones y trazabilidad.",
    entregable: "Mapas de calor, criterios RSSI, comparación de escenarios y recomendaciones.",
    icono: Wifi,
  },
  {
    titulo: "Analítica e IA aplicada",
    descripcion: "Procesamiento de datos, recomendaciones asistidas y automatización de decisiones técnicas.",
    beneficio: "Priorización de mejoras con resultados comparables y revisables.",
    entregable: "Módulos de recomendación, métricas, validación y reportes técnicos.",
    icono: Sparkles,
  },
  {
    titulo: "DevOps básico y soporte",
    descripcion: "Contenedores, Nginx, HTTPS, CI/CD, respaldos, monitoreo y atención de incidentes.",
    beneficio: "Publicación reproducible y operación con responsabilidades definidas.",
    entregable: "Docker Compose, workflows, guías de despliegue y acuerdos de soporte.",
    icono: ShieldCheck,
  },
];

const beneficiosProducto = [
  "Evidencia centralizada en PostgreSQL mediante backend FastAPI.",
  "Mapas de calor publicados desde mediciones capturadas por técnicos.",
  "Comparación de escenarios técnicos y propuestas asistidas por IA.",
  "Portal de cliente por enlace para supervisión organizacional.",
  "Modalidad 100 % en línea, sin sincronización diferida ni base local de dominio.",
];

const recursos = [
  {
    titulo: "Portal web",
    detalle: "Acceso al panel administrativo y operación publicada.",
    accion: "Ingresar",
    href: "/admin/login",
    disponible: true,
  },
  {
    titulo: "Manual de usuario",
    detalle: "Guía para administrador, técnico de campo y cliente final.",
    accion: "Abrir manual",
    href: "/manual/",
    disponible: true,
  },
  {
    titulo: "API técnica",
    detalle: "Documentación OpenAPI del backend publicado.",
    accion: "Ver API",
    href: "/api/docs",
    disponible: true,
  },
  {
    titulo: "APK Android",
    detalle: "Instalador móvil para técnicos, sujeto a release aprobado.",
    accion: "Pendiente de release",
    href: "",
    disponible: false,
  },
];

const preguntas: PreguntaChatbot[] = [
  {
    pregunta: "¿Qué es Team 24 Software?",
    respuesta:
      "Team 24 Software es el equipo desarrollador del Grupo 24 de Ingeniería de Software II. Construye soluciones web, móviles, backend e IA aplicada con trazabilidad académica y despliegue verificable.",
  },
  {
    pregunta: "¿Qué problema resuelve Wireless HeatMapper?",
    respuesta:
      "Resuelve mediciones WiFi fragmentadas, uso de planos impresos, transcripción manual y baja trazabilidad. Centraliza capturas, planos, mapas de calor y publicación al cliente.",
  },
  {
    pregunta: "¿Cómo ingreso al sistema publicado?",
    respuesta:
      "Desde el sitio público puedes entrar al panel por /admin/login. El portal de cliente se abre mediante enlaces únicos generados para cada proyecto publicado.",
  },
  {
    pregunta: "¿Cuál es la diferencia entre administrador, técnico y cliente?",
    respuesta:
      "El administrador gestiona usuarios, clientes y proyectos. El técnico captura mediciones y revisa escenarios. El cliente final consulta resultados publicados por enlace.",
  },
  {
    pregunta: "¿Dónde descargo la app móvil?",
    respuesta:
      "La APK se publica solo cuando exista un release aprobado. Mientras tanto, la sección Descargas mantiene el recurso marcado como pendiente para evitar enlaces informales.",
  },
  {
    pregunta: "¿Qué significa RSSI >= -70 dBm?",
    respuesta:
      "Es el objetivo de diseño visible del proyecto: una señal igual o superior a -70 dBm se considera una meta adecuada de cobertura para los análisis presentados.",
  },
  {
    pregunta: "¿Qué significa RSSI < -90 dBm?",
    respuesta:
      "RSSI menor a -90 dBm se interpreta como zona muerta dentro del criterio técnico del proyecto y debe revisarse como posible área sin cobertura útil.",
  },
  {
    pregunta: "¿Cómo reporto un problema?",
    respuesta:
      "Envía nombre, rol, organización, URL o pantalla, pasos para reproducir, fecha y hora, captura si corresponde, y versión de APK o navegador.",
  },
  {
    pregunta: "¿Qué datos trata el sistema?",
    respuesta:
      "El sistema trata datos de usuarios, clientes, proyectos, planos, mediciones WiFi, mapas de calor y enlaces de publicación. No se deben enviar contraseñas ni claves WiFi reales por soporte.",
  },
];

const politicas = [
  "Privacidad: datos recolectados, finalidad, responsables, conservación, seguridad y contacto.",
  "Términos de uso: acceso permitido, restricciones, disponibilidad y responsabilidades.",
  "Licenciamiento: titularidad académica, componentes de terceros y distribución controlada del APK.",
  "Soporte: canales, horarios, severidades, tiempos de respuesta y alcance del servicio.",
  "Mantenimiento: revisión por release, validación mensual y retiro de contenido obsoleto.",
];

function buscarRespuesta(consulta: string): string {
  const normalizada = consulta.toLowerCase();
  const preguntaExacta = preguntas.find(
    ({ pregunta }) => pregunta.toLowerCase() === normalizada,
  );
  if (preguntaExacta) {
    return preguntaExacta.respuesta;
  }

  const encontrada = preguntas.find(({ pregunta, respuesta }) => {
    const base = `${pregunta} ${respuesta}`.toLowerCase();
    return normalizada
      .split(/\s+/)
      .filter((palabra) => palabra.length > 3)
      .some((palabra) => base.includes(palabra));
  });

  return (
    encontrada?.respuesta ??
    "Puedo responder sobre Team 24 Software, Wireless HeatMapper, roles, descargas, soporte, RSSI y privacidad. Si la consulta requiere validación del equipo, usa el formulario o el correo de contacto."
  );
}

function SitioEmpresa() {
  const [consulta, setConsulta] = useState("");
  const [respuesta, setRespuesta] = useState(preguntas[1].respuesta);
  const [estadoChatbot, setEstadoChatbot] = useState<EstadoChatbot>("listo");
  const [origenRespuesta, setOrigenRespuesta] = useState<"azure_openai" | "local">("local");
  const anio = useMemo(() => new Date().getFullYear(), []);

  const responderConsulta = useCallback(async (texto: string) => {
    const pregunta = texto.trim();
    if (!pregunta) {
      setRespuesta("Escribe una consulta breve sobre Team 24 Software o Wireless HeatMapper.");
      setOrigenRespuesta("local");
      setEstadoChatbot("respaldo");
      return;
    }

    setEstadoChatbot("consultando");
    try {
      const data = await consultarChatbotEmpresa(pregunta);
      setRespuesta(data.respuesta);
      setOrigenRespuesta(data.origen);
      setEstadoChatbot("listo");
    } catch {
      setRespuesta(buscarRespuesta(pregunta));
      setOrigenRespuesta("local");
      setEstadoChatbot("respaldo");
    }
  }, []);

  function enviarConsulta(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    void responderConsulta(consulta);
  }

  return (
    <main className={styles.sitio}>
      <header className={styles.barraSuperior}>
        <a className={styles.marca} href="#inicio" aria-label="Ir al inicio">
          <img src={logoTeam24} alt="Team 24 Software" />
        </a>
        <nav className={styles.navegacion} aria-label="Secciones públicas">
          {navegacion.map(([etiqueta, href]) => (
            <a key={href} href={href}>
              {etiqueta}
            </a>
          ))}
        </nav>
        <a className={styles.botonAcceso} href="/admin/login">
          Acceso
          <ArrowRight size={16} aria-hidden="true" />
        </a>
      </header>

      <section id="inicio" className={styles.hero} aria-labelledby="titulo-hero">
        <img className={styles.heroImagen} src={heroEmpresa} alt="" aria-hidden="true" />
        <div className={styles.heroContenido}>
          <p className={styles.etiqueta}>Team 24 Software · Santa Cruz de la Sierra</p>
          <h1 id="titulo-hero">Soluciones de software técnico para redes, analítica y operación empresarial.</h1>
          <p>
            Desarrollamos plataformas web, móviles y backend para convertir procesos técnicos en evidencia
            centralizada, verificable y publicada en línea.
          </p>
          <div className={styles.accionesHero}>
            <a className={styles.botonPrimario} href="#producto">
              Ver Wireless HeatMapper
              <ArrowRight size={18} aria-hidden="true" />
            </a>
            <a className={styles.botonSecundario} href="#contacto">
              Solicitar demostración
            </a>
          </div>
        </div>
      </section>

      <section className={styles.bandaMetricas} aria-label="Indicadores institucionales">
        <article>
          <strong>100 % en línea</strong>
          <span>Sin persistencia local de dominio ni sincronización diferida.</span>
        </article>
        <article>
          <strong>Grupo 24</strong>
          <span>Equipo académico con roles Scrum y trazabilidad documental.</span>
        </article>
        <article>
          <strong>Azure + HTTPS</strong>
          <span>Publicación prevista en infraestructura cloud con CI/CD.</span>
        </article>
        <article>
          <strong>RSSI técnico</strong>
          <span>Objetivo ≥ -70 dBm y zona muerta &lt; -90 dBm.</span>
        </article>
      </section>

      <section id="empresa" className={styles.seccion} aria-labelledby="titulo-empresa">
        <div className={styles.encabezadoSeccion}>
          <p className={styles.etiqueta}>Empresa</p>
          <h2 id="titulo-empresa">Identidad institucional clara</h2>
          <p>
            Team 24 Software es la empresa desarrolladora del producto. Bulldog Tech. se mantiene como
            cliente del caso de estudio usado para contextualizar el problema de cobertura WiFi.
          </p>
        </div>
        <div className={styles.grillaDosColumnas}>
          <div className={styles.panelTexto}>
            <h3>Quiénes somos</h3>
            <p>
              Somos el Grupo 24 de Ingeniería de Software II, con perfil de desarrollo web, móvil,
              backend, documentación, pruebas y despliegue. Trabajamos con enfoque Scrum, evidencia
              trazable y validación técnica.
            </p>
            <dl className={styles.listaDefinicion}>
              <div>
                <dt>Misión</dt>
                <dd>Desarrollar soluciones digitales verificables, mantenibles y orientadas a necesidades reales de clientes.</dd>
              </div>
              <div>
                <dt>Visión</dt>
                <dd>Consolidarnos como equipo proveedor de software técnico para redes, analítica y procesos empresariales.</dd>
              </div>
            </dl>
          </div>
          <div className={styles.panelValores}>
            {["Calidad", "Trazabilidad", "Responsabilidad", "Seguridad", "Aprendizaje continuo", "Comunicación clara"].map(
              (valor) => (
                <span key={valor}>
                  <CheckCircle2 size={18} aria-hidden="true" />
                  {valor}
                </span>
              ),
            )}
          </div>
        </div>
      </section>

      <section id="servicios" className={styles.seccionAlterna} aria-labelledby="titulo-servicios">
        <div className={styles.encabezadoSeccion}>
          <p className={styles.etiqueta}>Servicios</p>
          <h2 id="titulo-servicios">Capacidades contratables y demostrables</h2>
          <p>
            Cada servicio se presenta con alcance verificable, beneficios concretos y entregables
            alineados al stack del proyecto.
          </p>
        </div>
        <div className={styles.grillaServicios}>
          {servicios.map((servicio) => {
            const IconoServicio = servicio.icono;
            return (
              <article className={styles.tarjetaServicio} key={servicio.titulo}>
                <IconoServicio size={28} aria-hidden="true" />
                <h3>{servicio.titulo}</h3>
                <p>{servicio.descripcion}</p>
                <strong>{servicio.beneficio}</strong>
                <span>{servicio.entregable}</span>
                <a href="#contacto">
                  Contactar
                  <ArrowRight size={16} aria-hidden="true" />
                </a>
              </article>
            );
          })}
        </div>
      </section>

      <section id="producto" className={styles.seccionProducto} aria-labelledby="titulo-producto">
        <div className={styles.productoContenido}>
          <p className={styles.etiqueta}>Producto destacado</p>
          <h2 id="titulo-producto">Wireless HeatMapper</h2>
          <p>
            Solución integrada para relevar, procesar y publicar resultados de cobertura WiFi en
            interiores mediante mapas de calor, portal web y asistencia IA en backend.
          </p>
          <div className={styles.componentesProducto}>
            {[
              ["App Android", Smartphone],
              ["Backend FastAPI", Cloud],
              ["PostgreSQL", LockKeyhole],
              ["Panel web", Building2],
              ["Portal cliente", Users],
              ["IA backend", Sparkles],
            ].map(([texto, IconoComponente]) => (
              <span key={texto as string}>
                <IconoComponente size={16} aria-hidden="true" />
                {texto as string}
              </span>
            ))}
          </div>
          <ul className={styles.listaBeneficios}>
            {beneficiosProducto.map((beneficio) => (
              <li key={beneficio}>
                <CheckCircle2 size={18} aria-hidden="true" />
                {beneficio}
              </li>
            ))}
          </ul>
          <div className={styles.accionesInline}>
            <a className={styles.botonPrimario} href="/admin/login">
              Login
              <ExternalLink size={16} aria-hidden="true" />
            </a>
            <a className={styles.botonSecundario} href="/manual/">
              Manual
            </a>
            <a className={styles.botonSecundario} href="/api/docs">
              API
            </a>
          </div>
        </div>
        <img className={styles.imagenProducto} src={productoHeatmapper} alt="Dispositivos mostrando mapas de calor WiFi y paneles de análisis." />
      </section>

      <section id="descargas" className={styles.seccion} aria-labelledby="titulo-descargas">
        <div className={styles.encabezadoSeccion}>
          <p className={styles.etiqueta}>Descargas</p>
          <h2 id="titulo-descargas">Recursos oficiales y versionados</h2>
          <p>
            Solo se publican recursos aprobados. Los elementos aún no liberados se muestran como
            pendientes para evitar archivos sueltos o enlaces informales.
          </p>
        </div>
        <div className={styles.grillaRecursos}>
          {recursos.map((recurso) => (
            <article className={styles.recurso} key={recurso.titulo}>
              <Download size={24} aria-hidden="true" />
              <h3>{recurso.titulo}</h3>
              <p>{recurso.detalle}</p>
              {recurso.disponible ? (
                <a href={recurso.href}>
                  {recurso.accion}
                  <ArrowRight size={16} aria-hidden="true" />
                </a>
              ) : (
                <span className={styles.estadoPendiente}>{recurso.accion}</span>
              )}
            </article>
          ))}
        </div>
      </section>

      <section id="soporte" className={styles.seccionSoporte} aria-labelledby="titulo-soporte">
        <img className={styles.imagenSoporte} src={soporteDevops} alt="Mesa de soporte técnico con paneles de monitoreo y operación cloud." />
        <div className={styles.soporteContenido}>
          <p className={styles.etiqueta}>Soporte</p>
          <h2 id="titulo-soporte">Atención asistida y escalamiento humano</h2>
          <p>
            El soporte inicial orienta al usuario antes de escalar. Horario de atención:
            lunes a viernes, 08:30 a 18:30, hora de Bolivia.
          </p>
          <div className={styles.severidades}>
            {[
              ["Alta", "Sistema inaccesible, login general caído o pérdida de acceso al portal.", "4 horas hábiles"],
              ["Media", "Error en carga de planos, heatmap o descarga no disponible.", "1 día hábil"],
              ["Baja", "Consulta funcional, ajuste de texto, duda de uso o mejora.", "2 días hábiles"],
            ].map(([nivel, ejemplo, tiempo]) => (
              <article key={nivel}>
                <strong>{nivel}</strong>
                <p>{ejemplo}</p>
                <span>{tiempo}</span>
              </article>
            ))}
          </div>
          <div className={styles.datosSoporte}>
            <h3>Datos mínimos para reportar incidentes</h3>
            <p>
              Nombre, rol, organización, URL o pantalla, pasos para reproducir, fecha y hora,
              captura si corresponde, y versión de APK o navegador.
            </p>
          </div>
        </div>
      </section>

      <section id="chatbot" className={styles.seccionAlterna} aria-labelledby="titulo-chatbot">
        <div className={styles.encabezadoSeccion}>
          <p className={styles.etiqueta}>Chatbot</p>
          <h2 id="titulo-chatbot">Asistente entrenado con información aprobada</h2>
          <p>
            Responde sobre empresa, producto, soporte, descargas, WiFi básico y privacidad. No
            solicita credenciales ni inventa precios o compromisos comerciales.
          </p>
        </div>
        <div className={styles.chatbot}>
          <div className={styles.panelPreguntas}>
            {preguntas.slice(0, 7).map((item) => (
              <button
                key={item.pregunta}
                type="button"
                disabled={estadoChatbot === "consultando"}
                onClick={() => {
                  setConsulta(item.pregunta);
                  void responderConsulta(item.pregunta);
                }}
              >
                {item.pregunta}
              </button>
            ))}
          </div>
          <div className={styles.panelRespuesta} aria-live="polite">
            {estadoChatbot === "consultando" ? (
              <Loader2 className={styles.iconoCargando} size={32} aria-hidden="true" />
            ) : (
              <Bot size={32} aria-hidden="true" />
            )}
            <span className={styles.estadoChatbot}>
              {estadoChatbot === "consultando"
                ? "Consultando Azure OpenAI"
                : origenRespuesta === "azure_openai"
                  ? "Respuesta generada con Azure OpenAI"
                  : "Respuesta local de respaldo"}
            </span>
            <p>{respuesta}</p>
            <form onSubmit={enviarConsulta} className={styles.formChatbot}>
              <label htmlFor="consulta-chatbot">Consulta breve</label>
              <div>
                <input
                  id="consulta-chatbot"
                  value={consulta}
                  onChange={(evento) => setConsulta(evento.target.value)}
                  placeholder="Ej.: ¿cómo reporto un problema?"
                  maxLength={700}
                />
                <button type="submit" disabled={estadoChatbot === "consultando"}>
                  <Send size={16} aria-hidden="true" />
                  Consultar
                </button>
              </div>
              {estadoChatbot === "respaldo" && (
                <small className={styles.avisoChatbot}>
                  No se pudo consultar la IA en este momento; se muestra una respuesta aprobada localmente.
                </small>
              )}
            </form>
          </div>
        </div>
      </section>

      <section id="contacto" className={styles.seccionContacto} aria-labelledby="titulo-contacto">
        <div className={styles.contactoDatos}>
          <p className={styles.etiqueta}>Contacto</p>
          <h2 id="titulo-contacto">Solicitudes comerciales, soporte y evidencias académicas</h2>
          <p>
            Para demostraciones, soporte o consultas formales, usa los canales autorizados. No
            envíes contraseñas, tokens, claves WiFi reales ni secretos de infraestructura.
          </p>
          <ul>
            <li>
              <Mail size={18} aria-hidden="true" />
              <a href={`mailto:${correoContacto}`}>{correoContacto}</a>
            </li>
            <li>
              <Phone size={18} aria-hidden="true" />
              <a href={`tel:${telefonoContacto}`}>{telefonoContacto}</a>
            </li>
            <li>
              <MessageSquare size={18} aria-hidden="true" />
              <a href={whatsappContacto}>WhatsApp autorizado</a>
            </li>
            <li>
              <MapPin size={18} aria-hidden="true" />
              Santa Cruz de la Sierra, Bolivia
            </li>
          </ul>
          <div className={styles.redesSociales} aria-label="Red social oficial">
            <a href={facebookEmpresa} target="_blank" rel="noreferrer">
              Facebook oficial
              <ExternalLink size={16} aria-hidden="true" />
            </a>
          </div>
        </div>
        <form className={styles.formularioContacto}>
          <label htmlFor="nombre-contacto">Nombre</label>
          <input id="nombre-contacto" name="nombre" autoComplete="name" />
          <label htmlFor="correo-contacto">Correo</label>
          <input id="correo-contacto" name="correo" type="email" autoComplete="email" />
          <label htmlFor="organizacion-contacto">Organización</label>
          <input id="organizacion-contacto" name="organizacion" autoComplete="organization" />
          <label htmlFor="motivo-contacto">Motivo</label>
          <select id="motivo-contacto" name="motivo" defaultValue="demo">
            <option value="demo">Solicitar demostración</option>
            <option value="soporte">Soporte general</option>
            <option value="academico">Consulta académica</option>
            <option value="comercial">Información comercial</option>
          </select>
          <label htmlFor="mensaje-contacto">Mensaje</label>
          <textarea id="mensaje-contacto" name="mensaje" rows={5} />
          <label className={styles.consentimiento}>
            <input type="checkbox" required />
            Acepto el tratamiento de estos datos para responder mi solicitud.
          </label>
          <a
            className={styles.botonPrimario}
            href={`mailto:${correoContacto}?subject=Solicitud%20desde%20sitio%20Team%2024%20Software`}
          >
            Enviar por correo
            <Mail size={16} aria-hidden="true" />
          </a>
        </form>
      </section>

      <section id="politicas" className={styles.seccion} aria-labelledby="titulo-politicas">
        <div className={styles.encabezadoSeccion}>
          <p className={styles.etiqueta}>Políticas públicas</p>
          <h2 id="titulo-politicas">Transparencia, mantenimiento y seguridad de información</h2>
          <p>
            El contenido del sitio se trata como información oficial y se revisa en cada release,
            de forma mensual, antes de demos y ante incidentes críticos.
          </p>
        </div>
        <div className={styles.grillaPoliticas}>
          {politicas.map((politica) => (
            <article key={politica}>
              <FileText size={22} aria-hidden="true" />
              <p>{politica}</p>
            </article>
          ))}
        </div>
      </section>

      <footer className={styles.piePagina}>
        <div>
          <img src={logoTeam24} alt="Team 24 Software" />
          <p>© {anio} Team 24 Software. Proyecto académico con publicación empresarial formal.</p>
        </div>
        <div className={styles.enlacesPie}>
          <a href={urlPublica}>URL pública</a>
          <a href={facebookEmpresa} target="_blank" rel="noreferrer">Facebook</a>
          <a href="/admin/login">Login</a>
          <a href="/manual/">Manual</a>
          <a href="#chatbot">Chatbot</a>
        </div>
      </footer>
    </main>
  );
}

export default SitioEmpresa;
