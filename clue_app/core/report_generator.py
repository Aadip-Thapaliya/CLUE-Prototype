# core/report_generator.py
"""
PDF Report Generator for CLUE using ReportLab.
"""
from reportlab.platypus import Image

from typing import Dict, Optional, List
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    output_path: str,
    title: str,
    model_results: Dict,
    metrics: Dict[str, float],
    notes: Optional[str] = None,
    image_path: Optional[List[str]] = None,
) -> str:
    """
    Generate a simple forecasting report.

    model_results: e.g. {
        "model_type": "AUTO_ARIMA",
        "model_order": (p,d,q),
        "forecast_horizon": 30
    }
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(output), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Model Summary", styles["Heading2"]))
    story.append(Spacer(1, 6))

    model_table_data = [[k, str(v)] for k, v in model_results.items()]
    model_table = Table(model_table_data, hAlign="LEFT")
    model_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(model_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Evaluation Metrics", styles["Heading2"]))
    story.append(Spacer(1, 6))

    metrics_table_data = [["Metric", "Value"]] + [
        [name, f"{value:.4f}"] for name, value in metrics.items()
    ]
    metrics_table = Table(metrics_table_data, hAlign="LEFT")
    metrics_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(metrics_table)
    story.append(Spacer(1, 12))

    if notes:
        story.append(Paragraph("Notes", styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(notes, styles["BodyText"]))
        story.append(Spacer(1, 12))

    # (Optional) charts as images can be added later in GUI layer
    if image_path:
        try:
            story.append(Paragraph("Forecast Plot", styles["Heading2"]))
            story.append(Spacer(1, 6))
            story.append(Image(image_path, width=400, height=250))
            story.append(Spacer(1, 12))
        except Exception:
            # silently ignore image errors for now
            pass

    doc.build(story)
    return str(output)
