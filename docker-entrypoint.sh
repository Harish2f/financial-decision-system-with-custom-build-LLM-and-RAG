#!/bin/bash
set -e

echo "Starting Financial Decision System"

python3 -m ingestion.generate_data
python3 -m ingestion.load_customers
python3 -m ingestion.load_invoices
python -m ingestion.load_payments
python3 -m pipelines.run_sql
python3 -m models.extract_training_data
python3 -m models.train_model
python3 -m decision.run_baseline
python -m decision.run_ml

echo "Pipeline completed successfully"