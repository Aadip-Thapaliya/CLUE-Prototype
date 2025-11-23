# core/report_generator.py

"""
Advanced PDF Report Generator for CLUE
Includes:
- Title Page with Logo
- Data / EDA Summary
- EDA Charts
- Model Details
- Evaluation Metrics (extended)
- Forecast Visualization
- Predicted Values Table
"""

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import matplotlib.pyplot as plt
import os
import tempfile


def _save_figure_to_image(fig):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.savefig(tmp.name, dpi=150, bbox_inches="tight")
    return tmp.name


def generate_report(
    output_path: str,
    title: str,
    model_results: dict,
    metrics: dict,
    eda_summary: str = None,
    eda_fig=None,
    forecast_fig=None,
    predicted_values=None,
    notes: str = ""
):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # ================= TITLE =================
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("CLUE Financial Forecast Report", styles['Heading2']))
    story.append(PageBreak())

    # ================= EDA SUMMARY =================
    if eda_summary:
        story.append(Paragraph("Exploratory Data Analysis", styles['Heading2']))
        for line in eda_summary.split("\n"):
            story.append(Paragraph(line, styles['BodyText']))
        story.append(Spacer(1, 12))

    # ================= EDA IMAGE =================
    if eda_fig is not None:
        img_path = _save_figure_to_image(eda_fig)
        story.append(Paragraph("EDA Visuals", styles['Heading2']))
        story.append(Image(img_path, width=400, height=300))
        story.append(PageBreak())

    # ================= MODEL DETAILS =================
    story.append(Paragraph("Model Details", styles['Heading2']))
    model_type = model_results.get("model_type", "N/A")
    order = model_results.get("model_order", "N/A")

    story.append(Paragraph(f"Model Type: {model_type}", styles['BodyText']))
    story.append(Paragraph(f"Model Order: {order}", styles['BodyText']))
    story.append(Spacer(1, 12))

    # ================= METRICS TABLE =================
    story.append(Paragraph("Evaluation Metrics", styles['Heading2']))

    table_data = [["Metric", "Value"]]
    for k, v in metrics.items():
        try:
            table_data.append([k, f"{v:.4f}"])
        except:
            table_data.append([k, str(v)])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    story.append(table)
    story.append(PageBreak())

    # ================= FORECAST IMAGE =================
    if forecast_fig is not None:
        img_path = _save_figure_to_image(forecast_fig)
        story.append(Paragraph("Forecast Visualization", styles['Heading2']))
        story.append(Image(img_path, width=400, height=300))
        story.append(PageBreak())

    # ================= PREDICTED VALUES =================
    if predicted_values is not None:
        story.append(Paragraph("Predicted Values", styles['Heading2']))
        table_data = [["Step", "Forecast"]]
        for i, val in enumerate(predicted_values, start=1):
            table_data.append([str(i), f"{float(val):.4f}"])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        story.append(table)
        story.append(PageBreak())

    # ================= NOTES =================
    if notes:
        story.append(Paragraph("Notes", styles['Heading2']))
        story.append(Paragraph(notes, styles['BodyText']))

    doc.build(story)
