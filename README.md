# Financial Decision System – Production-Grade Applied AI

This repository contains a fully production-grade AI system for detecting financial risk from customer payment behavior.  
It is designed using Enterprise style applied AI, governance, and orchestration standards.

The system decides whether to use **business rules or machine learning** based on measurable business impact, not hype.

It implements the full lifecycle:

Data generation → Ingestion → Feature engineering → Model training → Decision inference → Orchestration (Airflow) → Cloud database (Azure PostgreSQL)

The system is designed to resemble how modern financial ML platforms are built in real enterprises.

---

## Business Problem

Finance teams must identify customers who are likely to:
- Pay invoices late
- Accumulate unpaid balances
- Create financial risk

Wrong decisions are expensive:
- **False negatives** → Bad debt
- **False positives** → Blocking good customers and losing revenue

Therefore, this system enforces:
- An fully explainable **baseline**
- ML only when it **clearly improves financial outcomes**

---

## System Architecture

```bash

CSV / SAP-style data
↓
Ingestion (Python)
↓
Azure PostgreSQL (Operational Data Store)
↓
Feature Store (SQL)
↓
Baseline Rules + ML
↓
Decision Engine
↓
Monitoring & Metrics
↓
Airflow (Daily Execution)
```
---

## What the System Does

1. Loads customers, contracts, invoices and payments into Azure PostgreSQL
2. Builds customer-level finance features and risk labels in SQL 
3. Runs an explainable baseline rule  
4. Trains and evaluates a machine-learning model  
5. Approves ML only if it beats the baseline  
6. Exposes decisions via the Decision Pipeline
7. Monitors drift and performance  
8. Runs automatically every day  on a schedule via Airflow  

---

## Baseline vs ML Governance

The baseline flags a customer as risky if:
- Average delay > 15 days  
- OR unpaid balance > 10,000 €

The ML model is only allowed into production if it:
- Catches more risky customers
- Without introducing unacceptable false positives

The business decision is documented in:

docs/decision_log.md

---

## Feature Store

All risk features and labels are computed inside PostgreSQL using SQL:
- Late invoices
- Average days late
- Total billed
- Total paid
- Outstanding balance
- Risk label

This guarantees:
- No training / serving skew
- Full auditability
- Regulatory traceability


---

## Orchestration

The full production pipeline runs in Airflow:

```bash
generate_data
→ ingest_customers
→ ingest_contracts
→ ingest_invoices
→ ingest_payments
→ build_features
→ train_model
→ run_decisions

```

This supports:
- Daily execution
- Backfills
- Failure recovery
- Auditability

---

## Monitoring

The system tracks:
- Feature distributions
- Risk rate
- Model performance (TP, FP, FN, accuracy)

This prevents:
- Silent model degradation
- Data drift
- Finance and Regulatory risk

---

## How to Run Locally

Example workflow:

```bash
python -m ingestion.generate_data
python pipelines/run_sql.py
python decision/run_baseline.py
python decision/run_ml.py

airflow api-server
airflow scheduler
```

## CI

GitHub Actions validates:
- Data generation
- SQL feature engineering
- Model training
- Decision pipeline

## Compliance & Audit
 
   This project provides:

	- Reproducible datasets
	- Explainable baselines
	- ML approval based on financial impact
	- Drift monitoring
	- Fully traceable Airflow execution

## Technology Stack
    - Python
    - PostgreSQL (Azure)
    - Pandas
	- SQLAlchemy
	- XGBoost
	- Apache Airflow 3
	- Git
    - Azure ML
