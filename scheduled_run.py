import os
import requests
from news_fetcher import fetch_custom_news
from ai_core import fact_check_news, summarize_news

# 讀取 GitHub Actions 設定的環境變數密碼
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_alert(text):
    """專屬背景排程的推播函數"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload).raise_for_status()
    except Exception as e:
        print(f"推播失敗: {e}")

# 定義要排程監控的語法 (與你網頁版相同)
TOPIC_QUERIES = {
    "美伊軍事衝突": "Iran (US OR military OR strike OR conflict)",
    "霍爾木茲海峽封鎖危機": '"Strait of Hormuz" (blockade OR closure OR attack OR tension OR oil)',
    "川普社群動態與發言": 'Trump ("Truth Social" OR tweet OR X OR "social media" OR statement)'
}

def main():
    print("🚀 開始執行背景排程巡邏...")
    
    for topic, query in TOPIC_QUERIES.items():
        print(f"🔍 正在巡邏主題：{topic}")
        news_stream = fetch_custom_news(query)
        
        for news in news_stream:
            result = fact_check_news(news["content"])
            
            # 只有當 AI 判定可信，且威脅等級 >= 7 (is_critical 為 True) 時，才發送推播！
            if result.get("is_credible") and result.get("is_critical"):
                summary_text = summarize_news(news["content"], news.get("source", "未知來源"))
                
                alert_msg = (
                    f"🚨 **【重大地緣情報自動警報】** 🚨\n\n"
                    f"**監控主題**：{topic}\n"
                    f"**威脅等級**：{result.get('threat_level')}/10\n"
                    f"**情報來源**：{news.get('source', '未知')}\n\n"
                    f"**AI 戰略摘要**：\n{summary_text}\n\n"
                    f"[🔗 點擊閱讀原文]({news.get('url', '#')})"
                )
                
                send_alert(alert_msg)
                print(f"⚠️ 已發送【{topic}】的重大警報！")
                
    print("✅ 本次巡邏結束。")

if __name__ == "__main__":
    main()
