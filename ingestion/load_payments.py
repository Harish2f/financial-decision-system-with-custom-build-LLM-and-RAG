from ingestion.csv_source import CSVSource
from ingestion.pipeline import IngestionPipeline
from ingestion.repository import FinanceRepository
import config

source = CSVSource("data/payments.csv")
repo = FinanceRepository(config)

pipeline = IngestionPipeline(source, repo, "payments")
pipeline.run()

print("Payments loaded")