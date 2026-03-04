import streamlit as st

# 透過 Streamlit 的 secrets 管理員來讀取金鑰 (絕對安全)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
NEWS_API_KEY = st.secrets["NEWS_API_KEY"] # 👈 新增這一行

MODELS = {
    "fact_checker": "gemini-3.1-pro",
    "summarizer": "gemini-3.1-flash" 
}
