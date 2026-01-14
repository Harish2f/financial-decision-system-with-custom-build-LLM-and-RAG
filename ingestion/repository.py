import os
from sqlalchemy import create_engine

class FinanceRepository:
    def __init__(self):
        self.engine = self._create_engine()

    def _create_engine(self):
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT", "5432")
        db = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        sslmode = os.getenv("DB_SSLMODE", "require")

        if not all([host, db, user, password]):
            raise RuntimeError("Database environment variables are not set")

        url = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
            f"?sslmode={sslmode}"
        )

        return create_engine(url, pool_pre_ping=True)

    def write(self, table_name, df):
        df.to_sql(table_name, self.engine, if_exists="append", index=False)