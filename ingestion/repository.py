import sqlalchemy
from sqlalchemy import create_engine, text

class FinanceRepository:
    def __init__(self, config):
        self.engine = create_engine(
            f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
        )

    def write(self, table_name, df):
        conn = self.engine.connect()
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)
        conn.close()