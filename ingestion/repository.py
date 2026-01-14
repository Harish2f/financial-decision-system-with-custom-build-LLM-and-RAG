from sqlalchemy import create_engine
from config import DATABASE_URL

class FinanceRepository:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def write(self, table_name, df):
        df.to_sql(table_name, self.engine, if_exists="append", index=False)