import requests
import streamlit as st  # 👈 記得 import streamlit

def send_telegram_msg(text):
    """
    將文字訊息推播至 Telegram
    """
    # 🔐 改成透過 Streamlit secrets 安全讀取，再也不怕外洩！
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown" 
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True, "✅ 推播發送成功！請檢查手機。"
    except Exception as e:
        return False, f"❌ 推播發送失敗: {e}"
