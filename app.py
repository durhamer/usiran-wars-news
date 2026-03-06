import streamlit as st
from ai_core import fact_check_news, summarize_news
from news_fetcher import fetch_custom_news

st.set_page_config(page_title="地緣衝突情報站", layout="wide")

# --- 側邊欄設定區 ---
with st.sidebar:
    st.header("⚙️ 監控設定")
    
    # 定義不同主題的精準搜尋語法 (Google News 支援的寫法，不需加 AND)
    TOPIC_QUERIES = {
        "美伊軍事衝突": "Iran (US OR military OR strike OR conflict)",
        "霍爾木茲海峽封鎖危機": '"Strait of Hormuz" (blockade OR closure OR attack OR tension OR oil)'
    }
    
    selected_topic = st.selectbox(
        "選擇要監控的戰略目標：",
        options=list(TOPIC_QUERIES.keys())
    )
    
    st.info(f"🔍 目前搜尋語法：\n`{TOPIC_QUERIES[selected_topic]}`")

# --- 主畫面區 ---
st.title("🌍 衝突情報即時監控與 AI 事實查核")
st.subheader(f"當前監控目標：【{selected_topic}】")

if st.button("📡 開始抓取最新情報"):
    # 根據選擇的主題，取出對應的搜尋語法丟給 API
    query_string = TOPIC_QUERIES[selected_topic]
    
    with st.spinner(f"正在連線至 Google News 獲取最新資料...") :
        real_news_stream = fetch_custom_news(query_string)
        
    if not real_news_stream:
        st.warning("目前沒有抓到相關新聞。")
        
    for news in real_news_stream:
        with st.container():
            st.markdown(f"### 🕒 {news['time']} | 來源: `{news['source']}`")
            
            # 檢視原始英文情報的摺疊面板
            with st.expander("🔍 檢視原始英文情報"):
                st.write(news['content'])
            
            with st.spinner("🕵️‍♂️ 事實查核 Agent 分析中..."):
                result = fact_check_news(news["content"])
                
                if result.get("is_credible"):
                    st.success(f"✅ **發布許可:** {result.get('reason')}")
                    
                    # 👇 關鍵更新：傳入 news["source"] 給 AI 進行媒體立場分析
                    with st.spinner("✍️ AI 戰情摘要與媒體簡評生成中..."):
                        summary_text = summarize_news(news["content"], news["source"])
                        st.info(summary_text) 
                        
                    # 加入前往原文的按鈕
                    if "url" in news and news["url"] != "#":
                        st.link_button("🔗 閱讀完整原文", news["url"])
                    
                else:
                    st.error(f"❌ **已攔截:** {result.get('reason')}")
        st.divider()
