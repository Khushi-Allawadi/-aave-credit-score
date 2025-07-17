import json
import os
import pandas as pd
from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor

INPUT_FILE = "data/user-wallet-transactions.json"
OUTPUT_FILE = "output/wallet_scores_ml.csv"

if not os.path.exists(INPUT_FILE):
    print(f"❌ File not found: {INPUT_FILE}")
    exit()

# Load JSON
with open(INPUT_FILE, "r") as f:
    data = json.load(f)

if not data or not isinstance(data, list):
    print("❌ Invalid JSON format")
    exit()

print(f"📦 Loaded {len(data)} transactions")

# Feature extraction
wallet_actions = defaultdict(lambda: {
    "deposits": 0,
    "borrows": 0,
    "repays": 0,
    "redeems": 0,
    "liquidations": 0
})

for txn in data:
    wallet = txn.get("userWallet") or txn.get("actionData", {}).get("userId")
    if not wallet:
        continue
    action = txn.get("action", "").lower()
    if action == "deposit":
        wallet_actions[wallet]["deposits"] += 1
    elif action == "borrow":
        wallet_actions[wallet]["borrows"] += 1
    elif action == "repay":
        wallet_actions[wallet]["repays"] += 1
    elif action == "redeemunderlying":
        wallet_actions[wallet]["redeems"] += 1
    elif action == "liquidationcall":
        wallet_actions[wallet]["liquidations"] += 1

# Manual score (to train ML model)
wallet_features = []
for wallet, actions in wallet_actions.items():
    score = (
        actions["deposits"] * 2 +
        actions["repays"] * 1.5 -
        actions["borrows"] * 1 +
        actions["redeems"] * 1.2 -
        actions["liquidations"] * 10
    )
    score = max(0, min(int(score * 10), 1000))  # Clamp between 0 and 1000
    wallet_features.append({
        "wallet": wallet,
        "deposits": actions["deposits"],
        "borrows": actions["borrows"],
        "repays": actions["repays"],
        "redeems": actions["redeems"],
        "liquidations": actions["liquidations"],
        "score": score
    })

df = pd.DataFrame(wallet_features)

# Train/Test Split
X = df[["deposits", "borrows", "repays", "redeems", "liquidations"]]
y = df["score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models to test
models = {
    "LinearRegression": LinearRegression(),
    "XGBoost": XGBRegressor(objective="reg:squarederror", n_estimators=100, random_state=42),
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42)
}

best_model = None
best_score = -float("inf")
final_preds = None

# Compare models
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"📊 {name} | MAE: {mae:.2f} | R²: {r2:.2f}")
    
    if r2 > best_score:
        best_score = r2
        best_model = model
        final_preds = model.predict(X)

# Save predictions from best model
df["predicted_score"] = final_preds
df["predicted_score"] = df["predicted_score"].clip(0, 1000).round(2)

def classify_risk(score):
    if score >= 700:
        return "Low"
    elif score >= 400:
        return "Medium"
    else:
        return "High"

df["risk_category"] = df["predicted_score"].apply(classify_risk)
df[["wallet", "predicted_score", "risk_category"]].to_csv(OUTPUT_FILE, index=False)

print(f"✅ ML-based scores saved to: {OUTPUT_FILE}")
