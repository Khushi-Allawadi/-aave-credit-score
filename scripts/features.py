
# scripts/features.py

import pandas as pd
from collections import defaultdict

def load_json(path):
    import json
    with open(path, 'r') as f:
        return json.load(f)

def extract_features(data):
    wallets = defaultdict(lambda: {
        "total_deposit": 0,
        "total_borrow": 0,
        "total_repay": 0,
        "liquidation_count": 0,
        "active_days": set()
    })

    for txn in data:
        wallet = txn.get("userWallet")
        action = txn.get("action")
        timestamp = txn.get("timestamp")
        action_data = txn.get("actionData", {})
        
        amount = float(action_data.get("amount", 0))
        price = float(action_data.get("assetPriceUSD", 1))  # default to $1 if missing
        usd_value = amount * price / (10 ** 6)  # USDC is 6 decimals

        if not wallet:
            continue

        # Aggregate data
        if action == "deposit":
            wallets[wallet]["total_deposit"] += usd_value
        elif action == "borrow":
            wallets[wallet]["total_borrow"] += usd_value
        elif action == "repay":
            wallets[wallet]["total_repay"] += usd_value
        elif action == "liquidationcall":
            wallets[wallet]["liquidation_count"] += 1

        # Track activity days
        if timestamp:
            wallets[wallet]["active_days"].add(str(timestamp)[:8])  # crude day cutoff

    # Convert to dataframe
    rows = []
    for wallet, stats in wallets.items():
        repay_ratio = (stats["total_repay"] / stats["total_borrow"]) if stats["total_borrow"] > 0 else 1
        borrow_deposit_ratio = (stats["total_borrow"] / stats["total_deposit"]) if stats["total_deposit"] > 0 else 0

        rows.append({
            "wallet": wallet,
            "total_deposit": stats["total_deposit"],
            "total_borrow": stats["total_borrow"],
            "total_repay": stats["total_repay"],
            "repay_ratio": repay_ratio,
            "borrow_deposit_ratio": borrow_deposit_ratio,
            "liquidation_count": stats["liquidation_count"],
            "active_days": len(stats["active_days"])
        })

    return pd.DataFrame(rows)
