# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

print(">>> model.py 开始执行")

# =========================
# 示例数据（你后续可以换成真实数据）
# =========================
data = {
    "total_assets": [100, 200, 300, 400, 500],
    "total_liabilities": [50, 80, 120, 150, 200],
    "current_ratio": [1.2, 1.5, 1.1, 1.3, 0.9],
    "net_profit": [10, 20, 30, 40, 50],
    "roe": [0.1, 0.15, 0.2, 0.25, 0.3],
    "risk_label": [30, 45, 60, 75, 90]  # 连续风险分数
}

df = pd.DataFrame(data)

# =========================
# 特征（必须和 main.py 完全一致）
# =========================
features = [
    "total_assets",
    "total_liabilities",
    "current_ratio",
    "net_profit",
    "roe"
]

X = df[features]
y = df["risk_label"]

# =========================
# 训练模型（回归）
# =========================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("✅ 模型训练完成")

# =========================
# 保存模型
# =========================
joblib.dump(model, "model.pkl")

print("✅ 模型已保存为 model.pkl")