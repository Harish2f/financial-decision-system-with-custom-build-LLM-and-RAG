import pandas as pd

class CSVSource:
    def __init__(self, path):
        self.path = path

    def read(self):
        # Read the CSV into a DataFrame
        df = pd.read_csv(self.path)
        return df

    def load(self):
        return pd.read_csv(self.path)