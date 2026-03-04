import streamlit as st
from ai_core import fact_check_news
from news_fetcher import fetch_us_iran_news # 👈 引入我們的新模組

st.set_page_config(page_title="美伊衝突即時情報站", layout="wide")
st.title("🌍 衝突情報即時監控與 AI 事實查核")

st.subheader("真實情報流即時過濾")
st.caption("系統將自動從全球新聞網抓取最新資料，並攔截邏輯明顯錯誤或缺乏具體根據的極端消息。")

# 更改按鈕名稱
if st.button("📡 開始抓取全球最新情報"):
    
    with st.spinner("正在連線至 NewsAPI 獲取最新資料..."):
        real_news_stream = fetch_us_iran_news()
        
    if not real_news_stream:
        st.warning("目前沒有抓到相關新聞。")
        
    for news in real_news_stream:
        with st.container():
            st.markdown(f"### 🕒 {news['time']} | 來源: `{news['source']}`")
            st.write(f"**原始情報：** {news['content']}")
            
            with st.spinner("🕵️‍♂️ 事實查核 Agent 分析中..."):
                result = fact_check_news(news["content"])
                
                if result.get("is_credible"):
                    st.success(f"✅ **發布許可 (評估可信):** {result.get('reason')}")
                else:
                    st.error(f"❌ **已攔截 (判定可疑):** {result.get('reason')}")
        st.divider()
