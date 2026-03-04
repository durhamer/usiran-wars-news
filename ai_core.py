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

    # 稍微優化 Prompt，讓指令更明確
    prompt = f"""
    你是一個專業的地緣政治情報分析師與事實查核員。
    請分析以下關於美伊衝突的資訊，判斷是否具有明顯邏輯漏洞、或為極端假消息。
    
    資訊內容：
    {news_text}
    
    請以 JSON 格式回傳，必須包含以下兩個欄位：
    - "is_credible": 布林值 (true 或 false)
    - "reason": 字串 (解釋判斷原因，繁體中文，簡短一句話)
    """
    try:
        # 關鍵修改：加上 generation_config 強制鎖定為 application/json
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        # 因為已經強制是 JSON 了，可以直接讀取，不用再做字串清理
        return json.loads(response.text)
    except Exception as e:
        return {"is_credible": False, "reason": f"AI 查核程序發生錯誤: {e}"}
