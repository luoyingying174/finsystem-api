from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# =========================
# 📦 历史数据（内存）
# =========================
history_data = []


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
# 🤖 AI分析函数（阿里云通义千问）
# =========================
def ai_analyze(data: RiskInput):
    api_key = os.getenv("ALIYUN_API_KEY")
    print("API KEY:", api_key)

    if not api_key:
        return {
            "risk_score": -1,
            "risk_level": "错误",
            "analysis": ["未配置 API Key"],
            "suggestions": ["请在 Railway 配置 ALIYUN_API_KEY"]
        }

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
你是一名资深财务分析师，请根据以下数据分析企业风险：

总资产: {data.total_assets}
总负债: {data.total_liabilities}
流动比率: {data.current_ratio}
净利润: {data.net_profit}
ROE: {data.roe}

请返回严格JSON格式，包含：
risk_score（0-100）
risk_level（低/中/高风险）
analysis（数组，3-5条分析）
suggestions（数组，3-5条建议）
"""

    payload = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "system", "content": "你是专业财务分析AI"},
                {"role": "user", "content": prompt}
            ]
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)

        print("AI HTTP状态码:", response.status_code)
        print("AI返回原始数据:", response.text)

        if response.status_code != 200:
            return {
                "risk_score": -1,
                "risk_level": "错误",
                "analysis": [f"API调用失败: {response.text}"],
                "suggestions": ["检查 API Key 或网络"]
            }

        result = response.json()

        # ✅ 正确解析通义千问返回
        content = result["output"]["choices"][0]["message"]["content"]

        return {
            "risk_score": 50,
            "risk_level": "AI分析",
            "analysis": [content],
            "suggestions": ["以上为AI生成分析"]
        }

    except Exception as e:
        print("AI调用异常:", str(e))
        return {
            "risk_score": -1,
            "risk_level": "错误",
            "analysis": [str(e)],
            "suggestions": ["检查服务器或API配置"]
        }


# =========================
# 🚀 预测接口
# =========================
@app.post("/predict")
def predict(data: RiskInput):
    result = ai_analyze(data)

    # 保存历史（存评分）
    history_data.append(result.get("risk_score", 0))

    return result


# =========================
# 📊 历史接口
# =========================
@app.get("/history")
def get_history():
    return {
        "history": history_data
    }


# =========================
# 🚀 启动（本地调试）
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)