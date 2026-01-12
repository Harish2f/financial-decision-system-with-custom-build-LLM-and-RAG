import pandas as pd
from .data_source import DataSource

class CSVSource(DataSource):
    def __init__(self, path):
        self.path = path

    def load(self):
        return pd.read_csv(self.path)