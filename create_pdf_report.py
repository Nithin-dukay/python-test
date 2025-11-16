from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import os

print("=" * 80)
print("CREATING PDF VISUALIZATION REPORT")
print("=" * 80)

# Create PDF
pdf_path = './blackbox-analysis/pdfs/data_analysis_report.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

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
    alignment=TA_JUSTIFY
)

# Title Page
elements.append(Spacer(1, 1.5*inch))
title = Paragraph("Retail Sales Data Analysis Report", title_style)
elements.append(title)
elements.append(Spacer(1, 0.3*inch))

subtitle = Paragraph(f"Comprehensive Analysis of 9,994 Orders<br/>Generated on {datetime.now().strftime('%B %d, %Y')}", 
                     ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=colors.grey))
elements.append(subtitle)
elements.append(Spacer(1, 0.5*inch))

# Executive Summary
summary_data = [
    ['Metric', 'Value'],
    ['Total Sales', '$2,297,200.86'],
    ['Total Profit', '$286,397.02'],
    ['Profit Margin', '12.47%'],
    ['Total Orders', '5,009'],
    ['Total Customers', '793'],
    ['Average Order Value', '$458.61'],
    ['Return Rate', '8.00%'],
]

summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 11),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

elements.append(Paragraph("Executive Summary", heading_style))
elements.append(summary_table)
elements.append(PageBreak())

# Add visualizations
viz_dir = './blackbox-analysis/visualization/'
charts = [
    ('01_sales_profit_overview.png', 'Sales and Profit Overview'),
    ('02_time_series_trends.png', 'Time Series Trends'),
    ('03_product_performance.png', 'Product Performance Analysis'),
    ('04_discount_impact.png', 'Discount Impact Analysis'),
    ('05_customer_geographic.png', 'Customer and Geographic Analysis'),
    ('06_shipping_returns.png', 'Shipping and Returns Analysis'),
    ('07_profitability_analysis.png', 'Profitability Analysis'),
    ('08_yearly_comparison.png', 'Year-over-Year Comparison'),
]

for chart_file, chart_title in charts:
    chart_path = os.path.join(viz_dir, chart_file)
    if os.path.exists(chart_path):
        # Add chart title
        elements.append(Paragraph(chart_title, heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add chart image
        img = Image(chart_path, width=7*inch, height=5.25*inch)
        elements.append(img)
        elements.append(PageBreak())
        print(f"  ✓ Added: {chart_title}")
    else:
        print(f"  ⚠ Skipped: {chart_title} (file not found)")

# Build PDF
doc.build(elements)

print("\n" + "=" * 80)
print("✅ PDF REPORT CREATED SUCCESSFULLY!")
print("=" * 80)
print(f"\n📄 Report saved to: {pdf_path}")
print(f"   Total pages: {len(charts) + 1}")
print(f"   File size: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
