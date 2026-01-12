import sqlalchemy
from sqlalchemy import create_engine

class FinanceRepository:
    def __init__(self, config):
        self.engine = create_engine(
            f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
        )

    def write(self, table_name, df):
        df.to_sql(table_name, self.engine, if_exists="append", index=False)