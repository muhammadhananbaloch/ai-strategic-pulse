import streamlit as st
import plotly.graph_objects as go
from core.news_client import NewsClient
from core.engine import StrategicEngine
from config.settings import Settings

st.set_page_config(page_title="JBS Strategic Command", layout="wide")

# Custom JBS Boardroom CSS
st.markdown(f"""
    <style>
    .main {{ background-color: #F8F9FB; }}
    .stButton>button {{
        background: linear-gradient(135deg, {Settings.JBS_BLUE} 0%, {Settings.JBS_TEAL} 100%);
        color: white; border-radius: 8px; font-weight: 700; padding: 0.8rem;
    }}
    .memo-card {{
        background-color: white; border-radius: 12px; padding: 25px;
        border-top: 10px solid {Settings.JBS_TEAL}; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        color: #2D3436; font-size: 1.1rem; line-height: 1.6;
    }}
    .metric-box {{
        background: {Settings.JBS_BLUE}; color: white; padding: 15px;
        border-radius: 10px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- MISSING FUNCTION ADDED HERE ---
def create_gauge(score):
    """Generates the Strategic Opportunity Gauge for JBS Executives."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", 
        value = score,
        title = {'text': "Strategic Opportunity Score", 'font': {'color': Settings.JBS_BLUE, 'size': 20}},
        gauge = {
            'bar': {'color': Settings.JBS_TEAL},
            'axis': {'range': [0, 100], 'tickcolor': Settings.JBS_BLUE},
            'steps': [
                {'range': [0, 40], 'color': "#FF6B6B"},
                {'range': [40, 75], 'color': "#FFCC00"},
                {'range': [75, 100], 'color': "#00BFA5"}
            ],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig.update_layout(height=280, margin=dict(t=50, b=10), paper_bgcolor='rgba(0,0,0,0)')
    return fig
# -----------------------------------

def main():
    # Sidebar logo handling
    try:
        st.sidebar.image(Settings.LOGO_PATH, width="stretch")
    except Exception:
        st.sidebar.warning("Logo not found in assets/logos/")

    unit = st.sidebar.selectbox("Business Unit", Settings.SUB_COMPANIES)
    run_btn = st.sidebar.button("🚀 Analyze Competitive Gaps")

    st.title("🛡️ JBS Strategic Intelligence Command Center")
    st.caption("Strategic Market Scanning | Vision 2030 Alignment")

    if run_btn:
        with st.spinner("JBS AI is synthesizing competitive intelligence..."):
            # Instantiate classes
            client = NewsClient()
            engine = StrategicEngine()
            
            # Fetch and Analyze
            news = client.fetch_market_news(unit)
            score, memo = engine.analyze_market_intelligence(unit, news)
            
            # Row 1: The "Boardroom" Metrics
            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f"<div class='metric-box'><b>Vision 2030 Goal</b><br>PKR 100B</div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div class='metric-box'><b>Focus Market</b><br>KSA / Global</div>", unsafe_allow_html=True)
            with m3: st.markdown(f"<div class='metric-box'><b>Core Pivot</b><br>AI & Computer Vision</div>", unsafe_allow_html=True)

            # Row 2: The Gauge (Function now exists!)
            st.plotly_chart(create_gauge(score), use_container_width=True)
            
            # Row 3: Deep Dive Analysis
            col1, col2 = st.columns([1, 2], gap="large")
            with col1:
                st.subheader("📡 Filtered Market Signals")
                if news:
                    for art in news[:4]:
                        st.info(f"**{art['source']['name']}**: {art['title']}")
                else:
                    st.info("Scanning for external signals...")
            
            with col2:
                st.subheader("📝 Strategic Memo")
                st.markdown(f"<div class='memo-card'>{memo}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()