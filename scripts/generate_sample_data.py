
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 1000

transactions = pd.DataFrame({
    "transaction_id": range(1, n + 1),
    "customer_id": rng.integers(1, 101, size=n),
    "amount": np.round(
        rng.lognormal(mean=4, sigma=0.7, size=n), 2
    )
})

transactions.to_csv(
    "data/analytics_transactions.csv",
    index=False
)

print(transactions.head())
print(f"Generated {len(transactions)} transactions")

