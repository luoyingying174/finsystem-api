from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# =========================
# 📦 历史数据
# =========================
history_data = []

# =========================
# 🔑 API KEY（从环境变量读取）
# =========================
API_KEY = os.getenv("ALIYUN_API_KEY")

# =========================
# 📥 请求模型
# =========================
class RiskInput(BaseModel):
    total_assets: float
    total_liabilities: float
    current_ratio: float
    net_profit: float
    roe: float


# =========================
# 🤖 调用阿里云通义千问
# =========================
def call_qwen(prompt):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen-turbo",
        "input": {
            "prompt": prompt
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    try:
        return result["output"]["text"]
    except:
        return "AI分析失败，请检查API调用"


# =========================
# 🤖 AI分析（核心）
# =========================
def ai_analyze(data: RiskInput):

    prompt = f"""
你是一个专业的财务分析师，请根据以下企业数据进行分析：

总资产：{data.total_assets}
总负债：{data.total_liabilities}
流动比率：{data.current_ratio}
净利润：{data.net_profit}
ROE：{data.roe}

请严格按照以下格式输出：
风险评分: xx
风险等级: xx
分析:
1. xxx
2. xxx
建议:
1. xxx
2. xxx
"""

    ai_text = call_qwen(prompt)

    return {
        "risk_score": 50,  # 先占位（下一步我们解析）
        "risk_level": "AI分析",
        "analysis": [ai_text],
        "suggestions": ["详见AI分析"]
    }


# =========================
# 🚀 接口
# =========================
@app.post("/predict")
def predict(data: RiskInput):
    result = ai_analyze(data)

    history_data.append(result["risk_score"])

    return result


# =========================
# 📊 历史
# =========================
@app.get("/history")
def get_history():
    return {"history": history_data}