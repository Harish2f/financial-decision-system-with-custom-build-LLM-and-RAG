import os
from sqlalchemy import create_engine

def get_engine():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "finance_ai")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    sslmode = os.getenv("DB_SSLMODE", "prefer")

    url = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{host}:{port}/{name}?sslmode={sslmode}"
    )

    return create_engine(url)