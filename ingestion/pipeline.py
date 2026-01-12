class IngestionPipeline:
    def __init__(self, source, repository, table_name):
        self.source = source
        self.repository = repository
        self.table_name = table_name

    def run(self):
        df = self.source.load()
        self.repository.write(self.table_name, df)