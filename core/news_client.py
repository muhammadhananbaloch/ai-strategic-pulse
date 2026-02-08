import requests
import streamlit as st
from config.settings import Settings

@st.cache_data(ttl=3600)
def _fetch_news_from_api(query: str, api_key: str):
    # Search for JBS interests: AI in Banking, Manufacturing Automation in Pakistan/KSA
    search_query = f'({query} AND "AI") OR "fintech Pakistan" OR "Saudi Arabia Vision 2030 technology"'
    
    url = f"https://newsapi.org/v2/everything?q={search_query}&sortBy=relevancy&apiKey={api_key}&language=en"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return articles if articles else _get_mock_data(query)
        return _get_mock_data(query)
    except Exception:
        return _get_mock_data(query)

def _get_mock_data(unit):
    """Fallback data to ensure the JBS demo always works."""
    return [
        {"source": {"name": "Industry Intel"}, "title": f"Growth in {unit} sectors observed in KSA market.", "description": "Strategic shifts towards AI integration."},
        {"source": {"name": "Market Watch"}, "title": "Digital Transformation demand surges in Pakistan Banking.", "description": "Cloud-first strategies are becoming mandatory."}
    ]

class NewsClient:
    def __init__(self):
        self.api_key = Settings.NEWS_API_KEY
    def fetch_market_news(self, query: str):
        return _fetch_news_from_api(query, self.api_key)