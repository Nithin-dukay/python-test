from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os
import glob

print("=" * 80)
print("CREATING PDF VISUALIZATION REPORT")
print("=" * 80)

# Create PDF
pdf_path = './blackbox-analysis/pdfs/visualizations_report.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2E86AB'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#06A77D'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=11,
    spaceAfter=12,
    alignment=TA_LEFT
)

# Title Page
print("\n📄 Creating title page...")
elements.append(Spacer(1, 1.5*inch))
title = Paragraph("Sales Data Analysis Report", title_style)
elements.append(title)
elements.append(Spacer(1, 0.3*inch))

subtitle = Paragraph(f"Comprehensive Business Intelligence Dashboard<br/>Generated: {datetime.now().strftime('%B %d, %Y')}", 
                     ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=colors.grey))
elements.append(subtitle)
elements.append(Spacer(1, 0.5*inch))

# Executive Summary
summary_text = """
<b>Executive Summary:</b><br/>
This report provides a comprehensive analysis of sales data spanning from 2014 to 2017, 
covering 9,994 transactions across multiple product categories, regions, and customer segments. 
The analysis reveals key insights into business performance, profitability trends, and areas 
for strategic improvement.
<br/><br/>
<b>Key Highlights:</b><br/>
• Total Sales: $2.30 Million<br/>
• Total Profit: $286,397<br/>
• Average Profit Margin: 12.03%<br/>
• Total Orders: 5,009<br/>
• Unique Customers: 793<br/>
• Return Rate: 8.00%
"""
elements.append(Paragraph(summary_text, normal_style))
elements.append(PageBreak())

# Get all visualization files
viz_files = sorted(glob.glob('./blackbox-analysis/visualization/*.png'))

print(f"\n📊 Adding {len(viz_files)} visualizations to PDF...")

# Add each visualization with a title
viz_titles = [
    "Time Series Analysis: Sales & Profit Trends",
    "Category Performance Analysis",
    "Regional Performance & Distribution",
    "Discount Impact on Profitability",
    "Shipping & Yearly Performance Analysis",
    "Profit Heatmap by Product Categories",
    "Correlation Analysis of Key Metrics",
    "Statistical Distributions"
]

for idx, (viz_file, viz_title) in enumerate(zip(viz_files, viz_titles), 1):
    print(f"  ✓ Adding chart {idx}: {viz_title}")
    
    # Add section heading
    heading = Paragraph(f"{idx}. {viz_title}", heading_style)
    elements.append(heading)
    elements.append(Spacer(1, 0.2*inch))
    
    # Add image
    img = Image(viz_file, width=7*inch, height=4.5*inch)
    elements.append(img)
    elements.append(Spacer(1, 0.3*inch))
    
    # Add page break after each chart except the last one
    if idx < len(viz_files):
        elements.append(PageBreak())

# Build PDF
print("\n📝 Building PDF document...")
doc.build(elements)

print("\n" + "=" * 80)
print("✅ PDF REPORT CREATED SUCCESSFULLY!")
print("=" * 80)
print(f"\nPDF saved at: {pdf_path}")
print(f"Total pages: ~{len(viz_files) + 1}")
print(f"File size: {os.path.getsize(pdf_path) / (1024*1024):.2f} MB")
