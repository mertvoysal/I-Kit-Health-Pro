from pathlib import Path
import re
import unicodedata

from fpdf import FPDF


SOURCE_MD = Path("I-Kit_Project_Summary_Mert_Voysal_Updated.md")
TARGET_PDF = Path("I-Kit_Project_Summary_Mert_Voysal_Updated.pdf")


def to_ascii_safe(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    stripped = normalized.encode("ascii", "ignore").decode("ascii")
    return stripped.replace("`", "")


def clean_line(line: str) -> str:
    line = line.strip()
    line = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1 (\2)", line)
    return to_ascii_safe(line)


def write_markdown_to_pdf(source_path: Path, target_path: Path) -> None:
    lines = source_path.read_text(encoding="utf-8").splitlines()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()
    pdf.set_left_margin(16)
    pdf.set_right_margin(16)
    pdf.set_font("Helvetica", size=11)

    def mc(height: int, text: str) -> None:
        pdf.multi_cell(0, height, text, new_x="LMARGIN", new_y="NEXT")

    for raw_line in lines:
        line = clean_line(raw_line)

        if not line:
            pdf.ln(4)
            continue

        if line.startswith("---"):
            pdf.ln(2)
            continue

        if line.startswith("# "):
            pdf.set_font("Helvetica", style="B", size=16)
            mc(9, line[2:].strip())
            pdf.ln(1)
            pdf.set_font("Helvetica", size=11)
            continue

        if line.startswith("## "):
            pdf.set_font("Helvetica", style="B", size=13)
            mc(8, line[3:].strip())
            pdf.ln(1)
            pdf.set_font("Helvetica", size=11)
            continue

        if line.startswith("- "):
            mc(7, f"- {line[2:].strip()}")
            continue

        mc(7, line)

    pdf.output(str(target_path))


if __name__ == "__main__":
    if not SOURCE_MD.exists():
        raise FileNotFoundError(f"Source markdown file not found: {SOURCE_MD}")

    write_markdown_to_pdf(SOURCE_MD, TARGET_PDF)
    print(f"PDF exported: {TARGET_PDF.resolve()}")
