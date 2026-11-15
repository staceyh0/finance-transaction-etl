
import pandas as pd

df = pd.read_csv("data/analytics_transactions.csv")

print("FINANCIAL TRANSACTION SUMMARY")
print("-----------------------------")

print(f"Total Transactions: {len(df)}")
print(f"Unique Customers: {df['customer_id'].nunique()}")
print(f"Total Transaction Value: ${df['amount'].sum():,.2f}")
print(f"Average Transaction: ${df['amount'].mean():,.2f}")
print(f"Median Transaction: ${df['amount'].median():,.2f}")
print(f"Largest Transaction: ${df['amount'].max():,.2f}")
