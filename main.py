def ai_analysis(data, score, level):
    prompt = f"""
你是专业财务分析师，请分析：

总资产：{data.total_assets}
总负债：{data.total_liabilities}
流动比率：{data.current_ratio}
净利润：{data.net_profit}
ROE：{data.roe}

风险分数：{score}
风险等级：{level}

请给出详细风险分析和改进建议。
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        data_json = response.json()

        # 🔥 关键防护
        if "choices" in data_json:
            return data_json["choices"][0]["message"]["content"]
        else:
            print("AI返回错误：", data_json)
            return "AI分析失败（接口返回异常）"

    except Exception as e:
        print("请求异常：", e)
        return "AI分析失败（请求异常）"