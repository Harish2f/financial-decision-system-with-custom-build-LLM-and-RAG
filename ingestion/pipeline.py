class IngestionPipeline:
    def __init__(self, source, repository, table):
        self.source = source
        self.repository = repository
        self.table = table

    def run(self):
        df = self.source.load()
        self.repository.save(self.table, df)