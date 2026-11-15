import pandas as pd

df = pd.read_csv("data/analytics_transactions.csv")

# Use nullable integers for IDs
df["transaction_id"] = df["transaction_id"].astype("Int64")
df["customer_id"] = df["customer_id"].astype("Int64")

# Introduce validation failures
df.loc[0:9, "customer_id"] = pd.NA
df.loc[10:19, "amount"] = -100
df.loc[20:24, "transaction_id"] = pd.NA

# Introduce duplicate transaction IDs
df.loc[25:29, "transaction_id"] = df.loc[30, "transaction_id"]

df.to_csv("data/analytics_transactions_dirty.csv", index=False)

print("Dirty dataset generated!")