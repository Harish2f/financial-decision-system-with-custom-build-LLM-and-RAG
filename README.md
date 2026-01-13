# Financial Decision System – Production-Grade Applied AI

This repository contains a fully production-grade AI system for detecting financial risk from customer payment behavior.  
It is designed using Enterprise style applied AI, governance, and orchestration standards.

The system decides whether to use **business rules or machine learning** based on measurable business impact, not hype.

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
- An explainable **baseline**
- ML only when it **clearly improves financial outcomes**

---

## System Architecture

```bash

CSV / SAP-style data
↓
Ingestion (Python)
↓
PostgreSQL
↓
Feature Store (SQL)
↓
Baseline + ML
↓
Decision Engine
↓
Monitoring
↓
Airflow (Daily Execution)
```
---

## What the System Does

1. Loads customers, contracts, invoices and payments  
2. Builds financial features and risk labels in SQL  
3. Runs an explainable baseline rule  
4. Trains and evaluates a machine-learning model  
5. Approves ML only if it beats the baseline  
6. Monitors drift and performance  
7. Runs automatically every day via Airflow  

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

## Orchestration

The full production pipeline runs in Airflow:

ingest_data → build_features → baseline_eval + ml_eval → monitor

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
- Silent model failure
- Data drift
- Regulatory risk

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

## Compliance & Audit
 
   This project provides:

	- Reproducible datasets
	- Explainable baselines
	- ML approval based on financial impact
	- Drift monitoring
	- Fully traceable Airflow execution

## Technology Stack
    - Python
    - PostgreSQL
    - Pandas
	- SQLAlchemy
	- XGBoost
	- Apache Airflow
	- Git
    - Azure ML
