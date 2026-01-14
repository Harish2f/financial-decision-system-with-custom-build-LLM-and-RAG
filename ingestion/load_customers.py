from ingestion.csv_source import CSVSource
from ingestion.pipeline import IngestionPipeline
from ingestion.repository import FinanceRepository

source = CSVSource("data/customers.csv")
repo = FinanceRepository()

pipeline = IngestionPipeline(source, repo, "customers")
pipeline.run()

print("Customers loaded")