import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)

# Customers
customers = []
for i in range(500):
    customers.append({
        "customer_id": f"C{i}",
        "country": random.choice(["DE", "FR", "IT", "ES", "US"]),
        "industry": random.choice(["Energy", "Manufacturing", "Retail", "Logistics"]),
        "signup_date": datetime(2019, 1, 1) + timedelta(days=random.randint(0, 1200)),
        "credit_limit": random.randint(20000, 200000)
    })

customers = pd.DataFrame(customers)

# Contracts
contracts = []
for i in range(600):
    cust = customers.sample(1).iloc[0]
    start = cust["signup_date"] + timedelta(days=random.randint(30, 200))
    end = start + timedelta(days=random.randint(180, 900))
    contracts.append({
        "contract_id": f"K{i}",
        "customer_id": cust["customer_id"],
        "start_date": start,
        "end_date": end,
        "monthly_value": random.randint(1000, 20000),
        "sla_days": random.choice([15, 30, 45])
    })

contracts = pd.DataFrame(contracts)

# Invoices
invoices = []
for i in range(5000):
    con = contracts.sample(1).iloc[0]
    issue = con["start_date"] + timedelta(days=random.randint(0, 700))
    due = issue + timedelta(days=int(con["sla_days"]))
    invoices.append({
        "invoice_id": f"I{i}",
        "customer_id": con["customer_id"],
        "contract_id": con["contract_id"],
        "issue_date": issue,
        "due_date": due,
        "amount": random.randint(500, 30000)
    })

invoices = pd.DataFrame(invoices)

# Payments
payments = []
for _, inv in invoices.iterrows():
    if random.random() < 0.85:  # 85% invoices paid
        delay = random.choice([0, 5, 10, 30, 60])
        pay_date = inv["due_date"] + timedelta(days=delay)
        payments.append({
            "payment_id": f"P{inv['invoice_id']}",
            "invoice_id": inv["invoice_id"],
            "payment_date": pay_date,
            "amount_paid": inv["amount"]
        })

payments = pd.DataFrame(payments)

customers.to_csv("data/customers.csv", index=False)
contracts.to_csv("data/contracts.csv", index=False)
invoices.to_csv("data/invoices.csv", index=False)
payments.to_csv("data/payments.csv", index=False)

print("Data generated.")