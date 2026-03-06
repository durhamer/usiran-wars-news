import requests
from config import NEWS_API_KEY

def fetch_custom_news(query_keyword):
    """
    根據傳入的關鍵字，動態抓取相關新聞。
    """
    url = "https://newsapi.org/v2/everything"
    
    # 使用字典管理參數，requests 會自動幫我們組裝並處理特殊字元的 URL 編碼
    params = {
        "q": query_keyword,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        data = response.json()
        
        news_list = []
        # ... 前面的程式碼保持不變 ...
        for article in data.get("articles", []):
            clean_time = article.get("publishedAt", "未知時間")[:16].replace("T", " ")
            title = article.get("title", "無標題")
            description = article.get("description", "無內文摘要")
            content = f"【{title}】{description}"
            
            # 👇 新增這一行來抓取原文連結
            article_url = article.get("url", "#") 
            
            news_list.append({
                "time": clean_time,
                "source": article.get("source", {}).get("name", "未知來源"),
                "content": content,
                "url": article_url # 👇 將網址存入字典
            })
# ... 後面的程式碼保持不變 ...
            
        return news_list
        
    except Exception as e:
        return [{"time": "Error", "source": "系統提示", "content": f"NewsAPI 抓取失敗: {e}"}]
