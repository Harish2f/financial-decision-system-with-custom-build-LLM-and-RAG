from ingestion.csv_source import CSVSource
from ingestion.pipeline import IngestionPipeline
from ingestion.repository import FinanceRepository


source = CSVSource("data/contracts.csv")
repo = FinanceRepository()

pipeline = IngestionPipeline(source, repo, "contracts")
pipeline.run()

print("Contracts loaded")