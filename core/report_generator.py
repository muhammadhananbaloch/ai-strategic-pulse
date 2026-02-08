from fpdf import FPDF
from config.settings import Settings
import datetime
import os

class JBSReport(FPDF):
    def header(self):
        # JBS Logo
        if os.path.exists(Settings.LOGO_PATH):
            self.image(Settings.LOGO_PATH, 10, 8, 33)
        
        # Title
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 86, 210) # JBS Blue
        self.cell(0, 10, 'Strategic Intelligence Brief', 0, 1, 'R')
        
        # Date & Confidentiality
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Generated: {datetime.date.today()} | CONFIDENTIAL', 0, 1, 'R')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'JBS Vision 2030 | Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(0, 191, 165) # JBS Teal
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, f"  {label}", 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, body)
        self.ln()

def generate_pdf(unit, score, memo, news):
    pdf = JBSReport()
    pdf.add_page()
    
    # 1. Executive Summary
    pdf.chapter_title(f"Strategic Gap Analysis: {unit}")
    
    # Clean the markdown symbols for the PDF text
    clean_memo = memo.replace("**", "").replace("#", "").replace("🚩", "[!]").replace("💡", "[IDEATION]").replace("🚀", "[GOAL]")
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"Opportunity Score: {score}/100", 0, 1)
    pdf.ln(2)
    pdf.chapter_body(clean_memo)
    
    # 2. Market Signals
    pdf.chapter_title("Critical Market Signals")
    for art in news[:5]:
        # Handle encoding issues for PDF
        title = art['title'].encode('latin-1', 'replace').decode('latin-1')
        source = art['source']['name'].encode('latin-1', 'replace').decode('latin-1')
        
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 5, f"{source}:", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, title)
        pdf.ln(2)
        
    return pdf.output(dest='S').encode('latin-1')