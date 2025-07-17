import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_CSV = "output/wallet_scores.csv"

if not os.path.exists(INPUT_CSV):
    print("❌ Output CSV not found. Run credit_score.py first.")
    exit()

# Load CSV
df = pd.read_csv(INPUT_CSV)
print(f"📊 Loaded {len(df)} wallet scores")

# Basic Stats
print("\n💡 Score Summary:")
print(df["score"].describe())

# Create histogram
plt.figure(figsize=(10, 6))
sns.histplot(df["score"], bins=50, kde=True, color="skyblue")
plt.title("Distribution of Wallet Credit Scores")
plt.xlabel("Score")
plt.ylabel("Number of Wallets")
plt.grid(True)
plt.tight_layout()
plt.savefig("output/score_distribution.png")
plt.close()

print("✅ Distribution plot saved as output/score_distribution.png")
