import streamlit as st
import time
from ai_core import fact_check_news

st.set_page_config(page_title="美伊衝突即時情報站", layout="wide")
st.title("🌍 衝突情報即時監控與 AI 事實查核")

# 模擬從 NewsAPI 或 Telegram 抓下來的 raw data (包含極端假消息與正常新聞)
mock_news_stream = [
    {"time": "14:00", "source": "匿名 Telegram 頻道", "content": "快訊！美軍已經發射核彈摧毀德黑蘭！第三次世界大戰爆發！"},
    {"time": "14:15", "source": "Reuters (路透社)", "content": "美國國防部證實，已向波斯灣增派兩艘驅逐艦以應對區域緊張局勢。"},
    {"time": "14:30", "source": "社群媒體 X 網軍帳號", "content": "伊朗總統宣布即將解散所有武裝部隊，並準備向美軍無條件投降！"}
]

st.subheader("即時情報流即時過濾")
st.caption("系統將自動攔截邏輯明顯錯誤或缺乏具體根據的極端消息。")

if st.button("開始抓取最新情報"):
    for news in mock_news_stream:
        # 使用 st.container 把每則新聞包起來，讓版面更整齊
        with st.container():
            st.markdown(f"### 🕒 {news['time']} | 來源: `{news['source']}`")
            st.write(f"**原始情報：** {news['content']}")
            
            with st.spinner("🕵️‍♂️ 事實查核 Agent 分析中..."):
                time.sleep(1) # 模擬網路請求與處理時間
                result = fact_check_news(news["content"])
                
                if result.get("is_credible"):
                    st.success(f"✅ **發布許可 (評估可信):** {result.get('reason')}")
                    # 在這裡可以把資料存進 DataFrame 或是畫在地圖上
                else:
                    st.error(f"❌ **已攔截 (判定可疑):** {result.get('reason')}")
        st.divider()
