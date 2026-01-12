from ingestion.csv_source import CSVSource
from ingestion.pipeline import IngestionPipeline
from ingestion.repository import FinanceRepository
import config

source = CSVSource("data/customers.csv")
repo = FinanceRepository(config)

pipeline = IngestionPipeline(source, repo, "customers")
pipeline.run()

print("Customers loaded")