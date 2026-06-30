const input = document.querySelector("#busqueda");
const sections = Array.from(document.querySelectorAll(".manual-section"));
const emptyState = document.querySelector("#sin-resultados");
const navLinks = Array.from(document.querySelectorAll(".nav-list a"));
const progress = document.querySelector("#progreso");

function normalizar(texto) {
  return texto
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function filtrarManual(valor) {
  const termino = normalizar(valor.trim());
  let visibles = 0;

  sections.forEach((section) => {
    const contenido = normalizar(
      `${section.textContent ?? ""} ${section.dataset.search ?? ""}`,
    );
    const coincide = termino.length === 0 || contenido.includes(termino);
    section.classList.toggle("hidden", !coincide);
    if (coincide) visibles += 1;
  });

  emptyState.classList.toggle("hidden", visibles !== 0);
}

function marcarSeccionActiva() {
  const posicion = window.scrollY + 120;
  let activa = sections[0]?.id;

  sections.forEach((section) => {
    if (!section.classList.contains("hidden") && section.offsetTop <= posicion) {
      activa = section.id;
    }
  });

  navLinks.forEach((link) => {
    link.classList.toggle("active", link.getAttribute("href") === `#${activa}`);
  });
}

function actualizarProgreso() {
  if (!progress) return;
  const altoDocumento = document.documentElement.scrollHeight - window.innerHeight;
  const avance = altoDocumento <= 0 ? 0 : (window.scrollY / altoDocumento) * 100;
  progress.style.width = `${Math.min(100, Math.max(0, avance))}%`;
}

input?.addEventListener("input", (event) => {
  filtrarManual(event.target.value);
  marcarSeccionActiva();
  actualizarProgreso();
});

window.addEventListener(
  "scroll",
  () => {
    marcarSeccionActiva();
    actualizarProgreso();
  },
  { passive: true },
);
window.addEventListener("hashchange", marcarSeccionActiva);
marcarSeccionActiva();
actualizarProgreso();
