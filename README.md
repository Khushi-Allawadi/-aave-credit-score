# 💳 Aave Wallet Credit Scoring System

This project builds a **credit scoring engine for wallets interacting with the Aave V2 DeFi protocol**, based solely on historical transaction behavior. It processes raw transaction-level JSON data and produces a credit score between **0 and 1000** for each wallet, with higher scores indicating reliable, responsible DeFi usage.

---

## 🚀 Features

✅ Rule-based credit scoring logic  
✅ Machine Learning credit scoring (XGBoost, Random Forest, Linear Regression)  
✅ Risk classification: High / Medium / Low  
✅ Wallet score CSV output  
✅ Clean, reproducible project structure  
✅ Jupyter Notebook demo for analysis and interviews

---

## 🧠 What Does the Model Learn?

We analyze and quantify a wallet’s behavior using features like:

- 🟢 `deposits` (positive behavior)
- 🟢 `repays` (strong signal of responsibility)
- 🔴 `borrows` (neutral/negative weight)
- 🟢 `redeems` (mild positive)
- 🔴 `liquidation calls` (very risky behavior)

Each transaction type is weighted, and the total behavior is normalized and scaled to produce a **score from 0 to 1000**.

---

## ⚙️ How It Works

### 1. **Prepare Data**
Place your `user-wallet-transactions.json` file in the `data/` folder.

### 2. **Run the Script**
```bash
python3 scripts/credit_score.py

Outputs will be saved in:
    •    output/wallet_scores.csv — rule-based scores
    •    output/wallet_scores_ml.csv — ML-based scores with risk levels

3. Explore Notebook

For a full walkthrough of the model, scoring logic, and visualizations:

jupyter notebook notebooks/demo_credit_score.ipynb


📊 Model Performance

Model    MAE (Mean Absolute Error)    R² Score
XGBoost    9.55    0.98
Random Forest    10.57    0.98
Linear Regression    203.62    -36.66

 XGBoost was selected as the best model due to its low error and high predictive accuracy.


🚦 Risk Categorization Logic

Score Range    Risk Category    Description
700 - 1000    Low    Highly reliable wallets; good repayment history
400 - 699    Medium    Average risk; some borrowing/redeeming activity
0 - 399    High    Risky behavior, bots, or history of liquidation


aave-credit-score/
├── data/                      # Input transaction JSON file
├── output/                    # CSV outputs (scores + risk)
├── scripts/
│   └── credit_score.py        # One-step CLI script
├── notebooks/
│   └── demo_credit_score.ipynb # Analysis + ML modeling
├── README.md

💡 How to Extend
    •    Add time-based features (e.g., frequency of deposits over time)
    •    Integrate Aave V3 or Compound data
    •    Deploy as a Streamlit web app
    •    Add anomaly detection or bot detection logic
    

👩‍💻 Built By
Khushi – 22 | Aspiring ML/AI Engineer | Passionate about DeFi + Data 🔗
“I’m just getting started, but I’m building to get hired.”
