from ingestion.csv_source import CSVSource
from ingestion.pipeline import IngestionPipeline
from ingestion.repository import FinanceRepository
import config

source = CSVSource("data/invoices.csv")
repo = FinanceRepository(config)

pipeline = IngestionPipeline(source, repo, "invoices")
pipeline.run()

print("Invoices loaded")