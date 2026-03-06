import feedparser
import urllib.parse

def fetch_custom_news(query_keyword):
    """
    使用 Google News RSS 抓取真正「即時」的關鍵字新聞。
    """
    # 為了讓結果更新鮮，我們在關鍵字後面偷偷加上 when:1d (只抓過去 24 小時內)
    search_query = f"{query_keyword} when:1d"
    
    # 將關鍵字轉換成網址看得懂的格式 (URL Encoding)
    encoded_query = urllib.parse.quote(search_query)
    
    # Google News RSS 的神奇網址 (設定為英文語系以獲取國際第一手情報)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        # 讀取並解析 RSS
        feed = feedparser.parse(rss_url)
        news_list = []
        
        # 只抓取最新發布的前 5 則新聞
        for entry in feed.entries[:5]:
            # RSS 的時間格式通常長這樣："Fri, 06 Mar 2026 12:00:00 GMT"，我們取前面這段就好
            clean_time = entry.published[:25] 
            
            # Google News 的標題通常包含了來源，例如："XXX happened - Reuters"
            title = entry.title
            article_url = entry.link
            
            news_list.append({
                "time": clean_time,
                "source": getattr(entry, 'source', {}).get('title', 'Google News'), # 嘗試抓取來源標籤
                "content": f"【最新快訊】{title}", # RSS 的摘要有時帶有雜亂的 HTML，對於快訊來說，標題通常就足以讓 AI 判斷了
                "url": article_url
            })
            
        return news_list
        
    except Exception as e:
        return [{"time": "Error", "source": "系統提示", "content": f"即時 RSS 抓取失敗: {e}", "url": "#"}]
