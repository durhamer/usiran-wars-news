import requests

# 你的 Telegram Bot 金鑰與對話 ID (目前先放這裡測試，確認沒問題後我們再把它移進 Secrets 保護起來)
TELEGRAM_TOKEN = "8705402683:AAHyxOLKZuVjCOTarw6VmsvjBDN3zN8xzEU"
CHAT_ID = "1211610803"

def send_telegram_msg(text):
    """
    將文字訊息推播至 Telegram
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # 準備發送的資料，開啟 Markdown 模式讓文字可以有粗體等排版
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown" 
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("✅ Telegram 推播成功！")
        return True
    except Exception as e:
        print(f"❌ Telegram 推播失敗: {e}")
        return False

# 本地端直接執行這個檔案時，會觸發下面的測試程式
if __name__ == "__main__":
    test_message = "🚨 **戰情室測試**\n\n指揮官您好，您的專屬情報推播系統已連線成功！等待進一步指示。"
    send_telegram_msg(test_message)
