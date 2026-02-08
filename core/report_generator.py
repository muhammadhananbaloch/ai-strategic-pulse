from fpdf import FPDF
from config.settings import Settings
import datetime
import os
import re

class JBSReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_left_margin(15)
        self.set_right_margin(15)

    def sanitize_text(self, text):
        if not isinstance(text, str): return str(text)
        replacements = {
            '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
            '\u2013': '-', '\u2014': '-', '\u2022': '-', '’': "'"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text.encode('latin-1', 'replace').decode('latin-1')

    def clean_markdown(self, text):
        text = text.replace("**", "").replace("__", "")
        text = text.replace("### ", "").replace("## ", "")
        return text

    def header(self):
        # 1. Corporate Top Bar
        self.set_fill_color(0, 86, 210) # JBS Blue
        self.rect(0, 0, 210, 5, 'F')
        self.ln(8)
        
        # 2. Logo & Confidential Marker
        if os.path.exists(Settings.LOGO_PATH):
            try:
                self.image(Settings.LOGO_PATH, 15, 8, 30)
            except Exception: pass
            
        self.set_font('Arial', 'B', 16)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, 'STRATEGIC INTELLIGENCE BRIEF', 0, 1, 'R')
        
        self.set_font('Arial', 'I', 9)
        self.set_text_color(127, 140, 141)
        self.cell(0, 5, f'Generated: {datetime.date.today()} | STRICTLY CONFIDENTIAL', 0, 1, 'R')
        
        self.set_draw_color(200, 200, 200)
        self.line(15, 25, 195, 25)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'JBS Vision 2030 Initiative | Page {self.page_no()}', 0, 0, 'C')

    def draw_score_card(self, score):
        """Draws a premium score indicator."""
        self.ln(5)
        # Background Box
        self.set_fill_color(245, 247, 250) # Light Grey
        self.rect(15, self.get_y(), 180, 25, 'F')
        
        # Label
        self.set_xy(20, self.get_y() + 8)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.cell(65, 10, "Strategic Opportunity Score:", 0, 0)
        
        # Score Value with Dynamic Color
        self.set_font('Arial', 'B', 16)
        if score < 40: self.set_text_color(231, 76, 60) # Red
        elif score < 75: self.set_text_color(241, 196, 15) # Yellow
        else: self.set_text_color(39, 174, 96) # Green
        self.cell(20, 10, f"{score}/100", 0, 1)
        
        # Visual Bar Background
        bar_y = self.get_y() + 2
        self.set_fill_color(220, 220, 220)
        self.rect(20, bar_y, 170, 4, 'F')
        
        # Visual Bar Progress
        if score < 40: self.set_fill_color(231, 76, 60)
        elif score < 75: self.set_fill_color(241, 196, 15)
        else: self.set_fill_color(39, 174, 96)
        
        bar_width = (score / 100) * 170
        self.rect(20, bar_y, bar_width, 4, 'F')
        self.ln(20)

    def section_title(self, title, color=(0, 86, 210)):
        self.ln(5)
        self.set_fill_color(*color)
        self.rect(15, self.get_y(), 2, 8, 'F') # Left accent bar
        
        self.set_xy(18, self.get_y())
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*color)
        self.cell(0, 8, title.upper(), 0, 1)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Arial', '', 10)
        self.set_text_color(60, 60, 60)
        
        text = self.clean_markdown(text)
        text = self.sanitize_text(text)
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            if line.startswith('*') or line.startswith('-'):
                self.set_x(20) # Indent
                self.cell(5, 6, chr(149), 0, 0)
                self.multi_cell(0, 6, line[1:].strip())
            else:
                self.set_x(15)
                self.multi_cell(0, 6, line)
            self.ln(1)
        self.ln(2)

def generate_pdf(unit, score, memo, news):
    pdf = JBSReport()
    pdf.add_page()
    
    # 1. Scorecard
    pdf.draw_score_card(score)
    
    # 2. Executive Summary - FIXED BUFFER LOGIC
    pdf.section_title(f"Strategic Analysis: {unit}")
    
    lines = memo.split('\n')
    current_section = "intro"
    buffer = []

    def flush_buffer(section_type):
        if not buffer: return
        text = "\n".join(buffer)
        
        if section_type == "vision":
             pdf.section_title("Vision 2030 Impact", (0, 86, 210)) # Blue
             pdf.body_text(text)
        elif section_type == "gap":
             pdf.section_title("Competitive Gap Analysis", (192, 57, 43)) # Red
             pdf.body_text(text)
        elif section_type == "move":
             pdf.section_title("Strategic Recommendation", (39, 174, 96)) # Green
             pdf.body_text(text) # <--- THIS WAS MISSING! FIXES THE EMPTY SECTION.
        else:
             pdf.body_text(text)
        buffer.clear()

    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Detect Header Switch
        if "VISION 2030" in line.upper() and "IMPACT" in line.upper():
            flush_buffer(current_section)
            current_section = "vision"
            clean_line = line.replace("VISION 2030 IMPACT", "").replace(":", "").replace("🚀", "").strip()
            if clean_line: buffer.append(clean_line)
            
        elif "COMPETITIVE GAP" in line.upper():
            flush_buffer(current_section)
            current_section = "gap"
            clean_line = line.replace("COMPETITIVE GAP", "").replace(":", "").replace("🚩", "").strip()
            if clean_line: buffer.append(clean_line)
            
        elif "WORKS BETTER" in line.upper() or "JBS MOVE" in line.upper():
            flush_buffer(current_section)
            current_section = "move"
            clean_line = line.replace("THE 'WORKS BETTER' MOVE", "").replace("THE JBS MOVE", "").replace(":", "").replace("💡", "").strip()
            if clean_line: buffer.append(clean_line)
            
        else:
            buffer.append(line)
            
    flush_buffer(current_section)

    pdf.ln(5)

    # 3. Market Signals
    pdf.section_title("Critical Market Signals", (0, 86, 210))
    
    for art in news[:8]:
        source = pdf.sanitize_text(art['source']['name'])
        title = pdf.sanitize_text(art['title'])
        
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 6, f"{source}", 0, 1)
        
        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, title)
        pdf.ln(3)
        
    return pdf.output(dest='S').encode('latin-1', 'replace')