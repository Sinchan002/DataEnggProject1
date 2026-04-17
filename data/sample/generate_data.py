# data/sample/generate_sample_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# --- Brokers ---
brokers = pd.DataFrame({
    "broker_id":       [f"B{str(i).zfill(3)}" for i in range(1, 11)],
    "name":            ["Alice Sharma", "Bob Chen", "Carlos Ruiz", "Diana Patel",
                        "Ethan Müller", "Fatima Al-Sayed", "George Kim",
                        "Hannah Osei", "Ivan Novak", "Julia Tanaka"],
    "region":          ["North", "West", "South", "East", "North", "West",
                        "South", "East", "North", "West"],
    "commission_rate": [0.015, 0.020, 0.018, 0.022, 0.017,
                        0.019, 0.021, 0.016, 0.023, 0.020],
})

# --- Clients ---
clients = pd.DataFrame({
    "client_id":   [f"C{str(i).zfill(4)}" for i in range(1, 51)],
    "client_name": [f"Client_{i}" for i in range(1, 51)],
    "segment":     np.random.choice(["Retail", "Institutional", "HNI"], 50),
})

# --- Transactions (90 days) ---
start_date = datetime(2024, 1, 1)
n = 2000

transactions = pd.DataFrame({
    "trade_id":          [f"T{str(i).zfill(6)}" for i in range(1, n + 1)],
    "broker_id":         np.random.choice(brokers["broker_id"], n),
    "client_id":         np.random.choice(clients["client_id"], n),
    "transaction_amount": np.round(np.random.lognormal(mean=10, sigma=1.5, size=n), 2),
    "product_type":      np.random.choice(["Equity", "Forex", "Commodity", "Bond"], n),
    "date":              [start_date + timedelta(days=random.randint(0, 89)) for _ in range(n)],
    "status":            np.random.choice(["completed", "pending", "failed"], n,
                                          p=[0.92, 0.05, 0.03]),
})

brokers.to_csv("data/sample/brokers.csv", index=False)
clients.to_csv("data/sample/clients.csv", index=False)
transactions.to_csv("data/sample/transactions.csv", index=False)
print("Sample data generated.")