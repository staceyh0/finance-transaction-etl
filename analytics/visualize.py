from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from app.ingestion import read_transactions
from app.cleaning import clean_transactions

# Configuration
DATA_PATH = Path("data/analytics_transactions_dirty.csv")
OUTPUT_DIR = Path("dashboard")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.figsize": (10, 6),
    "font.size": 11,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Load and validate transactions
transactions = read_transactions(DATA_PATH)
result = clean_transactions(transactions)

summary = result["summary"]

valid_transactions = result["valid_transactions"]
rejected_transactions = result["rejected_transactions"]

print("Dataset:", DATA_PATH)
print("Total transactions:", summary["total_rows"])
print("Valid transactions:", len(valid_transactions))
print("Rejected transactions:", len(rejected_transactions))
print("Rejection summary:", summary)

# Prepare cleaned analytics data
df = pd.DataFrame(
    valid_transactions,
    columns=["transaction_id", "customer_id", "amount"]
)

df["amount"] = pd.to_numeric(df["amount"], errors="raise")

# Helper function
def save_chart(filename):
    """Save the current Matplotlib figure."""
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=200, bbox_inches="tight")
    plt.close()


# Chart 1: Top 10 customers by transaction value
customer_totals = (
    df.groupby("customer_id")["amount"]
    .sum()
    .nlargest(10)
    .sort_values()
)

if not customer_totals.empty:
    ax = customer_totals.plot(
        kind="barh",
        color="#2563EB"
    )

    ax.set_title("Top 10 Customers by Transaction Value", pad=16)
    ax.set_xlabel("Total Transaction Value ($)")
    ax.set_ylabel("Customer ID")
    ax.bar_label(ax.containers[0], fmt="$%.0f", padding=4)
    ax.grid(axis="x", alpha=0.2)
    ax.set_axisbelow(True)

    save_chart("top_customers.png")
else:
    print("Skipping Chart 1: No valid customer transactions.")


# Chart 2: Transaction amount distribution
if not df.empty:
    fig, ax = plt.subplots()

    ax.hist(
        df["amount"].dropna(),
        bins=30,
        color="#0D9488",
        edgecolor="white"
    )

    ax.set_title("Distribution of Transaction Amounts", pad=16)
    ax.set_xlabel("Transaction Amount ($)")
    ax.set_ylabel("Number of Transactions")
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    save_chart("amount_distribution.png")
else:
    print("Skipping Chart 2: No valid transactions.")


# Chart 3: Top 10 most active customers
customer_counts = (
    df.groupby("customer_id")
    .size()
    .nlargest(10)
    .sort_values()
)

if not customer_counts.empty:
    ax = customer_counts.plot(
        kind="barh",
        color="#7C3AED"
    )

    ax.set_title("Top 10 Most Active Customers", pad=16)
    ax.set_xlabel("Number of Transactions")
    ax.set_ylabel("Customer ID")
    ax.bar_label(ax.containers[0], padding=4)
    ax.grid(axis="x", alpha=0.2)
    ax.set_axisbelow(True)

    save_chart("customer_activity.png")
else:
    print("Skipping Chart 3: No valid customer transactions.")


# Chart 4: Transaction rejections by reason
reasons = [
    "Missing customer ID",
    "Missing transaction ID",
    "Invalid amount",
    "Duplicate transaction"
]

counts = [
    summary["missing_customer_id"],
    summary["missing_transaction_id"],
    summary["invalid_amount"],
    summary["duplicate_transactions"]
]

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.barh(reasons, counts, color="#D97706")
ax.bar_label(bars, padding=4)

ax.set_title("Transaction Rejections by Reason", pad=16)
ax.set_xlabel("Number of Transactions")
ax.invert_yaxis()
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

save_chart("rejection_reasons.png")


# Chart 5: Transaction Validation Overview

total = summary["total_rows"]
valid = summary["valid_rows"]
rejected = len(rejected_transactions)

if total > 0:
    acceptance_rate = valid / total * 100
    rejection_rate = rejected / total * 100

    fig, ax = plt.subplots(figsize=(10, 3.5))

    # Draw a thin horizontal stacked bar
    ax.barh(
        0,
        valid,
        color="#16A34A",
        height=0.25,
        label="Accepted"
    )

    ax.barh(
        0,
        rejected,
        left=valid,
        color="#DC2626",
        height=0.25,
        label="Rejected"
    )

    # Label accepted percentage
    ax.text(
        valid / 2,
        0,
        f"{acceptance_rate:.1f}% Accepted",
        ha="center",
        va="center",
        color="white",
        fontsize=12,
        fontweight="bold"
    )

    # Keep the bar thin by controlling the y-axis
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])

    ax.set_xlim(0, total)
    ax.set_xlabel("Number of Transactions")

    ax.set_title(
        "Transaction Validation Overview",
        fontsize=16,
        fontweight="bold",
        pad=45
    )

    # Summary above the bar
    ax.text(
        0.5,
        1.12,
        f"{total:,} Processed  |  "
        f"{valid:,} Accepted  |  "
        f"{rejected:,} Rejected ({rejection_rate:.1f}%)",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        color="gray"
    )

    # Legend below the chart
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=2,
        frameon=False
    )

    ax.spines[["top", "right", "left"]].set_visible(False)

    fig.subplots_adjust(
        top=0.68,
        bottom=0.32,
        left=0.08,
        right=0.95
    )

    fig.savefig(
        OUTPUT_DIR / "validation_results.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

else:
    print("Skipping Chart 5: No transactions to analyze.")


print("All charts generated successfully!")
