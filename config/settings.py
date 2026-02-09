import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Model Identifier
    MODEL_ID = "gemini-2.5-flash-lite"
    
    # JBS Brand Colors
    JBS_BLUE = "#0056D2"
    JBS_TEAL = "#00BFA5"
    JBS_DARK = "#1A1A1B"

    # JBS STRATEGIC CONTEXT (Derived from your report)
    JBS_CONTEXT = """
    JBS is a PKR 100B Vision 2030 company transitioning from hardware to 
    AI, Cloud, and Managed Services. Key markets: Pakistan, KSA, North America.
    Subsidiaries: ENA (IoT/Power), Blutech (Data), Hysab Kytab (Fintech).
    Key Verticals: Banking, Manufacturing, Telecom.
    Strategic Pivot: Becoming an AI & Computer Vision leader.
    """

    # COMPETITOR KEYWORDS (Based on your industry report)
    COMPETITORS = ["Systems Ltd", "10Pearls", "Contour Software", "IBM Pakistan"]

    SUB_COMPANIES = [
        "Jaffer Business Systems", 
        "JBS Digital Transformation",
        "JBS Infrastructure",
        "JBS Arabia",
        "JBS Americas & Europe",
        "ENA - An IoT & Power Solutions Company",
        "Blutech - Data Center & Cloud Services",
        "Hysab Kytab - Fintech Solutions"
    ]

    # Path to assets
    ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    LOGO_PATH = os.path.join(ASSETS_DIR, "logos", "jbsgloballive_logo.jpg")