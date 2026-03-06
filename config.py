import os
import streamlit as st

# 雙棲環境設定：自動判斷是 Streamlit 網頁還是 GitHub 伺服器
try:
    # 1. 如果在 Streamlit 網頁上，去 Secrets 保險箱拿金鑰
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    # 2. 如果出錯了（代表在 GitHub Actions 裡），改去環境變數拿金鑰
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

MODELS = {
    "fact_checker": "gemini-2.5-flash-lite",
    "summarizer": "gemini-2.5-flash-lite" 
}
