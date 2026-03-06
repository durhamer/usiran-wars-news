import streamlit as st
from ai_core import fact_check_news, summarize_news
from news_fetcher import fetch_custom_news
from push_alert import send_telegram_msg

st.set_page_config(page_title="地緣衝突情報站", layout="wide")

# --- 側邊欄設定區 ---
with st.sidebar:
    st.header("⚙️ 監控設定")
    
    # 定義不同主題的精準搜尋語法 (Google News 支援的寫法)
    TOPIC_QUERIES = {
        "美伊軍事衝突": "Iran (US OR military OR strike OR conflict)",
        "霍爾木茲海峽封鎖危機": '"Strait of Hormuz" (blockade OR closure OR attack OR tension OR oil)',
        "川普社群動態與發言": 'Trump ("Truth Social" OR tweet OR X OR "social media" OR statement)'
    }
    
    selected_topic = st.selectbox(
        "選擇要監控的戰略目標：",
        options=list(TOPIC_QUERIES.keys())
    )
    
    st.info(f"🔍 目前搜尋語法：\n`{TOPIC_QUERIES[selected_topic]}`")
    
    # --- 系統測試區 ---
    st.divider()
    st.header("🚨 系統測試區")
    if st.button("🔔 測試 Telegram 推播"):
        with st.spinner("正在發送訊號至 Telegram..."):
            success, msg = send_telegram_msg("🚨 **戰情室測試**\n\n指揮官您好，全雲端推播系統已連線成功！等待您的下一步戰術指示。")
            if success:
                st.success(msg)
            else:
                st.error(msg)

# --- 主畫面區 ---
st.title("🌍 衝突情報即時監控與 AI 事實查核")
st.subheader(f"當前監控目標：【{selected_topic}】")

if st.button("📡 開始抓取最新情報"):
    query_string = TOPIC_QUERIES[selected_topic]
    
    with st.spinner(f"正在連線獲取最新資料...") :
        real_news_stream = fetch_custom_news(query_string)
        
    if not real_news_stream:
        st.warning("目前沒有抓到相關新聞。")
        
    for news in real_news_stream:
        with st.container():
            st.markdown(f"### 🕒 {news['time']} | 來源: `{news['source']}`")
            
            with st.expander("🔍 檢視原始英文情報"):
                st.write(news['content'])
            
            with st.spinner("🕵️‍♂️ 事實查核 Agent 分析中..."):
                result = fact_check_news(news["content"])
                
                if result.get("is_credible"):
                    # 顯示發布許可與 AI 給出的威脅評分
                    st.success(f"✅ **發布許可:** {result.get('reason')}  \n⚠️ **系統威脅評級: {result.get('threat_level', 0)}/10**")
                    
                    with st.spinner("✍️ AI 繁中摘要生成中..."):
                        # 將新聞內容與來源一起傳給 AI，讓它進行媒體立場簡評
                        summary_text = summarize_news(news["content"], news.get("source", "未知來源"))
                        st.info(f"**情報摘要與媒體簡評：**\n\n{summary_text}")
                        
                    if "url" in news and news["url"] != "#":
                        st.link_button("🔗 閱讀完整原文", news["url"])
                    
                    # 🚨 核心防禦機制：如果是重大危機 (分數 >= 7)，自動發送 Telegram 警報
                    if result.get("is_critical"):
                        st.error("🚨 偵測到高威脅層級 (>=7)，已同步發送 Telegram 警報！")
                        
                        alert_msg = (
                            f"🚨 **【重大地緣情報警報】** 🚨\n\n"
                            f"**威脅等級**：{result.get('threat_level')}/10\n"
                            f"**情報來源**：{news.get('source', '未知')}\n\n"
                            f"**AI 戰略摘要**：\n{summary_text}\n\n"
                            f"[🔗 點擊閱讀原文]({news.get('url', '#')})"
                        )
                        send_telegram_msg(alert_msg)
                        
                else:
                    st.error(f"❌ **已攔截:** {result.get('reason')}")
        st.divider()
