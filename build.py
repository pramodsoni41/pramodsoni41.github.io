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
:root{
  --bg:#f6f8fc;
  --card:#ffffff;
  --text:#0f172a;
  --muted:#475569;
  --accent:#2563eb;
  --line:#d8e2f0;
}

*{box-sizing:border-box}
body{
  margin:0;
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;
  background: linear-gradient(180deg,#ffffff,var(--bg));
  color:var(--text);
}

.hero-flex{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:24px;
  flex-wrap:wrap;
}

.hero-text{
  flex: 1 1 520px;
  min-width: 280px;
}

.hero-photo{
  flex: 0 0 220px;
  display:flex;
  justify-content:flex-end;
}

.hero-photo img{
  width: 200px;
  height: 240px;
  object-fit: cover;
  border-radius: 14px;
  border: 1px solid var(--line);
  box-shadow: 0 10px 24px rgba(2,6,23,.10);
}

@media (max-width: 720px){
  .hero-photo{
    justify-content:center;
    flex: 1 1 100%;
  }
  .hero-photo img{
    width: 220px;
    height: 260px;
  }
}

a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}

.wrap{max-width:980px;margin:0 auto;padding:22px}

.header{padding-top:34px;padding-bottom:10px}

.hero{
  padding:22px;
  border:1px solid var(--line);
  background: var(--card);
  border-radius:18px;
  box-shadow: 0 10px 30px rgba(2,6,23,.06);
}

h1{margin:0;font-size:2.1rem}
.subtitle{margin:.4rem 0 0;color:var(--muted)}
.meta{margin:.25rem 0 0;color:var(--muted)}

.links{margin:14px 0;display:flex;flex-wrap:wrap;gap:12px}
.contact{display:flex;flex-wrap:wrap;gap:14px;color:var(--muted);font-size:.95rem}

.link-btn{
  padding:8px 14px;
  border-radius:8px;
  border:1px solid var(--line);
  background:#ffffff;
  font-weight:500;
  transition: all 0.2s ease;
  box-shadow: 0 4px 10px rgba(2,6,23,.05);
}
.link-btn:hover{
  background:var(--accent);
  color:#ffffff;
  border-color:var(--accent);
}

table td, table th {
  border-bottom: 1px solid #e2e8f0;
  padding: 8px;
  vertical-align: top;
}

table tr:hover {
  background: #f8fafc;
}

.card{
  border:1px solid var(--line);
  background: var(--card);
  border-radius:18px;
  padding:18px;
  margin-top:16px;
  box-shadow: 0 8px 24px rgba(2,6,23,.06);
}

.card h2{
  margin:0 0 10px;
  font-size:1.2rem;
  color:#1f3c88;
  border-bottom:2px solid #e5e7eb;
  padding-bottom:6px;
}

.nav-links a.active {
  background: var(--accent);
  color: #ffffff !important;
  border-radius: 8px;
  padding: 6px 14px;
}

.card ul li { margin-bottom: 12px; }
.card small { color: var(--muted); }

.grid{display:grid;grid-template-columns:1fr;gap:16px}

.item{padding:10px 0;border-top:1px dashed rgba(15,23,42,.15)}
.item:first-child{border-top:none;padding-top:0}
.item h3{margin:0 0 6px;font-size:1.05rem}

p{line-height:1.6;color:var(--text)}
li{line-height:1.6;color:var(--text)}

.footer{color:var(--muted);padding-top:10px;padding-bottom:30px}

@media (min-width: 820px){
  .grid{grid-template-columns:1fr 1fr}
}

/* Slideshow */
.slider { position: relative; overflow: hidden; border-radius: 16px; border: 1px solid var(--line); }
.slides { position: relative; height: min(52vh, 520px); background: rgba(2,6,23,0.04); }
.slide { position: absolute; inset: 0; opacity: 0; transition: opacity 600ms ease; }
.slide.active { opacity: 1; }
.slide img { width: 100%; height: 100%; object-fit: cover; display: block; }

.nav{
  position:absolute; top:50%; transform:translateY(-50%);
  width:44px; height:44px; border-radius:999px;
  border:1px solid rgba(15,23,42,0.12);
  background: rgba(255,255,255,0.85);
  color: var(--text);
  font-size:28px; line-height:40px;
  cursor:pointer;
  box-shadow: 0 8px 18px rgba(2,6,23,.10);
}
.nav:hover{ background: rgba(255,255,255,0.95); }
.nav.prev{ left:12px; }
.nav.next{ right:12px; }
.publications ol {
  font-size: 1.2rem;
  line-height: 2;
}
.dots{
  position:absolute; left:50%; transform:translateX(-50%);
  bottom:10px; display:flex; gap:8px; padding:8px 10px;
  background: rgba(255,255,255,0.80);
  border:1px solid rgba(15,23,42,0.10);
  border-radius:999px;
}
.dot{
  width:10px; height:10px; border-radius:999px; border:none;
  background: rgba(15,23,42,0.25); cursor:pointer;
}
.dot.active{ background: var(--accent); }

.navbar{
  background:#ffffff;
  border-bottom:1px solid var(--line);
  position:sticky;
  top:0;
  z-index:1000;
}

.nav-inner{
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.nav-brand{
  font-weight:600;
  font-size:1.05rem;
  color:var(--text);
}

.nav-links{
  display:flex;
  gap:18px;
}

.nav-links a{
  color:var(--muted);
  font-weight:500;
  transition:0.2s;
}

.nav-links a:hover{
  color:var(--accent);
}
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