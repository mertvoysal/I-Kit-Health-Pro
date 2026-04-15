from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
TARGET_PDF = PROJECT_ROOT / "I-Kit_Health_Application_Summary.pdf"

SCREENSHOT_PATHS = [
    PROJECT_ROOT / "docs" / "images" / "app-overview.png",
    PROJECT_ROOT / "docs" / "images" / "current-snapshot-1.png",
    PROJECT_ROOT / "docs" / "images" / "current-snapshot-2.png",
]


def title(text):
    return Paragraph(text, styles["TitleStyle"])


def heading(text):
    return Paragraph(text, styles["HeadingStyle"])


def body(text):
    return Paragraph(text, styles["BodyStyle"])


def bullets(items):
    return [Paragraph(f"&bull; {item}", styles["BulletStyle"]) for item in items]


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=25,
        textColor=colors.HexColor("#1d2a44"),
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="HeadingStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#253b80"),
        spaceBefore=8,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyStyle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.8,
        leading=15,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletStyle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.6,
        leading=14.5,
        leftIndent=8,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CaptionStyle",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=9.2,
        leading=12,
        textColor=colors.HexColor("#4f5b73"),
        spaceBefore=2,
        spaceAfter=10,
    )
)


def build_pdf():
    TARGET_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(TARGET_PDF),
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title="I-Kit Health Pro - Updated Executive Summary",
        author="Mert Voysal",
    )

    story = []
    story.append(title("I-Kit Health Pro: Updated Executive Summary"))
    story.append(
        body(
            "<b>Prepared for:</b> Data Science MSc Application Portfolio<br/>"
            "<b>Project origin:</b> TUBITAK 2209-A University Students Research Projects Support Program<br/>"
            "<b>Role:</b> Project Manager and Lead Developer &nbsp;&nbsp; <b>Date:</b> 14 April 2026"
        )
    )
    story.append(Spacer(1, 6))

    story.append(heading("1) Project Scope and Objective"))
    story.append(
        body(
            "I-Kit Health Pro is an AI-assisted thyroid decision-support platform that analyzes key lab "
            "markers (TSH, FTI, TT3/T3, TT4, T4U) with demographic inputs to support early risk screening "
            "and specialist routing."
        )
    )
    story.extend(
        bullets(
            [
                "Three-class prediction target: Hyperthyroidism, Hypothyroidism, Healthy",
                "Clinical support design: not an autonomous diagnosis engine",
                "Fast web workflow designed for practical physician-assistant usage",
            ]
        )
    )

    story.append(heading("2) Methodology and System Design"))
    story.extend(
        bullets(
            [
                "Backend: Flask + CatBoost + Scikit-learn + Pandas + NumPy",
                "Hybrid decision strategy: ML probabilities + deterministic medical guardrails",
                "Strict input and threshold validation for biological plausibility and safety",
                "Model artifact workflow with metadata tracking and reproducibility",
            ]
        )
    )

    story.append(heading("3) Evaluation Results (Current Build)"))
    metric_table = Table(
        [
            ["Metric", "Result"],
            ["Accuracy (holdout)", "0.9858"],
            ["Precision macro (holdout)", "0.9341"],
            ["Recall macro (holdout)", "0.8823"],
            ["F1 macro (holdout)", "0.9055"],
            ["5-fold CV Accuracy (mean +/- std)", "0.9855 +/- 0.0025"],
            ["5-fold CV F1 macro (mean)", "0.9170"],
        ],
        colWidths=[8.5 * cm, 6.5 * cm],
    )
    metric_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eefc")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1f3d7a")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8faff")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c7d5f4")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(metric_table)
    story.append(
        body(
            "Evaluation artifacts are reproducible and versioned in the project workspace "
            "(metrics JSON/MD and confusion matrix CSV)."
        )
    )

    story.append(heading("4) Routing Module and Practical Utility"))
    story.extend(
        bullets(
            [
                "Specialist ranking combines department relevance, title/experience score, patient satisfaction, and distance.",
                "Distance engine supports district matrix fallback and live-location road routing.",
                "If route API is unavailable, the system automatically switches to safe distance fallback.",
            ]
        )
    )

    story.append(heading("5) Safety and Clinical Responsibility"))
    story.extend(
        bullets(
            [
                "The interface explicitly states that the tool is a clinical decision-support system, not a diagnosis authority.",
                "Payload and laboratory range checks are enforced before model inference.",
                "Final clinical responsibility remains with licensed healthcare professionals.",
            ]
        )
    )

    story.append(heading("6) Personal Contribution"))
    story.append(
        body(
            "I designed and implemented the end-to-end architecture: data preparation, CatBoost model integration, "
            "guardrail logic, route-aware specialist recommendation, evaluation pipeline, and user-facing decision-support dashboard."
        )
    )

    story.append(heading("7) Visual Appendix"))
    for idx, img_path in enumerate(SCREENSHOT_PATHS, start=1):
        if not img_path.exists():
            continue
        img = Image(str(img_path))
        img._restrictSize(16.5 * cm, 9.4 * cm)
        story.append(img)
        story.append(Paragraph(f"Figure {idx}: Current interface snapshot.", styles["CaptionStyle"]))

    story.append(Spacer(1, 6))
    story.append(
        body(
            "<b>Links:</b> Hugging Face demo and source assets are available in the project portfolio package."
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(f"PDF exported: {TARGET_PDF}")
