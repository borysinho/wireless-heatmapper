from __future__ import annotations

import re
import sys
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import fitz


PDF_NAME = "Certified Wireless Network Administrator - Official Study Guide.pdf"
OUTPUT_DIR_NAME = "Certified Wireless Network Administrator - Official Study Guide Markdown"
WORKERS = 8


@dataclass(frozen=True)
class Section:
    number: int
    title: str
    start_page: int
    end_page: int
    filename: str


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def section_filename(index: int, title: str) -> str:
    if title.lower().startswith("chapter "):
        match = re.match(r"chapter\s+(\d+)\s*-\s*(.*)", title, re.IGNORECASE)
        if match:
            chapter_no = int(match.group(1))
            slug = slugify(match.group(2))
            return f"{chapter_no:02d}-{slug}.md"
    if title.lower().startswith("appendix"):
        return f"{index:02d}-{slugify(title)}.md"
    if "glossary" in title.lower():
        return f"{index:02d}-{slugify(title)}.md"
    return f"{index:02d}-{slugify(title) or 'front-matter'}.md"


def build_sections(pdf_path: Path) -> list[Section]:
    doc = fitz.open(pdf_path)
    try:
        level_one = [entry for entry in doc.get_toc() if entry[0] == 1]
        if not level_one:
            return [
                Section(
                    number=1,
                    title=pdf_path.stem,
                    start_page=0,
                    end_page=doc.page_count - 1,
                    filename="01-document.md",
                )
            ]

        sections: list[Section] = []
        for index, (_, title, toc_page) in enumerate(level_one):
            start_page = max(toc_page - 1, 0)
            if index + 1 < len(level_one):
                end_page = max(level_one[index + 1][2] - 2, start_page)
            else:
                end_page = doc.page_count - 1
            sections.append(
                Section(
                    number=index + 1,
                    title=title,
                    start_page=start_page,
                    end_page=end_page,
                    filename=section_filename(index, title),
                )
            )
        return sections
    finally:
        doc.close()


def normalize_markdown(markdown: str, section: Section, output_dir: Path) -> str:
    output_prefix = output_dir.resolve().as_posix().rstrip("/") + "/"
    markdown = markdown.replace(output_prefix, "")
    markdown = markdown.replace("\\", "/")
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()
    page_note = f"_PDF pages {section.start_page + 1}-{section.end_page + 1}_"
    return f"# {section.title}\n\n{page_note}\n\n{markdown}\n"


def convert_section(args: tuple[Path, Path, Section]) -> tuple[str, int, int]:
    pdf_path, output_dir, section = args

    import pymupdf4llm

    pymupdf4llm.use_layout(False)

    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    pages = list(range(section.start_page, section.end_page + 1))
    markdown = pymupdf4llm.to_markdown(
        str(pdf_path),
        pages=pages,
        write_images=True,
        embed_images=False,
        image_path=str(images_dir),
        image_format="png",
        image_size_limit=0.025,
        dpi=180,
        filename=section.filename.replace(".md", ".pdf"),
        page_separators=True,
        show_progress=False,
    )

    output_file = output_dir / section.filename
    output_file.write_text(
        normalize_markdown(markdown, section, output_dir),
        encoding="utf-8",
    )
    return section.filename, section.start_page + 1, section.end_page + 1


def write_index(output_dir: Path, sections: list[Section], results: dict[str, tuple[int, int]]) -> None:
    lines = [
        "# Certified Wireless Network Administrator - Official Study Guide",
        "",
        "Contenido convertido desde PDF con PyMuPDF / pymupdf4llm.",
        "",
        "## Archivos",
        "",
    ]
    for section in sections:
        start_page, end_page = results[section.filename]
        lines.append(f"- [{section.title}]({section.filename}) - PDF pages {start_page}-{end_page}")
    lines.append("")
    lines.append("## Recursos")
    lines.append("")
    lines.append("- [Imágenes extraídas](images/)")
    lines.append("- [Script de conversión](convert_pdf_to_markdown.py)")
    lines.append("")
    (output_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    pdf_path = root / PDF_NAME
    output_dir = root / OUTPUT_DIR_NAME

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    output_dir.mkdir(exist_ok=True)
    (output_dir / "images").mkdir(exist_ok=True)

    sections = build_sections(pdf_path)
    print(f"Found {len(sections)} top-level sections.")
    print(f"Converting with {WORKERS} workers...")

    results: dict[str, tuple[int, int]] = {}
    jobs = [(pdf_path, output_dir, section) for section in sections]
    with ProcessPoolExecutor(max_workers=WORKERS, mp_context=mp.get_context("fork")) as executor:
        futures = {executor.submit(convert_section, job): job[2] for job in jobs}
        for future in as_completed(futures):
            section = futures[future]
            filename, start_page, end_page = future.result()
            results[filename] = (start_page, end_page)
            print(f"  done: {filename} (PDF pages {start_page}-{end_page})")

    write_index(output_dir, sections, results)
    print(f"Finished: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
