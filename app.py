import streamlit as st
import plotly.graph_objects as go
from core.news_client import NewsClient
from core.engine import StrategicEngine
from core.report_generator import generate_pdf
from config.settings import Settings

st.set_page_config(page_title="JBS Global Radar", layout="wide")

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

def create_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = score,
        title = {'text': "Global Innovation Alignment", 'font': {'color': Settings.JBS_BLUE, 'size': 20}},
        gauge = {
            'bar': {'color': Settings.JBS_TEAL},
            'axis': {'range': [0, 100], 'tickcolor': Settings.JBS_BLUE},
            'steps': [{'range': [0, 50], 'color': "#FF6B6B"}, {'range': [50, 85], 'color': "#FFCC00"}, {'range': [85, 100], 'color': "#00BFA5"}]
        }
    ))
    fig.update_layout(height=280, margin=dict(t=50, b=10), paper_bgcolor='rgba(0,0,0,0)')
    return fig

def main():
    try:
        st.sidebar.image(Settings.LOGO_PATH, width="stretch")
    except Exception:
        st.sidebar.warning("Logo not found")

    st.sidebar.header("📡 Global Innovation Radar")
    st.sidebar.info("Select strategic horizons to scan for global best practices.")

    # --- THE NEW DROPDOWN ---
    client = NewsClient()
    available_topics = list(client.STRATEGIC_THEMES.keys())
    
    selected_topics = st.sidebar.multiselect(
        "Select Strategic Focus Areas",
        options=available_topics,
        default=["Banking & FinTech AI"]
    )
    
    run_btn = st.sidebar.button("🚀 Scan Global Signals")

    st.title("🛡️ JBS Global Innovation Radar")
    st.caption("Benchmarking JBS against World-Class Tech Standards")

    # Session State
    if 'analysis_data' not in st.session_state:
        st.session_state.analysis_data = None

    if run_btn and selected_topics:
        with st.spinner(f"Scanning global networks for {', '.join(selected_topics)}..."):
            engine = StrategicEngine()
            
            # Fetch GLOBAL Data
            news = client.fetch_global_innovation(selected_topics)
            score, memo = engine.analyze_global_trends(selected_topics, news)
            
            st.session_state.analysis_data = {
                'unit': ", ".join(selected_topics), # Used as title in PDF
                'news': news,
                'score': score,
                'memo': memo
            }

    # Display Results
    if st.session_state.analysis_data:
        data = st.session_state.analysis_data
        
        pdf_bytes = generate_pdf(data['unit'], data['score'], data['memo'], data['news'])
        st.sidebar.download_button("📄 Download Strategy Brief", data=pdf_bytes, file_name="JBS_Global_Strategy.pdf", mime="application/pdf")
        
        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(f"<div class='metric-box'><b>Strategic Horizon</b><br>{data['unit']}</div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-box'><b>Benchmark</b><br>Global Leaders</div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='metric-box'><b>JBS Ambition</b><br>Market Leader</div>", unsafe_allow_html=True)

        st.plotly_chart(create_gauge(data['score']), width="stretch")
        
        col1, col2 = st.columns([1, 2], gap="large")
        with col1:
            st.subheader("🌍 Global Signals")
            if data['news']:
                for art in data['news'][:5]:
                    st.info(f"**{art['source']['name']}**: {art['title']}")
            else:
                st.warning("No global signals found. Check API.")
        
        with col2:
            st.subheader("📝 Strategic Memo")
            st.markdown(f"<div class='memo-card'>{data['memo']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()