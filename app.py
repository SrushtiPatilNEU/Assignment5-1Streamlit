import streamlit as st
import requests

# FastAPI endpoint for generating report - make sure to include the path
API_URL = "https://fastapi-app-1057230376331.us-central1.run.app/generate_report"


# Streamlit UI setup with custom style
st.set_page_config(page_title="NVIDIA Research Assistant", page_icon=":bar_chart:", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #0073e6;
            color: white;
            border-radius: 5px;
            padding: 10px 30px;
            font-size: 16px;
            font-weight: bold;
            width: 100%;
        }
        .stTextInput input {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            width: 100%;
        }
        .stSelectbox select {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            width: 100%;
        }
        h1 {
            font-size: 40px;
            color: #0073e6;
            text-align: center;
        }
        h2 {
            color: #2a2a2a;
            text-align: center;
        }
        .report-section {
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        .stSelectbox, .stTextInput, .stButton {
            margin-bottom: 15px;
        }
        footer {
            text-align: center;
            font-size: 14px;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.title("NVIDIA Research Assistant :bar_chart:")
    st.write("This tool generates comprehensive NVIDIA research reports by leveraging financial data, historical performance, and real-time web insights.")
    st.write("---")

    st.subheader("Research Query")
    query = st.text_area("Enter your research query", height=150)
    year = st.selectbox("Select Year", [2021, 2022, 2023, 2024, 2025], key="year")
    quarter = st.selectbox("Select Quarter", [1, 2, 3, 4], key="quarter")
    agent = st.selectbox("Select Agent", ["Snowflake Agent", "RAG Agent", "Web Search Agent", "All Agents"], key="agent")

agent_mapping = {
    "Snowflake Agent": "snowflake_agent",
    "RAG Agent": "rag_search",
    "Web Search Agent": "web_search",
    "All Agents": "all_agents"
}

backend_agent = agent_mapping.get(agent, None)


if st.button("Generate Report", use_container_width=True):
    with st.spinner("Generating report, please wait..."):
        payload = {
            "query": query,
            "year": year,
            "quarter": quarter,
            "agent_name": backend_agent  
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                st.header("Generated Research Report")

                # Show full research report (if exists)
                if data.get("report"):
                    st.markdown("### 📄 Report")
                    st.markdown(data["report"], unsafe_allow_html=True)

                if data.get("charts"):
                    st.markdown("### 📊 Chart Data")
                    st.write(data["charts"])

                if data.get("chart_image"):
                    st.markdown("### 📈 Financial Metrics Chart")
                    st.image(data["chart_image"])

                # Show web insights if available (Web Agent / All Agents)
                if data.get("web_insights"):
                    st.markdown("### 🌐 Web Insights")
                    st.write(data["web_insights"])

                if data.get("web_links"):
                    st.markdown("### 🔗 Sources")
                    for link in data["web_links"]:
                        st.markdown(f"[{link}]({link})")

                # Catch fallback
                if not data.get("report") and not data.get("charts"):
                    st.warning("No report or charts found.")
            else:
                st.error(f"❌ Failed to generate report. Status code: {response.status_code}")
                st.error(f"Error details: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {str(e)}")
