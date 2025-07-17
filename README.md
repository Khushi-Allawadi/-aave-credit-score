# 💳 Aave Wallet Credit Scoring System

A machine learning–powered engine that assigns a **credit score (0–1000)** to Ethereum wallets based on their behavior on the Aave V2 DeFi protocol. The higher the score, the more responsible and trustworthy the wallet is.

---

## 🚀 Features

- ✅ Rule-based and ML-based credit scoring  
- ✅ Risk classification: **High / Medium / Low**  
- ✅ Outputs clean CSV files with scores + labels  
- ✅ Streamlit frontend for demo  
- ✅ Jupyter Notebook for analysis + presentation  
- ✅ Plug-and-play CLI script for new datasets

---

## 📊 What Behavior Does It Measure?

Wallets are scored based on their transaction patterns:

| Action             | Interpretation             | Weight    |
|--------------------|-----------------------------|-----------|
| `deposit`          | Positive behavior           | 🟢 +2      |
| `repay`            | Responsible user            | 🟢 +1.5    |
| `redeemunderlying` | Mild positive activity      | 🟢 +1.2    |
| `borrow`           | Slight risk introduced      | 🔴 -1      |
| `liquidationcall`  | Strong negative signal      | 🔴 -10     |

---

## ⚙️ How It Works

### 1️⃣ Prepare the Data
Place your file `user-wallet-transactions.json` inside the `data/` folder.

### 2️⃣ Run the Script
```bash
python3 scripts/credit_score.py

## ✅ Outputs

Once you run the pipeline, you'll get:

- `output/wallet_scores.csv` — Rule-based scores  
- `output/wallet_scores_ml.csv` — ML-based scores + risk categories  

---

## 📓 3️⃣ Explore the Notebook

Want to understand how the ML model works, what features were used, and how risk was categorized?

👉 Open the Jupyter Notebook:
It includes:

- Feature engineering logic  
- Model comparisons (XGBoost, RandomForest, LinearRegression)  
- Visualizations of wallet behavior & scores  
- Performance metrics

---

## 🤖 Model Performance

| Model              | MAE (↓ Better) | R² Score (↑ Better) |
|--------------------|----------------|---------------------|
| **XGBoost**        | **9.55**       | **0.98**            |
| Random Forest      | 10.57          | 0.98                |
| Linear Regression  | 203.62         | -36.66              |

🧠 **XGBoost** wins — lowest error, highest accuracy. It's used for final scoring.

---

> Scoring DeFi wallets like credit bureaus score humans — but without the middlemen.
