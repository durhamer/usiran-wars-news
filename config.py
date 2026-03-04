import os

# API Keys (建議在正式環境中使用 Streamlit secrets 或環境變數)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "你的_GEMINI_API_KEY_填這裡")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "你的_NEWS_API_KEY_填這裡")

# 統一管理不同 Agent 使用的 AI 模型
MODELS = {
    "fact_checker": "gemini-3.1-pro", # 需要較強的邏輯推理能力來查核事實
    "summarizer": "gemini-3.1-flash"  # 若未來擴充新聞摘要功能，可用較快速的模型
}
