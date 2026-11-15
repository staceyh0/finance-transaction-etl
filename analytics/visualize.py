from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Load synthetic analytics data
df = pd.read_csv("data/analytics_transactions.csv")

output_dir = Path("dashboard")
output_dir.mkdir(exist_ok=True)


# Chart 1: Top 10 Customers
customer_totals = (
    df.groupby("customer_id")["amount"]
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
customer_totals.plot(kind="barh")

plt.title("Top 10 Customers by Transaction Value")
plt.xlabel("Total Transaction Value ($)")
plt.ylabel("Customer ID")
plt.tight_layout()

plt.savefig(output_dir / "top_customers.png", dpi=150)
plt.close()


# Amount Distribution
plt.figure(figsize=(10, 6))

plt.hist(df["amount"], bins=30, edgecolor="black")

plt.title("Distribution of Transaction Amounts")
plt.xlabel("Transaction Amount ($)")
plt.ylabel("Number of Transactions")
plt.tight_layout()

plt.savefig(output_dir / "amount_distribution.png", dpi=150)
plt.close()

# Customer Activity
customer_counts = (
    df.groupby("customer_id")
    .size()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
customer_counts.plot(kind="barh")

plt.title("Top 10 Most Active Customers")
plt.xlabel("Number of Transactions")
plt.ylabel("Customer ID")
plt.tight_layout()

plt.savefig(output_dir / "customer_activity.png", dpi=150)
plt.close()

print("All charts generated successfully!")

