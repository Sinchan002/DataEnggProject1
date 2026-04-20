# # data/sample/generate_sample_data.py
# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# import random

# random.seed(42)
# np.random.seed(42)

# # --- Brokers ---
# brokers = pd.DataFrame({
#     "broker_id":       [f"B{str(i).zfill(3)}" for i in range(1, 11)],
#     "name":            ["Alice Sharma", "Bob Chen", "Carlos Ruiz", "Diana Patel",
#                         "Ethan Müller", "Fatima Al-Sayed", "George Kim",
#                         "Hannah Osei", "Ivan Novak", "Julia Tanaka"],
#     "region":          ["North", "West", "South", "East", "North", "West",
#                         "South", "East", "North", "West"],
#     "commission_rate": [0.015, 0.020, 0.018, 0.022, 0.017,
#                         0.019, 0.021, 0.016, 0.023, 0.020],
# })

# # --- Clients ---
# clients = pd.DataFrame({
#     "client_id":   [f"C{str(i).zfill(4)}" for i in range(1, 51)],
#     "client_name": [f"Client_{i}" for i in range(1, 51)],
#     "segment":     np.random.choice(["Retail", "Institutional", "HNI"], 50),
# })

# # --- Transactions (90 days) ---
# start_date = datetime(2024, 1, 1)
# n = 2000

# transactions = pd.DataFrame({
#     "trade_id":          [f"T{str(i).zfill(6)}" for i in range(1, n + 1)],
#     "broker_id":         np.random.choice(brokers["broker_id"], n),
#     "client_id":         np.random.choice(clients["client_id"], n),
#     "transaction_amount": np.round(np.random.lognormal(mean=10, sigma=1.5, size=n), 2),
#     "product_type":      np.random.choice(["Equity", "Forex", "Commodity", "Bond"], n),
#     "date":              [start_date + timedelta(days=random.randint(0, 89)) for _ in range(n)],
#     "status":            np.random.choice(["completed", "pending", "failed"], n,
#                                           p=[0.92, 0.05, 0.03]),
# })

# brokers.to_csv("data/sample/brokers.csv", index=False)
# clients.to_csv("data/sample/clients.csv", index=False)
# transactions.to_csv("data/sample/transactions.csv", index=False)
# print("Sample data generated.")


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# --- 100 Brokers ---
first_names = [
    "Alice", "Bob", "Carlos", "Diana", "Ethan", "Fatima", "George", "Hannah",
    "Ivan", "Julia", "Kevin", "Laura", "Mohammed", "Nina", "Oscar", "Priya",
    "Quentin", "Rachel", "Samuel", "Tina", "Umar", "Vera", "William", "Xena",
    "Yusuf", "Zara", "Aaron", "Bella", "Cyrus", "Disha", "Elias", "Freya",
    "Gaurav", "Helena", "Ishaan", "Jasmine", "Kiran", "Leila", "Marco", "Nadia",
    "Omar", "Phoebe", "Raj", "Sara", "Tariq", "Uma", "Victor", "Wendy",
    "Xander", "Yara", "Zaid", "Amina", "Bruno", "Camille", "Darius", "Elena",
    "Felix", "Gina", "Hassan", "Iris", "James", "Kavya", "Leon", "Maya",
    "Noah", "Olivia", "Pedro", "Quinn", "Riya", "Stefan", "Tanvi", "Ulrich",
    "Valeria", "Wesley", "Xiulan", "Yasmin", "Zubair", "Aditi", "Benjamin",
    "Clara", "Deepak", "Eva", "Faisal", "Gloria", "Hugo", "Ingrid", "Jin",
    "Krisha", "Luca", "Mira", "Nikhil", "Ola", "Pia", "Rohan", "Simone",
    "Tariq", "Ursula", "Vikram", "Wanda"
]

last_names = [
    "Sharma", "Chen", "Ruiz", "Patel", "Müller", "Al-Sayed", "Kim", "Osei",
    "Novak", "Tanaka", "Singh", "Fischer", "Hassan", "Petrov", "Fernandez",
    "Nair", "Dubois", "Okonkwo", "Weber", "Yamamoto", "Khan", "Ivanova",
    "Brown", "Cruz", "Lindqvist", "Reyes", "Torres", "Nakamura", "Becker",
    "Mehta", "Andersen", "Sato", "Nguyen", "Martins", "Ahmed", "Popescu",
    "Vargas", "Johansson", "Gupta", "Rashid", "Mensah", "Eriksson", "Chow",
    "Souza", "Afolabi", "Kowalski", "Demir", "Olsen", "Bakr", "Jain",
    "Moreau", "Chandra", "Owusu", "Haddad", "Bergman", "Ito", "Santos",
    "Levi", "Ramos", "Bhatt", "Strömberg", "Endo", "Diallo", "Cardoso",
    "Molina", "Haugen", "Iyer", "Park", "Ferreira", "Gomes", "Svensson",
    "Suresh", "Barakat", "Nkosi", "Larsson", "Hu", "Ali", "Siddiqui",
    "Rao", "Fonseca", "Schneider", "Kapoor", "Ibáñez", "Yamada", "Musa",
    "Lindberg", "Zhang", "Araújo", "Holm", "Datta", "Yilmaz", "Kwame",
    "Magnusson", "Takahashi", "Sinha", "Lopes", "Petersen", "Asante",
    "Holmberg", "Aziz", "Mäkinen", "Bose"
]

regions = ["North", "South", "East", "West", "Central"]

n_brokers = 100

brokers = pd.DataFrame({
    "broker_id":       [f"B{str(i).zfill(3)}" for i in range(1, n_brokers + 1)],
    "name":            [f"{first_names[i % len(first_names)]} {last_names[i % len(last_names)]}" for i in range(n_brokers)],
    "region":          np.random.choice(regions, n_brokers),
    "commission_rate": np.round(np.random.uniform(0.010, 0.030, n_brokers), 4),
})

# --- 200 Clients ---
segments = ["Retail", "Institutional", "HNI"]
clients = pd.DataFrame({
    "client_id":   [f"C{str(i).zfill(4)}" for i in range(1, 201)],
    "client_name": [f"Client_{i}" for i in range(1, 201)],
    "segment":     np.random.choice(segments, 200),
})

# --- Transactions (90 days, 10,000 records) ---
start_date = datetime(2024, 1, 1)
n = 10000

transactions = pd.DataFrame({
    "trade_id":           [f"T{str(i).zfill(6)}" for i in range(1, n + 1)],
    "broker_id":          np.random.choice(brokers["broker_id"], n),
    "client_id":          np.random.choice(clients["client_id"], n),
    "transaction_amount": np.round(np.random.lognormal(mean=10, sigma=1.5, size=n), 2),
    "product_type":       np.random.choice(["Equity", "Forex", "Commodity", "Bond"], n),
    "date":               [start_date + timedelta(days=random.randint(0, 89)) for _ in range(n)],
    "status":             np.random.choice(
                              ["completed", "pending", "failed"], n,
                              p=[0.92, 0.05, 0.03]
                          ),
})

import os
os.makedirs("data/sample", exist_ok=True)
brokers.to_csv("data/sample/brokers.csv", index=False)
clients.to_csv("data/sample/clients.csv", index=False)
transactions.to_csv("data/sample/transactions.csv", index=False)

print(f"Brokers   : {len(brokers)} rows  → data/sample/brokers.csv")
print(f"Clients   : {len(clients)} rows  → data/sample/clients.csv")
print(f"Transactions: {len(transactions)} rows → data/sample/transactions.csv")
print("\n--- Broker sample (first 5) ---")
print(brokers.head().to_string(index=False))
print("\n--- Transaction sample (first 5) ---")
print(transactions.head().to_string(index=False))
print("\n--- Region distribution ---")
print(brokers["region"].value_counts().to_string())