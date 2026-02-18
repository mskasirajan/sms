"""
PDF generation utility using ReportLab.
Generates student report cards as PDF files.
"""
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)


def generate_report_card_pdf(
    school_name: str,
    student_name: str,
    admission_no: str,
    class_name: str,
    exam_name: str,
    academic_year: str,
    subject_marks: list[dict],   # [{"subject": str, "marks": float, "max": float, "grade": str}]
    total_marks: float,
    total_max: float,
    percentage: float,
    grade: str,
    rank: int,
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("title", parent=styles["Heading1"], alignment=1, fontSize=16)
    sub_style = ParagraphStyle("sub", parent=styles["Normal"], alignment=1, fontSize=11)
    label_style = styles["Normal"]

    elements = []

    elements.append(Paragraph(school_name, title_style))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph(f"Report Card — {exam_name} ({academic_year})", sub_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Student info table
    info_data = [
        ["Student Name:", student_name, "Admission No:", admission_no],
        ["Class:", class_name, "Grade:", grade],
        ["Percentage:", f"{percentage:.2f}%", "Rank:", str(rank) if rank else "N/A"],
    ]
    info_table = Table(info_data, colWidths=[4 * cm, 6 * cm, 4 * cm, 4 * cm])
    info_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5 * cm))

    # Marks table
    marks_header = [["Subject", "Marks Obtained", "Max Marks", "Grade"]]
    marks_data = marks_header + [
        [row["subject"], str(row["marks"]), str(row["max"]), row["grade"] or ""]
        for row in subject_marks
    ]
    marks_data.append(["TOTAL", str(total_marks), str(total_max), grade])

    marks_table = Table(marks_data, colWidths=[8 * cm, 4 * cm, 4 * cm, 2 * cm])
    marks_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4A90D9")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#EAF4FB")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#F5F5F5")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(marks_table)

    doc.build(elements)
    return buffer.getvalue()
