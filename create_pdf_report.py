"""
PDF Report Generator for Employment Data Analysis
Creates a comprehensive visual PDF dashboard
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
import glob

print("=" * 80)
print("GENERATING PDF DASHBOARD REPORT")
print("=" * 80)

# Create PDF
pdf_path = './blackbox-analysis/pdfs/employment_data_dashboard.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=A4)
story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2C3E50'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#34495E'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

# Title Page
story.append(Paragraph("Employment Data Analysis Dashboard", title_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Business Data Collection (BDC)", styles['Heading2']))
story.append(Paragraph("Comprehensive Analysis Report", styles['Heading3']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Period: 2011 Q2 - 2025 Q2", styles['Normal']))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Total Records: 20,108", styles['Normal']))
story.append(PageBreak())

# Add all visualizations
viz_files = sorted(glob.glob('./blackbox-analysis/visualization/*.png'))

print(f"\n📄 Adding {len(viz_files)} visualizations to PDF...")

for i, viz_file in enumerate(viz_files, 1):
    # Extract chart name from filename
    chart_name = os.path.basename(viz_file).replace('.png', '').replace('_', ' ').title()
    chart_name = chart_name.split(' ', 1)[1] if ' ' in chart_name else chart_name
    
    # Add chart title
    story.append(Paragraph(f"{i}. {chart_name}", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Add image
    img = RLImage(viz_file, width=7*inch, height=5*inch)
    story.append(img)
    story.append(Spacer(1, 0.2*inch))
    
    # Add page break after every chart except the last one
    if i < len(viz_files):
        story.append(PageBreak())
    
    print(f"   ✅ Added: {chart_name}")

# Build PDF
doc.build(story)

print(f"\n✅ PDF Dashboard created successfully!")
print(f"📄 Location: {pdf_path}")
print(f"📊 Total pages: ~{len(viz_files) + 1}")
print("=" * 80)
