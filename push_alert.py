import requests

def send_telegram_msg(text):
    """
    將文字訊息推播至 Telegram
    """
    # 測試階段先將金鑰放在這裡，測試成功後我們再把它移進 Streamlit Secrets 保護
    TELEGRAM_TOKEN = "8705402683:AAHyxOLKZuVjCOTarw6VmsvjBDN3zN8xzEU"
    CHAT_ID = "1211610803"
    
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
