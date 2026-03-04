import requests
from config import NEWS_API_KEY

def fetch_us_iran_news():
    """
    透過 NewsAPI 抓取關於美伊衝突的最新新聞。
    """
    # 關鍵字設定為美國、伊朗與軍事/衝突相關，按發布時間排序，抓取前 5 筆
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=Iran AND (US OR military OR strike OR conflict)&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"pageSize=5&"
        f"apiKey={NEWS_API_KEY}"
    )
    
    try:
        response = requests.get(url)
        response.raise_for_status() # 如果發生 401 錯誤(金鑰無效)會自動拋出例外
        data = response.json()
        
        news_list = []
        for article in data.get("articles", []):
            # 將時間格式稍微清理一下 (原本是 2024-03-04T14:00:00Z)
            clean_time = article.get("publishedAt", "未知時間")[:16].replace("T", " ")
            
            # 組合標題與摘要作為情報內容
            title = article.get("title", "無標題")
            description = article.get("description", "無內文摘要")
            content = f"【{title}】{description}"
            
            news_list.append({
                "time": clean_time,
                "source": article.get("source", {}).get("name", "未知來源"),
                "content": content
            })
            
        return news_list
        
    except Exception as e:
        return [{"time": "Error", "source": "系統提示", "content": f"NewsAPI 抓取失敗: {e}"}]
