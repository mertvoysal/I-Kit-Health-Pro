from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import HRFlowable, Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer


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
        canvas.drawString(document.leftMargin, 1.3 * cm, generated_on)
        canvas.drawCentredString(A4[0] / 2, 1.3 * cm, "I-Kit Health Pro | Project Profile")
        canvas.drawRightString(A4[0] - document.rightMargin, 1.3 * cm, f"Page {canvas.getPageNumber()}")
        canvas.restoreState()

    story = []
    i = 0
    while i < len(parsed):
        item_type, value = parsed[i]
        if item_type == "title":
            story.append(Paragraph(_inline_format(value), styles["ProfileTitle"]))
            i += 1
            continue
        if item_type == "heading":
            if value == "Technical Architecture":
                story.append(PageBreak())
            if value == "Routing and Real-World Utility":
                story.append(PageBreak())

            heading_para = Paragraph(_inline_format(value), styles["ProfileHeading"])

            if value == "Technical Architecture":
                # Keep main section title with the first subsection title.
                if i + 1 < len(parsed) and parsed[i + 1][0] == "heading":
                    sub_heading = Paragraph(_inline_format(parsed[i + 1][1]), styles["ProfileHeading"])
                    story.append(KeepTogether([heading_para, sub_heading]))
                    i += 2
                    continue

            # Keep heading with full bullet block when present.
            if i + 1 < len(parsed) and parsed[i + 1][0] == "bullet":
                keep_items = [heading_para]
                j = i + 1
                while j < len(parsed) and parsed[j][0] == "bullet":
                    keep_items.append(
                        Paragraph(
                            _inline_format(parsed[j][1]),
                            styles["ProfileBullet"],
                            bulletText="\u2022",
                        )
                    )
                    j += 1
                story.append(KeepTogether(keep_items))
                i = j
                continue

            # Otherwise keep heading with at least the first content line.
            if i + 1 < len(parsed) and parsed[i + 1][0] == "body":
                next_value = parsed[i + 1][1]
                if (
                    next_value.startswith("**Applicant:**")
                    or next_value.startswith("**Target Program:**")
                    or next_value.startswith("**Target Use:**")
                    or next_value.startswith("**Project Origin:**")
                    or next_value.startswith("**Role:**")
                    or next_value.startswith("**Date:**")
                    or next_value.startswith("**One-Line Summary:**")
                ):
                    next_para = Paragraph(_inline_format(next_value), styles["ProfileMeta"])
                else:
                    next_para = Paragraph(_inline_format(next_value), styles["ProfileBody"])
                story.append(KeepTogether([heading_para, next_para]))
                i += 2
                continue

            story.append(heading_para)
            i += 1
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
            i += 1
            continue
        if item_type == "bullet":
            story.append(
                Paragraph(
                    _inline_format(value),
                    styles["ProfileBullet"],
                    bulletText="\u2022",
                )
            )
            i += 1
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
            i += 1
            continue
        if item_type == "spacer":
            story.append(Spacer(1, 4))
            i += 1

    story.append(Spacer(1, 8))

    snapshot_images = []
    for snapshot_path in CURRENT_SNAPSHOT_PATHS:
        if not snapshot_path.exists():
            continue
        image = Image(str(snapshot_path))
        image._restrictSize(16.2 * cm, 10.2 * cm)
        snapshot_images.append(image)

    if snapshot_images:
        # Keep the section title with the first image.
        story.append(
            KeepTogether(
                [
                    Paragraph("Current Interface Snapshots", styles["ProfileHeading"]),
                    Spacer(1, 4),
                    snapshot_images[0],
                ]
            )
        )
        for image in snapshot_images[1:]:
            story.append(Spacer(1, 8))
            story.append(image)

    added_snapshots = len(snapshot_images)
    if added_snapshots >= 2:
        story.append(
            Paragraph(
                "Figure 1 and Figure 2: Current I-Kit Health Pro interface snapshot.",
                styles["SnapshotCaption"],
            )
        )
    elif added_snapshots == 1:
        story.append(
            Paragraph(
                "Figure 1: Current I-Kit Health Pro interface snapshot.",
                styles["SnapshotCaption"],
            )
        )

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)


if __name__ == "__main__":
    build_pdf()
    print(f"PDF generated: {TARGET_PDF}")
