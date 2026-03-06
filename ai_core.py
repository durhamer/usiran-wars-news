import google.generativeai as genai
from config import GEMINI_API_KEY, MODELS
import json

# 設定 Gemini API 金鑰
genai.configure(api_key=GEMINI_API_KEY)

def fact_check_news(news_text):
    """
    接收新聞文本，透過 AI 判斷其邏輯與事實可信度，並同時進行「危機評分」。
    強制回傳 JSON 格式以利程式解析。
    """
    model_name = MODELS["fact_checker"]
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    你是一個專業的地緣政治情報分析師與事實查核員。
    請分析以下關於地緣衝突（如美伊衝突、中東局勢或川普發言）的資訊。
    
    資訊內容：
    {news_text}
    
    請以 JSON 格式回傳，必須包含以下四個欄位：
    - "is_credible": 布林值 (true 或 false，判斷是否有明顯邏輯漏洞或極端假消息)
    - "reason": 字串 (解釋判斷原因，繁體中文，簡短一句話)
    - "threat_level": 整數 (1到10分。評估此事件對全球軍事局勢、總體經濟、或科技與半導體供應鏈的衝擊程度。1分代表尋常口水戰，7分以上代表實質制裁或衝突升溫，10分代表爆發全面戰爭或斷鏈危機)
    - "is_critical": 布林值 (當 threat_level 大於等於 7 時為 true，否則為 false)
    """
    try:
        # 強制鎖定輸出格式為 JSON，避免解析崩潰
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        # 發生錯誤時的安全預設值
        return {
            "is_credible": False, 
            "reason": f"AI 查核程序發生錯誤: {e}", 
            "threat_level": 0, 
            "is_critical": False
        }

def summarize_news(news_text, source_name="未知來源"):
    """
    接收英文新聞內容與來源，透過較快速的 Flash 模型進行繁體中文摘要與媒體立場簡評。
    """
    model_name = MODELS["summarizer"]
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    請扮演專業的情報分析師，將以下英文地緣政治新聞進行「繁體中文」摘要，並針對其新聞來源進行「立場簡評」。
    
    請嚴格依照以下格式輸出：

    【情報摘要】：
    請用 2 到 3 個重點條列（bullet points）呈現最核心的「人、事、時、地、物」及對局勢的影響。

    【媒體立場與背景簡評】：
    新聞來源是：「{source_name}」。
    請根據你對該媒體機構（或新聞內容中提及之作者）的了解，用 1 到 2 句話客觀評估其常見的政治立場、背後屬性（例如：西方主流媒體、親美/親伊立場、中東國家官媒、商業財經媒體等），以及閱讀此報導時應注意的潛在偏見或風向。

    新聞內容：
    {news_text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"摘要生成失敗: {e}"
