from db import get_engine

class FinanceRepository:
    def __init__(self):
        self.engine = get_engine()

    def write(self, table_name, df):
        df.to_sql(table_name, self.engine, if_exists="append", index=False)