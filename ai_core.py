import google.generativeai as genai
from config import GEMINI_API_KEY, MODELS
import json

genai.configure(api_key=GEMINI_API_KEY)

def fact_check_news(news_text):
    """
    接收新聞文本，透過 AI 判斷其邏輯與事實可信度。
    """
    model_name = MODELS["fact_checker"]
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    你是一個專業的地緣政治情報分析師與事實查核員。
    請分析以下關於美伊衝突的最新資訊。
    判斷這則資訊是否具有明顯的邏輯漏洞、是否為常見的戰爭假消息宣傳，或者是否過於誇大。
    
    請務必只以 JSON 格式回傳，不要有任何其他文字。格式如下：
    {{"is_credible": true或false, "reason": "解釋你的判斷原因（繁體中文，簡短一句話）"}}

    資訊內容：
    {news_text}
    """
    try:
        response = model.generate_content(prompt)
        # 清理可能夾帶的 Markdown 標籤以便解析 JSON
        clean_text = response.text.strip("`").removeprefix("json\n").strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"is_credible": False, "reason": f"AI 查核程序發生錯誤: {e}"}
