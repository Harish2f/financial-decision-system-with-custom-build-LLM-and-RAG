# Financial Decision System – Production Grade Applied AI

ProductioncGrade Applied AI Platform (AKS + Airflow + CI/CD)

This repository contains a productioncgrade financial risk decision system built using enterprisecstyle Applied AI, governance, and cloud orchestration patterns.

The system is intentionally designed to choose between rule based logic and machine learning based on measurable business impact, not model hype.

It reflects how real financial ML platforms are built, deployed, and governed in production environments.

---

## Business Problem

Finance teams must identify customers who are likely to:
- Pay invoices late
- Accumulate unpaid balances
- Create downstream financial risk

Wrong decisions are expensive:
- **False negatives** → Bad debt, cash-flow risk
- **False positives** → Blocking good customers and losing revenue

Therefore, this system enforces:
- An fully explainable **baseline** as the default.
- ML only when it **clearly improves financial outcomes**

---

## Key Design Principles

- Business first ML (ML must justify itself)
- Explainability before accuracy
- Automated governance
- Reproducibility & auditability
- Cloud native execution

---

## System Architecture

```bash

CSV / SAP-style data
        ↓
Ingestion (Python)
        ↓
Azure PostgreSQL (data plane)
        ↓
SQL Feature Store
        ↓
Baseline Rules + ML Model
        ↓
Decision Evaluation
        ↓
Monitoring & Metrics
        ↓
Airflow (AKS)
        ↓
CI/CD (GitHub Actions)

```
---



## What the System Does

1. Loads customers, contracts, invoices and payments into Azure PostgreSQL
2. Builds customer level finance features and risk labels in SQL 
3. Runs an explainable baseline rule  
4. Trains and evaluates a machine learning model  
5. Approves ML only if it outperforms the baseline  
6. Exposes decisions via the Decision Pipeline
7. Monitors drift and performance  
8. Runs automatically every day  on a schedule via Airflow  on Kubernetes

--- 

## Baseline vs ML Governance

The baseline flags a customer as risky if:
- Average delay > 15 days  
- OR unpaid balance > 10,000 €

The ML model is only allowed into production if it:
- Catches more risky customers
- Without introducing unacceptable false positives

TThe business decision and approval rationale are documented in:

[Decision Log](docs/decision_log.md)

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

## Cloud Native Deployment

Infrastructure
- AKS (Azure Kubernetes Service) – execution layer
- Azure PostgreSQL Flexible Server – data plane
- Azure Container Registry (ACR) – image storage
- Apache Airflow (Helm) – orchestration

CI/CD
- GitHub Actions
- Multi-architecture Docker builds (linux/amd64)
- Automatic:
	•	Image build & push
	•	Kubernetes secret management
	•	Deployment rollout

---


## Orchestration

This system uses Apache Airflow 3 deployed on Azure Kubernetes Service (AKS) with the KubernetesExecutor.

Key points:
- Airflow deployed via Helm chart (apache airflow/airflow 1.18.0)
- Git synced DAGs - no need to rebuild images for DAG changes
- DAGs live in GitHub and are delivered via git-sync
- Scheduler, triggerer, statsd, and dag processor run continuously
- Task pods are ephemeral and only launched when DAGs run

```bash
generate_data
→ ingest_customers
→ ingest_contracts
→ ingest_invoices
→ ingest_payments
→ build_features
→ baseline_eval
→ ml_eval
→ run_decisions
→ monitor

Airflow components in the cluster include:

airflow-api-server
airflow-scheduler
airflow-triggerer
airflow-dag-processor
airflow-statsd
airflow-postgresql

```

This supports:
- Daily execution
- Backfills
- Failure recovery
- End-to-end auditability

---

## Production Grade DAG Hardening

hardened for reliability:
- Retries on transient errors
- Execution timeouts to prevent runaway tasks
- Resource requests and limits per task (KubernetesExecutor)
- catchup disabled to avoid unintended backfills
- max_active_runs=1 to ensure controlled execution

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

Requirements
- Python 3.11+
- .venv or virtual environment
- Azure CLI authenticated
- kubectl configured for your AKS cluster

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
- Model training & Evaluation
- Decision pipeline execution

## Compliance & Audit
 
   This project provides:

	- Reproducible datasets
	- Explainable baselines
	- ML approval based on financial impact
	- Automated deployment logs
	- Fully traceable Airflow execution
	- Kubernetes-native secret handling

## Technology Stack
    - Python
    - Azure PostgreSQL (Azure Flexible Server)
    - Pandas
	- SQLAlchemy
	- XGBoost
	- Apache Airflow 3
	- Docker
	- Azure Container Registry
	- Kubernetes (AKS)
	- GitHub Actions (CI/CD)
