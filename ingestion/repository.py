import pandas as pd
from sqlalchemy import create_engine
from config import get_db_config

class FinanceRepository:
    def __init__(self):
        cfg = get_db_config()

        self.engine = create_engine(
            f"postgresql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['name']}?sslmode={cfg['sslmode']}"
        )

    def write(self, table_name, df, schema="public"):
        df.to_sql(
            table_name,
            self.engine,
            schema=schema,
            if_exists="append",
            index=False,
            method="multi",
        )