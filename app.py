import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aave Wallet Credit Score", layout="centered")

st.title("💳 Aave Credit Scoring Dashboard")
st.markdown("Analyze wallet behavior and risk levels based on Aave V2 transaction data.")

# Load data
df = pd.read_csv("output/wallet_scores_ml.csv")

# Rename wallet addresses to User_1, User_2, ...
wallet_mapping = {addr: f"User_{i+1}" for i, addr in enumerate(df["wallet"].unique())}
df["wallet"] = df["wallet"].map(wallet_mapping)

# Optional: Save to new CSV for reuse
df.to_csv("output/wallet_scores_named.csv", index=False)

# Show score distribution
st.subheader("🔢 Score Distribution")
fig, ax = plt.subplots()
df["predicted_score"].plot.hist(bins=50, edgecolor='black', ax=ax)
ax.set_xlabel("Credit Score")
ax.set_ylabel("Number of Wallets")
st.pyplot(fig)

# Risk Breakdown
st.subheader("🛡️ Risk Category Breakdown")
st.dataframe(df["risk_category"].value_counts().reset_index().rename(columns={'index': 'Risk Level', 'risk_category': 'Wallet Count'}))

# Wallet lookup
st.subheader("🔍 Wallet Lookup")
wallet_input = st.text_input("Enter User_ID( User_1, User_2...)")
if wallet_input:
    result = df[df["wallet"].str.lower() == wallet_input.lower()]
    if not result.empty:
        st.success(f"Score: {result.iloc[0]['predicted_score']:.2f} | Risk: {result.iloc[0]['risk_category']}")
    else:
        st.warning("Wallet not found.")
        

