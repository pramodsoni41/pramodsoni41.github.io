# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 16:35:21 2026

@author: acer
"""

from pathlib import Path
import re
import html
import shutil
import subprocess

import yaml
import bibtexparser
from jinja2 import Environment, FileSystemLoader, select_autoescape


BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUT_DIR = Path(r"I:\My Drive\Personal Webpage\Github\pramodsoni41.github.io")


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Design tokens ─────────────────────────────────── */
:root {
  --bg:      #f0f4f8;
  --card:    #ffffff;
  --text:    #0f172a;
  --muted:   #64748b;
  --accent:  #1d4ed8;
  --accent2: #3b82f6;
  --line:    #e2e8f0;
  --radius:  14px;
  --shadow:  0 4px 20px rgba(15,23,42,.08);
  --shadow-hover: 0 8px 32px rgba(15,23,42,.13);
}

/* ── Reset & base ──────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: 'Inter', system-ui, -apple-system, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  font-size: 15px;
}

/* accent bar at very top */
body::before {
  content: '';
  display: block;
  height: 4px;
  background: linear-gradient(90deg, var(--accent), var(--accent2), #60a5fa);
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 2000;
}

/* ── Links ──────────────────────────────────────────── */
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; color: var(--accent2); }

/* ── Layout ─────────────────────────────────────────── */
.wrap { max-width: 1000px; margin: 0 auto; padding: 0 22px; }

/* ── Navbar ─────────────────────────────────────────── */
.navbar {
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--line);
  position: sticky;
  top: 4px;          /* sits below the accent bar */
  z-index: 1000;
}

.nav-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 56px;
}

.nav-brand {
  font-weight: 700;
  font-size: 1rem;
  color: var(--text);
  letter-spacing: -.01em;
  white-space: nowrap;
}

.nav-links { display: flex; gap: 4px; }

.nav-links a {
  color: var(--muted);
  font-weight: 500;
  font-size: .875rem;
  padding: 6px 10px;
  border-radius: 8px;
  transition: background .15s, color .15s;
}

.nav-links a:hover { color: var(--accent); background: #eff6ff; text-decoration: none; }
.nav-links a.active { background: var(--accent); color: #fff !important; }

/* hamburger (mobile) */
.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
}
.nav-toggle span {
  display: block; width: 22px; height: 2px;
  background: var(--text); border-radius: 2px;
  transition: .2s;
}

@media (max-width: 760px) {
  .nav-toggle { display: flex; }
  .nav-links {
    display: none;
    flex-direction: column;
    position: absolute;
    top: 60px; left: 0; right: 0;
    background: #fff;
    border-bottom: 1px solid var(--line);
    padding: 12px 22px 18px;
    gap: 2px;
    z-index: 999;
  }
  .nav-links.open { display: flex; }
  .nav-links a { font-size: .95rem; padding: 9px 12px; }
}

/* ── Hero ───────────────────────────────────────────── */
.header { padding: 30px 0 4px; }

.hero {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 32px 36px;
  box-shadow: var(--shadow);
}

.hero-flex {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  flex-wrap: wrap;
}

.hero-text { flex: 1 1 480px; min-width: 260px; }

h1 { font-size: 2rem; font-weight: 700; letter-spacing: -.02em; line-height: 1.2; }

.subtitle { margin: .5rem 0 .2rem; color: var(--muted); font-size: .95rem; font-weight: 500; }
.meta     { color: var(--muted); font-size: .875rem; }

/* profile link pills */
.links { margin: 18px 0 14px; display: flex; flex-wrap: wrap; gap: 8px; }

.link-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: #fff;
  color: var(--text);
  font-size: .82rem;
  font-weight: 600;
  white-space: nowrap;
  transition: background .15s, border-color .15s, color .15s, box-shadow .15s;
  box-shadow: 0 1px 4px rgba(15,23,42,.06);
  text-decoration: none !important;
}
.link-btn:hover {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
  box-shadow: 0 4px 12px rgba(29,78,216,.25);
}
.link-btn.primary {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
.link-btn.primary:hover { background: #1e40af; border-color: #1e40af; }

.contact { display: flex; flex-wrap: wrap; gap: 16px; color: var(--muted); font-size: .875rem; }

.hero-photo { flex: 0 0 190px; display: flex; justify-content: flex-end; }
.hero-photo img {
  width: 180px; height: 220px;
  object-fit: cover;
  border-radius: 12px;
  border: 3px solid #dbeafe;
  box-shadow: 0 8px 24px rgba(15,23,42,.12);
}

@media (max-width: 680px) {
  .hero { padding: 24px 20px; }
  .hero-photo { justify-content: center; flex: 1 1 100%; order: -1; }
  .hero-photo img { width: 140px; height: 170px; }
}

/* ── Stats bar ──────────────────────────────────────── */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-top: 16px;
}
.stat-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 18px 16px;
  text-align: center;
  box-shadow: var(--shadow);
  transition: transform .15s, box-shadow .15s;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-hover); }
.stat-num  { font-size: 1.8rem; font-weight: 700; color: var(--accent); line-height: 1; }
.stat-label{ font-size: .78rem; color: var(--muted); margin-top: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: .04em; }

@media (max-width: 560px) {
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
}

/* ── Cards ──────────────────────────────────────────── */
.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 22px 24px;
  margin-top: 16px;
  box-shadow: var(--shadow);
  transition: box-shadow .2s;
}
.card:hover { box-shadow: var(--shadow-hover); }

.card h2 {
  margin: 0 0 14px;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--accent);
  padding-bottom: 10px;
  border-bottom: 2px solid var(--line);
  display: flex;
  align-items: center;
  gap: 8px;
}
.card h2::before {
  content: '';
  display: inline-block;
  width: 4px; height: 18px;
  background: var(--accent);
  border-radius: 2px;
  flex-shrink: 0;
}

.card ul li { margin-bottom: 10px; }
.card small  { color: var(--muted); }

/* ── Timeline items ─────────────────────────────────── */
.item {
  padding: 12px 0;
  border-top: 1px solid var(--line);
}
.item:first-child { border-top: none; padding-top: 0; }

.item h3 { font-size: .95rem; font-weight: 600; margin-bottom: 2px; }
.item .period {
  font-size: .8rem;
  font-weight: 600;
  color: var(--accent);
  background: #eff6ff;
  border-radius: 999px;
  padding: 2px 10px;
  display: inline-block;
  margin-bottom: 4px;
}
.item p { font-size: .88rem; color: var(--muted); margin-top: 2px; }

/* ── Grid ───────────────────────────────────────────── */
.grid { display: grid; grid-template-columns: 1fr; gap: 16px; margin-top: 16px; }
@media (min-width: 820px) { .grid { grid-template-columns: 1fr 1fr; } }
.grid .card { margin-top: 0; }

/* ── Publications ───────────────────────────────────── */
.publications ol { padding-left: 22px; }
.publications ol li {
  font-size: .9rem;
  line-height: 1.65;
  margin-bottom: 12px;
  color: var(--text);
}
.publications ol li em { color: var(--accent); font-style: normal; font-weight: 600; }

/* ── Slideshow ──────────────────────────────────────── */
.slider { position: relative; overflow: hidden; border-radius: 12px; border: 1px solid var(--line); }
.slides { position: relative; height: min(50vh, 480px); background: #f1f5f9; }
.slide  { position: absolute; inset: 0; opacity: 0; transition: opacity 600ms ease; }
.slide.active { opacity: 1; }
.slide img { width: 100%; height: 100%; object-fit: cover; display: block; }

.nav {
  position: absolute; top: 50%; transform: translateY(-50%);
  width: 40px; height: 40px; border-radius: 50%;
  border: 1px solid rgba(15,23,42,.12);
  background: rgba(255,255,255,.9);
  color: var(--text);
  font-size: 24px; line-height: 38px; text-align: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(15,23,42,.12);
  transition: background .15s;
}
.nav:hover { background: #fff; }
.nav.prev { left: 10px; }
.nav.next { right: 10px; }

.dots {
  position: absolute; left: 50%; transform: translateX(-50%);
  bottom: 10px; display: flex; gap: 6px; padding: 6px 10px;
  background: rgba(255,255,255,.85);
  border: 1px solid rgba(15,23,42,.08);
  border-radius: 999px;
}
.dot {
  width: 8px; height: 8px; border-radius: 50%; border: none;
  background: rgba(15,23,42,.2); cursor: pointer;
  transition: background .2s, transform .2s;
}
.dot.active { background: var(--accent); transform: scale(1.3); }

/* ── Table ──────────────────────────────────────────── */
table { border-collapse: collapse; width: 100%; }
table td, table th {
  border-bottom: 1px solid var(--line);
  padding: 9px 10px;
  vertical-align: top;
  font-size: .88rem;
}
table tr:hover { background: #f8fafc; }

/* ── Footer ─────────────────────────────────────────── */
.site-footer {
  margin-top: 48px;
  padding: 28px 22px;
  border-top: 1px solid var(--line);
  text-align: center;
  color: var(--muted);
  font-size: .82rem;
  background: #fff;
}
.site-footer a { color: var(--muted); }
.site-footer a:hover { color: var(--accent); }

p  { line-height: 1.65; color: var(--text); }
li { line-height: 1.65; color: var(--text); }

/* ── Misc ───────────────────────────────────────────── */
main.wrap { padding-bottom: 12px; }
"""


# -----------------------------
# General helpers
# -----------------------------
def clean_latex_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace(r"\&", "&")
    text = text.replace("``", '"').replace("''", '"')
    text = text.replace(r"\hfill", " ")
    text = text.replace(r"\par", " ")
    text = text.replace(r"~", " ")
    text = text.replace(r"\LaTeX{}", "LaTeX")
    text = text.replace(r"\LaTeX", "LaTeX")
    text = text.replace(r"\ldots", "...")
    text = text.replace("---", "—")
    text = text.replace("--", "–")

    text = re.sub(r"\\smallcaps\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\textsc\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\textbf\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\emph\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\href\{([^}]*)\}\{([^}]*)\}", r'<a href="\1" target="_blank">\2</a>', text)
    text = re.sub(r"\\[A-Za-z]+", "", text)
    text = re.sub(r'\\textbf\{([^}]*)\}', r'<strong>\1</strong>', text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_rubric_block(tex_path: Path, rubric_name: str) -> str:
    if not tex_path.exists():
        return ""
    text = tex_path.read_text(encoding="utf-8")
    match = re.search(
        rf'\\begin\{{rubric\}}\{{{re.escape(rubric_name)}\}}(.*?)\\end\{{rubric\}}',
        text,
        flags=re.DOTALL
    )
    return match.group(1) if match else ""


def extract_subrubric_block(text: str, subrubric_name: str) -> str:
    match = re.search(
        rf'\\subrubric\{{{re.escape(subrubric_name)}\}}(.*?)(?=\\subrubric\{{|$)',
        text,
        flags=re.DOTALL
    )
    return match.group(1) if match else ""


# -----------------------------
# BibTeX
# -----------------------------
def format_authors(author_field: str) -> str:
    if not author_field:
        return ""
    authors = [a.strip() for a in author_field.split(" and ")]
    return "; ".join(authors)


def format_bib_entry(entry: dict) -> str:
    entry_type = entry.get("ENTRYTYPE", "").lower()
    authors = html.escape(format_authors(entry.get("author", "")))
    year = html.escape(str(entry.get("year", "")))
    title = html.escape(entry.get("title", "").strip("{} "))
    volume = html.escape(entry.get("volume", ""))
    number = html.escape(entry.get("number", ""))
    pages = html.escape(entry.get("pages", ""))
    journal = html.escape(entry.get("journal", ""))
    booktitle = html.escape(entry.get("booktitle", ""))

    if entry_type == "article":
        parts = [f"{authors} ({year}). {title}."]
        if journal:
            s = f"<em>{journal}</em>"
            if volume:
                s += f", {volume}"
                if number:
                    s += f"({number})"
            if pages:
                s += f", {pages}"
            parts.append(s + ".")
        return " ".join(parts)

    if entry_type == "inproceedings":
        parts = [f"{authors} ({year}). {title}."]
        if booktitle:
            s = f"<em>{booktitle}</em>"
            if pages:
                s += f", {pages}"
            parts.append(s + ".")
        return " ".join(parts)

    if entry_type == "incollection":
        parts = [f"{authors} ({year}). {title}."]
        if booktitle:
            s = f"<em>{booktitle}</em>"
            if pages:
                s += f", {pages}"
            parts.append(s + ".")
        return " ".join(parts)

    return f"{authors} ({year}). {title}."


def load_publications_from_bib(bib_path: Path):
    if not bib_path.exists():
        return [], [], [], []

    with bib_path.open("r", encoding="utf-8") as f:
        bib_database = bibtexparser.load(f)

    entries = bib_database.entries

    def year_key(e):
        try:
            return int(e.get("year", 0))
        except Exception:
            return 0

    entries = sorted(entries, key=year_key, reverse=True)

    publications_all = []
    journal_articles = []
    conference_papers = []
    book_chapters = []

    for entry in entries:
        formatted = format_bib_entry(entry)
        etype = entry.get("ENTRYTYPE", "").lower()

        publications_all.append(formatted)
        if etype == "article":
            journal_articles.append(formatted)
        elif etype == "inproceedings":
            conference_papers.append(formatted)
        elif etype == "incollection":
            book_chapters.append(formatted)

    return publications_all, journal_articles, conference_papers, book_chapters


# -----------------------------
# CV section parsers
# -----------------------------
def parse_entry_blocks(rubric_text: str):
    pattern = r'\\entry\*\[([^\]]*)\]\s*(.*?)(?=\\entry\*\[|$)'
    return re.findall(pattern, rubric_text, flags=re.DOTALL)


def load_employment_from_tex(tex_path: Path):
    rubric_text = extract_rubric_block(tex_path, "Employment History")
    matches = parse_entry_blocks(rubric_text)

    items = []
    for period, body in matches:
        title_match = re.search(r'\\textbf\{([^}]*)\}', body)
        title = clean_latex_text(title_match.group(1)) if title_match else ""

        body_no_title = re.sub(r'\\textbf\{[^}]*\}\s*,?\s*', '', body, count=1).strip()
        items.append({
            "period": clean_latex_text(period),
            "title": title,
            "details": clean_latex_text(body_no_title)
        })
    return items


def load_education_from_tex(tex_path: Path):
    rubric_text = extract_rubric_block(tex_path, "Education")
    matches = parse_entry_blocks(rubric_text)

    items = []
    for period, body in matches:
        degree_match = re.search(r'\\textbf\{([^}]*)\}', body)
        degree = clean_latex_text(degree_match.group(1)) if degree_match else ""

        body_wo_degree = re.sub(r'\\textbf\{[^}]*\}\s*,?\s*', '', body, count=1).strip()
        parts = [p.strip() for p in re.split(r'\\par', body_wo_degree) if p.strip()]

        items.append({
            "period": clean_latex_text(period),
            "degree": degree,
            "institution": clean_latex_text(parts[0]) if len(parts) > 0 else "",
            "specialization": clean_latex_text(parts[1]) if len(parts) > 1 else "",
            "links": clean_latex_text(" ".join(parts[2:])) if len(parts) > 2 else "",
        })
    return items


def load_projects_from_tex(tex_path: Path):
    if not tex_path.exists():
        return []

    text = tex_path.read_text(encoding="utf-8")
    pattern = r'\\textbf\{([^}]*)\}\s*(\(([^)]*)\))?'
    matches = re.findall(pattern, text)

    projects = []
    for full_title, _, extra in matches:
        raw = full_title.strip()
        extra = extra.strip() if extra else ""

        title = raw
        agency = ""
        amount = ""

        parts = [p.strip() for p in raw.split(",")]
        if len(parts) > 1:
            possible_agency = parts[-1]
            title_candidate = ", ".join(parts[:-1])
            if any(k.lower() in possible_agency.lower() for k in [
                "giz", "namami gange", "aicte", "teqip", "department of science and technology", "dst", "slcr"
            ]):
                title = title_candidate
                agency = possible_agency

        if extra:
            if "Rs." in extra or "INR" in extra or "USD" in extra:
                amount = extra
            elif not agency:
                agency = extra

        projects.append({
            "title": title,
            "agency": agency,
            "amount": amount
        })

    return projects


def load_consultancy_from_tex(tex_path: Path):
    if not tex_path.exists():
        return []

    text = tex_path.read_text(encoding="utf-8")
    pattern = r'\\entry\*\{\}\s*(.*?)(?=\\entry\*\{\}|\\end\{rubric\})'
    blocks = re.findall(pattern, text, flags=re.DOTALL)

    consultancy = []
    for block in blocks:
        block = block.strip()
        itemize_match = re.search(r'(.*?)\\begin\{itemize\}(.*?)\\end\{itemize\}', block, flags=re.DOTALL)

        if itemize_match:
            main_text = clean_latex_text(itemize_match.group(1))
            items_text = itemize_match.group(2)
            subitems = re.findall(r'\\item\s*(.*?)(?=\\item|$)', items_text, flags=re.DOTALL)
            subitems = [clean_latex_text(s) for s in subitems if clean_latex_text(s)]
            consultancy.append({"title": main_text, "subitems": subitems})
        else:
            consultancy.append({"title": clean_latex_text(block), "subitems": []})

    return consultancy


def load_teaching_from_tex(tex_path: Path):
    rubric_text = extract_rubric_block(tex_path, "Teaching")
    if not rubric_text:
        return []

    parts = re.split(r'\\subrubric\{([^}]*)\}', rubric_text)
    groups = []

    for i in range(1, len(parts), 2):
        heading = clean_latex_text(parts[i])
        content = parts[i + 1]

        raw_entries = re.findall(
            r'\\entry\*\{\}\s*(.*?)(?=\\entry\*\{\}|\\subrubric\{|$)',
            content,
            flags=re.DOTALL
        )

        courses = []
        for raw in raw_entries:
            raw_clean = clean_latex_text(raw)
            m = re.match(r'^(.*?)\s*(?:\(([^)]*)\))?$', raw_clean)
            course_name = m.group(1).strip() if m else raw_clean
            course_code = m.group(2).strip() if m and m.group(2) else ""
            courses.append({"name": course_name, "code": course_code})

        groups.append({"category": heading, "courses": courses})

    return groups


def parse_student_entry(entry_text: str):
    entry_text = clean_latex_text(entry_text)
    m = re.match(r'(.+?)\s*(.*)', entry_text)
    if not m:
        return {"name": entry_text, "period": "", "topic": ""}

    text = entry_text

    # Name (year): topic
    m1 = re.match(r'^(.*?)\s*\((.*?)\)\s*:\s*(.*)$', text)
    if m1:
        return {
            "name": clean_latex_text(m1.group(1)),
            "period": clean_latex_text(m1.group(2)),
            "topic": clean_latex_text(m1.group(3)),
        }

    # Name: roll topic
    m2 = re.match(r'^(.*?)\s*:\s*(.*)$', text)
    if m2:
        return {
            "name": clean_latex_text(m2.group(1)),
            "period": "",
            "topic": clean_latex_text(m2.group(2)),
        }

    return {"name": text, "period": "", "topic": ""}


def load_students_from_tex(tex_path: Path):
    rubric_text = extract_rubric_block(tex_path, "Thesis Supervised")
    if not rubric_text:
        return []

    parts = re.split(r'\\subrubric\{([^}]*)\}', rubric_text)
    groups = []

    for i in range(1, len(parts), 2):
        heading = clean_latex_text(parts[i])
        content = parts[i + 1]

        raw_entries = re.findall(
            r'\\entry\*\{\}\s*(.*?)(?=\\entry\*\{\}|\\subrubric\{|$)',
            content,
            flags=re.DOTALL
        )

        students = [parse_student_entry(raw.strip()) for raw in raw_entries if raw.strip()]
        groups.append({"category": heading, "students": students})

    return groups


def load_plain_entries_from_rubric(tex_path: Path, rubric_name: str):
    rubric_text = extract_rubric_block(tex_path, rubric_name)
    if not rubric_text:
        return []

    matches = re.findall(
        r'\\entry\*\{\}\s*(.*?)(?=\\entry\*\{\}|$)',
        rubric_text,
        flags=re.DOTALL
    )
    return [clean_latex_text(x) for x in matches if clean_latex_text(x)]


def load_labeled_entries_from_rubric(tex_path: Path, rubric_name: str):
    rubric_text = extract_rubric_block(tex_path, rubric_name)
    if not rubric_text:
        return []

    rubric_text = re.sub(r'\\noentry\{[^}]*\}', '', rubric_text)
    matches = re.findall(
        r'\\entry\*\[([^\]]*)\]\s*(.*?)(?=\\entry\*\[|\\entry\*\{|$)',
        rubric_text,
        flags=re.DOTALL
    )

    items = []
    for label, value in matches:
        items.append({
            "label": clean_latex_text(label),
            "value": clean_latex_text(value)
        })
    return items


def load_awards_from_misc(tex_path: Path):
    rubric_text = extract_rubric_block(tex_path, "Miscellaneous Experience")
    if not rubric_text:
        return []

    awards_text = extract_subrubric_block(rubric_text, "Awards and Achievements")
    if not awards_text:
        return []

    matches = re.findall(
        r'\\entry\*\[([^\]]*)\]\s*(.*?)(?=\\entry\*\[|$)',
        awards_text,
        flags=re.DOTALL
    )

    awards = []
    for year, desc in matches:
        awards.append({
            "year": clean_latex_text(year),
            "text": clean_latex_text(desc)
        })
    return awards


# -----------------------------
# CV PDF build
# -----------------------------
def run_cmd(cmd, cwd: Path):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        shell=False
    )

    if result.returncode != 0:
        print("\n❌ Command failed:", " ".join(cmd))
        print("\n--- STDOUT ---\n")
        print(result.stdout)
        print("\n--- STDERR ---\n")
        print(result.stderr)
        raise RuntimeError(f"Command failed with exit code {result.returncode}")

    return result


def build_cv():
    """Build PDF CV from LaTeX source in cv/ folder (requires xelatex + biber)."""
    cv_dir = BASE_DIR / "cv"
    main_tex = "main.tex"
    main_name = "main"

    if not cv_dir.exists():
        print("⚠️ CV folder not found:", cv_dir)
        return

    try:
        run_cmd(["xelatex", "-interaction=nonstopmode", main_tex], cwd=cv_dir)
        run_cmd(["biber", main_name], cwd=cv_dir)
        run_cmd(["xelatex", "-interaction=nonstopmode", main_tex], cwd=cv_dir)
        run_cmd(["xelatex", "-interaction=nonstopmode", main_tex], cwd=cv_dir)

        pdf_src = cv_dir / f"{main_name}.pdf"
        pdf_dst = OUT_DIR / "cv.pdf"
        shutil.copy2(pdf_src, pdf_dst)

        print("✅ CV built and copied:", pdf_dst)

    except Exception as e:
        print("⚠️ CV build failed:", e)


def build_cv_html():
    """Generate static cv.html from data/cv.yaml and data/publications.bib."""
    data_dir = BASE_DIR / "data"
    yaml_path = data_dir / "cv.yaml"
    bib_path = data_dir / "publications.bib"

    if not yaml_path.exists():
        print("⚠️ data/cv.yaml not found")
        return

    cv = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    profile = cv.get("profile", {})

    _, journals, confs, books = load_publications_from_bib(bib_path)

    def section(title, content_html):
        return f"""
  <div class="section">
    <h2>{html.escape(title)}</h2>
    {content_html}
  </div>"""

    def timeline_items(items, date_key, title_key, subtitle_key, desc_key="description"):
        rows = []
        for item in items:
            rows.append(f"""
    <div class="employment-item">
      <div class="employment-date">{html.escape(str(item.get(date_key, "")))}</div>
      <div class="employment-marker">&#128278;</div>
      <div class="employment-content">
        <strong>{html.escape(str(item.get(title_key, "")))}</strong>
        {", " + html.escape(str(item.get(subtitle_key, ""))) if item.get(subtitle_key) else ""}
        {"<br>" + html.escape(str(item.get(desc_key, ""))) if item.get(desc_key) else ""}
      </div>
    </div>""")
        return "\n".join(rows)

    def pub_list(pubs):
        if not pubs:
            return "<p>No entries.</p>"
        items = "\n".join(f"<li>{p}</li>" for p in pubs)
        return f"<ol>{items}</ol>"

    # Build contact block
    contact_lines = []
    if profile.get("email"):
        contact_lines.append(f'<div><strong>Email:</strong> <a href="mailto:{html.escape(profile["email"])}">{html.escape(profile["email"])}</a></div>')
    if profile.get("phone"):
        contact_lines.append(f'<div><strong>Phone:</strong> {html.escape(profile["phone"])}</div>')
    if profile.get("website"):
        url = profile["website"] if profile["website"].startswith("http") else f"https://{profile['website']}"
        contact_lines.append(f'<div><strong>Website:</strong> <a href="{html.escape(url)}" target="_blank">{html.escape(profile["website"])}</a></div>')
    if profile.get("iitbhu_page"):
        contact_lines.append(f'<div><strong>Institute Page:</strong> <a href="{html.escape(profile["iitbhu_page"])}" target="_blank">IIT (BHU) Profile</a></div>')
    if profile.get("linkedin"):
        contact_lines.append(f'<div><strong>LinkedIn:</strong> <a href="{html.escape(profile["linkedin"])}" target="_blank">dr-pramod-soni</a></div>')
    for link_key in ("google_scholar", "orcid", "research_gate"):
        if profile.get(link_key):
            contact_lines.append(f'<div><strong>{link_key.replace("_", " ").title()}:</strong> <a href="{html.escape(profile[link_key])}" target="_blank">{html.escape(profile[link_key])}</a></div>')

    # Employment section
    employment_html = timeline_items(
        cv.get("employment", []), "period", "role", "institute"
    )

    # Education section
    education_html = timeline_items(
        cv.get("education", []), "period", "degree", "institute", "specialization"
    )

    # Research interests
    interests = cv.get("research_interests", [])
    interests_html = "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in interests) + "</ul>" if interests else ""

    # Research projects
    projects_html = ""
    for p in cv.get("research_projects", cv.get("projects", [])):
        meta = []
        if p.get("agency"):
            meta.append(html.escape(p["agency"]))
        if p.get("amount"):
            meta.append(html.escape(p["amount"]))
        if p.get("duration"):
            meta.append(html.escape(p["duration"]))
        if p.get("role"):
            meta.append(html.escape(p["role"]))
        meta_str = " &bull; ".join(meta)
        projects_html += f"""
    <div class="entry">
      <strong>{html.escape(p.get("title", ""))}</strong>
      {("<br><span style='font-size:13px;color:#475569'>" + meta_str + "</span>") if meta_str else ""}
    </div>"""

    # Consultancy projects
    consultancy_html = ""
    for c in cv.get("consultancy_projects", []):
        consultancy_html += f'<div class="entry">{html.escape(c)}</div>'

    # Expert lectures
    lectures_html = "<ul>" + "".join(
        f"<li>{html.escape(lec)}</li>" for lec in cv.get("expert_lectures", [])
    ) + "</ul>"

    # Short term courses
    stc_html = "<ul>" + "".join(
        f"<li>{html.escape(s)}</li>" for s in cv.get("short_term_courses", [])
    ) + "</ul>"

    # Memberships
    memberships_html = "<ul>" + "".join(
        f"<li>{html.escape(m)}</li>" for m in cv.get("memberships", [])
    ) + "</ul>"

    # Awards
    awards_html = ""
    for a in cv.get("awards", []):
        awards_html += f'<div class="employment-item"><div class="employment-date">{html.escape(str(a.get("year", "")))}</div><div class="employment-marker">&#127942;</div><div class="employment-content">{html.escape(a.get("text", ""))}</div></div>'

    # Skills
    skills_rows = "".join(
        f"<tr><td><strong>{html.escape(s.get('label', ''))}</strong></td><td>{html.escape(s.get('value', ''))}</td></tr>"
        for s in cv.get("skills", [])
    )
    skills_html = f"<table style='width:100%;border-collapse:collapse'>{skills_rows}</table>"

    # Teaching
    teaching_html = ""
    for group in cv.get("teaching", []):
        teaching_html += f"<h3 style='margin:12px 0 6px;font-size:1rem;color:#374151'>{html.escape(group.get('category', ''))}</h3><ul>"
        for course in group.get("courses", []):
            code = f" ({html.escape(course.get('code', ''))})" if course.get("code") else ""
            teaching_html += f"<li>{html.escape(course.get('name', ''))}{code}</li>"
        teaching_html += "</ul>"

    # Students
    students_html = ""
    for group in cv.get("students", []):
        students_html += f"<h3 style='margin:12px 0 6px;font-size:1rem;color:#374151'>{html.escape(group.get('category', ''))}</h3><ul>"
        for s in group.get("students", []):
            period = f" ({html.escape(s.get('period', ''))})" if s.get("period") else ""
            topic = f": {html.escape(s.get('topic', ''))}" if s.get("topic") else ""
            students_html += f"<li><strong>{html.escape(s.get('name', ''))}</strong>{period}{topic}</li>"
        students_html += "</ul>"

    # Administration
    admin_html = ""
    for group in cv.get("administration", []):
        admin_html += f"<h3 style='margin:12px 0 6px;font-size:1rem;color:#374151'>{html.escape(group.get('title', ''))}</h3><ul>"
        for item in group.get("items", []):
            admin_html += f"<li>{html.escape(item)}</li>"
        admin_html += "</ul>"

    # Assemble sections
    sections = []
    if employment_html.strip():
        sections.append(section("Employment History", employment_html))
    if education_html.strip():
        sections.append(section("Education", education_html))
    if interests_html:
        sections.append(section("Research Interests", interests_html))
    if projects_html.strip():
        sections.append(section("Research Projects", projects_html))
    if consultancy_html.strip():
        sections.append(section("Consultancy Projects", consultancy_html))
    if journals:
        sections.append(section(f"Journal Articles ({len(journals)})", pub_list(journals)))
    if confs:
        sections.append(section(f"Conference Papers ({len(confs)})", pub_list(confs)))
    if books:
        sections.append(section(f"Book Chapters ({len(books)})", pub_list(books)))
    if teaching_html.strip():
        sections.append(section("Teaching", teaching_html))
    if students_html.strip():
        sections.append(section("Students Supervised", students_html))
    if admin_html.strip():
        sections.append(section("Administrative Responsibilities", admin_html))
    if awards_html.strip():
        sections.append(section("Awards & Recognition", awards_html))
    if skills_html.strip():
        sections.append(section("Skills", skills_html))
    if memberships_html.strip():
        sections.append(section("Professional Memberships", memberships_html))
    if lectures_html.strip() and cv.get("expert_lectures"):
        sections.append(section("Expert Lectures Delivered", lectures_html))
    if stc_html.strip() and cv.get("short_term_courses"):
        sections.append(section("Short Term Courses Organized", stc_html))

    photo_html = ""
    if profile.get("photo"):
        photo_html = f'<div class="header-right"><img src="{html.escape(profile["photo"])}" alt="{html.escape(profile.get("name", ""))}"></div>'

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Curriculum Vitae | {html.escape(profile.get("name", ""))}</title>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box;font-family:"Segoe UI",Arial,sans-serif}}
    body{{background:#eef2f7;color:#1e293b;padding:30px;line-height:1.6}}
    .cv{{max-width:950px;margin:auto;background:#fff;padding:50px;border-radius:16px;box-shadow:0 15px 40px rgba(0,0,0,.08)}}
    .header{{display:flex;justify-content:space-between;align-items:center;gap:30px;padding-bottom:30px;border-bottom:2px solid #dbe4ee}}
    .header-left{{flex:1}}
    .header-left h1{{font-size:38px;font-weight:700;color:#0f172a;margin-bottom:10px}}
    .designation{{font-size:18px;font-weight:600;margin-bottom:10px;color:#1d4ed8}}
    .institute{{font-size:15px;color:#475569;margin-bottom:15px}}
    .contact{{font-size:14px;color:#334155}}
    .contact div{{margin-bottom:6px}}
    .header-right img{{width:170px;height:200px;object-fit:cover;border-radius:12px;border:3px solid #dbeafe}}
    .print-btn{{margin-top:18px;padding:12px 28px;border:none;border-radius:10px;background:#0f172a;color:#fff;cursor:pointer;font-size:15px;font-weight:600}}
    .section{{margin-top:35px}}
    .section h2{{font-size:22px;color:#0f172a;margin-bottom:15px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}}
    .entry{{margin-bottom:18px}}
    .employment-item{{display:grid;grid-template-columns:200px 24px 1fr;gap:12px;align-items:start;margin-bottom:14px}}
    .employment-date{{font-size:15px;color:#111827;text-align:right;font-weight:500;padding-top:2px}}
    .employment-marker{{color:#8b004b;font-size:18px;line-height:1;padding-top:2px}}
    .employment-content{{font-size:15px;line-height:1.5;color:#111827}}
    ol{{padding-left:20px}} ol li{{margin-bottom:8px;font-size:14px;line-height:1.6}}
    ul{{padding-left:20px}} ul li{{margin-bottom:6px;font-size:14px}}
    table td{{padding:6px 10px;border-bottom:1px solid #e2e8f0;font-size:14px;vertical-align:top}}
    a{{color:#1d4ed8;text-decoration:none}}
    .footer{{margin-top:40px;text-align:center;font-size:13px;color:#64748b}}
    @media print{{body{{background:#fff;padding:0}}.cv{{box-shadow:none;border-radius:0;padding:20px;max-width:100%}}.print-btn{{display:none}}@page{{size:A4;margin:12mm}}}}
  </style>
</head>
<body>
<div class="cv">
  <div class="header">
    <div class="header-left">
      <h1>{html.escape(profile.get("name", ""))}</h1>
      <div class="designation">{html.escape(profile.get("designation", ""))}</div>
      <div class="institute">{html.escape(profile.get("institute", ""))}<br>{html.escape(profile.get("city", ""))}</div>
      <div class="contact">{"".join(contact_lines)}</div>
      <button class="print-btn" onclick="window.print()">Download PDF</button>
    </div>
    {photo_html}
  </div>
  {"".join(sections)}
  <div class="footer">Curriculum Vitae &mdash; {html.escape(profile.get("name", ""))}</div>
</div>
</body>
</html>
"""

    out_path = OUT_DIR / "cv.html"
    out_path.write_text(page, encoding="utf-8")
    print(f"cv.html generated from data/ ({len(journals)} journal articles, {len(confs)} conference papers, {len(books)} book chapters)")

def load_administration(tex_path: Path):
    if not tex_path.exists():
        return []

    text = tex_path.read_text(encoding="utf-8")

    # Extract main rubric
    main_block = extract_rubric_block(tex_path, "Other Responsibilities")

    if not main_block:
        print("⚠️ 'Other Responsibilities' rubric not found")
        return []

    # Split into subrubrics (institutes)
    parts = re.split(r'\\subrubric\{([^}]*)\}', main_block)

    groups = []

    for i in range(1, len(parts), 2):
        heading = clean_latex_text(parts[i])
        content = parts[i + 1]

        entries = re.findall(
            r'\\entry\*\{\}\s*(.*?)(?=\\entry\*\{\}|\\subrubric\{|$)',
            content,
            flags=re.DOTALL
        )

        items = [clean_latex_text(e) for e in entries if clean_latex_text(e)]

        if items:
            groups.append({
                "title": heading,
                "items": items
            })

    return groups



# -----------------------------
# Site build
# -----------------------------
def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # LOAD BASE DATA
    # -----------------------------
    data = yaml.safe_load(
        (BASE_DIR / "content.yaml").read_text(encoding="utf-8")
    )

    cv_dir = BASE_DIR / "cv"

    # -----------------------------
    # PUBLICATIONS
    # -----------------------------
    bib_path = cv_dir / "publications.bib"
    if not bib_path.exists():
        bib_path = BASE_DIR / "data" / "publications.bib"
    pubs_all, journals, confs, books = load_publications_from_bib(bib_path)

    data.update({
        "publications": pubs_all,
        "recent_publications": pubs_all[:5],
        "journal_articles": journals,
        "conference_papers": confs,
        "book_chapters": books,
    })

    # -----------------------------
    # CV SECTIONS
    # -----------------------------
    data.update({
        "projects": load_projects_from_tex(cv_dir / "Research_Projects.tex"),
        "consultancy_projects": load_consultancy_from_tex(cv_dir / "Consultancy_Projects.tex"),
        "teaching_groups": load_teaching_from_tex(cv_dir / "Teaching.tex"),
        "employment_history": load_employment_from_tex(cv_dir / "employment.tex"),
        "education_history": load_education_from_tex(cv_dir / "education.tex"),
        "student_groups": load_students_from_tex(cv_dir / "Thesis.tex"),
        "awards_list": load_awards_from_misc(cv_dir / "misc.tex"),
        "memberships": load_plain_entries_from_rubric(cv_dir / "Membership.tex", "Professional Memberships"),
        "skills_list": load_labeled_entries_from_rubric(cv_dir / "skills.tex", "Skills"),
        "expert_lectures": load_plain_entries_from_rubric(cv_dir / "expert_lec.tex", "Expert Lectures Delivered"),
        "stp_items": load_plain_entries_from_rubric(cv_dir / "STP.tex", "Short Term Courses Organized"),
    })

    # -----------------------------
    # ✅ ADMINISTRATION (FINAL FIX)
    # -----------------------------
    admin_file = cv_dir / "responsibilities.tex"
    data["administration_groups"] = load_administration(admin_file)


    # -----------------------------
    # SLIDESHOW
    # -----------------------------
    slideshow_dir = BASE_DIR / "assets" / "slideshow"

    if slideshow_dir.exists():
        images = sorted(
            [p for p in slideshow_dir.iterdir()
             if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]],
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        data["slideshow"] = [f"assets/slideshow/{p.name}" for p in images]
    else:
        data["slideshow"] = []

    # -----------------------------
    # JINJA ENVIRONMENT
    # -----------------------------
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # -----------------------------
    # PAGES TO BUILD
    # -----------------------------
    pages = [
        "index.html",
        "Other_Activities.html",
        "publications.html",
        "projects.html",
        "teaching.html",
        "administration.html",   # ← now dynamic
        "students.html",
        "Important_Links.html",
        "ganga_model.html",
    ]

    # -----------------------------
    # RENDER PAGES
    # -----------------------------
    for page in pages:
        template = env.get_template(page)

        html_out = template.render(
            **data,
            current_page=page.replace(".html", "")
        )

        (OUT_DIR / page).write_text(html_out, encoding="utf-8")

    # -----------------------------
    # STATIC FILES
    # -----------------------------
    (OUT_DIR / "style.css").write_text(CSS.strip(), encoding="utf-8")

    slider_src = TEMPLATES_DIR / "slider.js"
    if slider_src.exists():
        shutil.copy2(slider_src, OUT_DIR / "slider.js")

    assets_src = BASE_DIR / "assets"
    assets_dst = OUT_DIR / "assets"
    if assets_src.exists():
        shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)

    print("✅ Website built successfully")
    print("📁 Output:", OUT_DIR)


if __name__ == "__main__":
    import sys
    if "cv" in sys.argv:
        build_cv_html()
    elif "pdf" in sys.argv:
        build_cv()
    else:
        build()
        build_cv_html()