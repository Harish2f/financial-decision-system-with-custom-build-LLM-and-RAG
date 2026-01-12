from ingestion.csv_source import CSVSource
from ingestion.pipeline import IngestionPipeline
from ingestion.repository import FinanceRepository
import config

source = CSVSource("data/contracts.csv")
repo = FinanceRepository(config)

pipeline = IngestionPipeline(source, repo, "contracts")
pipeline.run()

print("Contracts loaded")