from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import HRFlowable, Image, Paragraph, SimpleDocTemplate, Spacer


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
SOURCE_MD = PROJECT_ROOT / "I-Kit_Health_Project_Profile.md"
TARGET_PDF = PROJECT_ROOT / "I-Kit_Health_Project_Profile.pdf"
CURRENT_SNAPSHOT_PATHS = [
    PROJECT_ROOT / "docs" / "images" / "current-snapshot-1.png",
    PROJECT_ROOT / "docs" / "images" / "current-snapshot-2.png",
]


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ProfileTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0B1C3D"),
            alignment=TA_LEFT,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ProfileMeta",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#44536B"),
            alignment=TA_LEFT,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ProfileHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#12284A"),
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ProfileBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1F2A37"),
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ProfileBullet",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1F2A37"),
            leftIndent=12,
            bulletIndent=2,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ProfileNote",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=13,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#5B6470"),
            spaceBefore=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SnapshotCaption",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=13,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#5B6470"),
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    return styles


def _parse_markdown(md_text: str):
    lines = md_text.splitlines()
    story_items = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            story_items.append(("spacer", None))
            continue
        if stripped == "---":
            story_items.append(("rule", None))
            continue
        if stripped.startswith("# "):
            story_items.append(("title", stripped[2:].strip()))
            continue
        if stripped.startswith("## "):
            story_items.append(("heading", stripped[3:].strip()))
            continue
        if stripped.startswith("### "):
            story_items.append(("heading", stripped[4:].strip()))
            continue
        if stripped.startswith("- "):
            story_items.append(("bullet", stripped[2:].strip()))
            continue
        story_items.append(("body", stripped))
    return story_items


def _inline_format(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("**", "<b>", 1).replace("**", "</b>", 1) if text.count("**") >= 2 else text
    while "`" in text:
        parts = text.split("`", 2)
        if len(parts) < 3:
            break
        text = f"{parts[0]}<font name='Courier'>{parts[1]}</font>{parts[2]}"
    return text


def build_pdf():
    if not SOURCE_MD.exists():
        raise FileNotFoundError(f"Source markdown not found: {SOURCE_MD}")

    styles = _build_styles()
    md_text = SOURCE_MD.read_text(encoding="utf-8")
    parsed = _parse_markdown(md_text)

    doc = SimpleDocTemplate(
        str(TARGET_PDF),
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.3 * cm,
        title="I-Kit Health Pro - Project Profile",
        author="Mert Voysal",
    )
    generated_on = datetime.now().strftime("%d %b %Y")

    def draw_footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawString(document.leftMargin, 1.3 * cm, f"Generated: {generated_on}")
        canvas.drawCentredString(A4[0] / 2, 1.3 * cm, "I-Kit Health Pro | Project Profile")
        canvas.drawRightString(A4[0] - document.rightMargin, 1.3 * cm, f"Page {canvas.getPageNumber()}")
        canvas.restoreState()

    story = []
    for item_type, value in parsed:
        if item_type == "title":
            story.append(Paragraph(_inline_format(value), styles["ProfileTitle"]))
            continue
        if item_type == "heading":
            story.append(Paragraph(_inline_format(value), styles["ProfileHeading"]))
            continue
        if item_type == "body":
            if (
                value.startswith("**Applicant:**")
                or value.startswith("**Target Program:**")
                or value.startswith("**Target Use:**")
                or value.startswith("**Project Origin:**")
                or value.startswith("**Role:**")
                or value.startswith("**Date:**")
                or value.startswith("**One-Line Summary:**")
            ):
                story.append(Paragraph(_inline_format(value), styles["ProfileMeta"]))
            else:
                story.append(Paragraph(_inline_format(value), styles["ProfileBody"]))
            continue
        if item_type == "bullet":
            story.append(
                Paragraph(
                    _inline_format(value),
                    styles["ProfileBullet"],
                    bulletText="\u2022",
                )
            )
            continue
        if item_type == "rule":
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.8,
                    color=colors.HexColor("#D6DCE7"),
                    spaceBefore=6,
                    spaceAfter=6,
                )
            )
            continue
        if item_type == "spacer":
            story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Visual annex below includes the current interface snapshots from the latest application state.",
            styles["ProfileNote"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(Paragraph("Current Interface Snapshots", styles["ProfileHeading"]))

    snapshot_idx = 1
    for snapshot_path in CURRENT_SNAPSHOT_PATHS:
        if not snapshot_path.exists():
            continue
        image = Image(str(snapshot_path))
        image._restrictSize(16.2 * cm, 10.2 * cm)
        story.append(image)
        story.append(
            Paragraph(
                f"Figure {snapshot_idx}: Current I-Kit Health Pro interface snapshot.",
                styles["SnapshotCaption"],
            )
        )
        snapshot_idx += 1

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)


if __name__ == "__main__":
    build_pdf()
    print(f"PDF generated: {TARGET_PDF}")
