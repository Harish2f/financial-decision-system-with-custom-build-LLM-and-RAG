import sqlalchemy
from sqlalchemy import text
import config

engine = sqlalchemy.create_engine(
    f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
)

with open("pipelines/build_customer_features.sql") as f:
    sql = f.read()

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()

print("Customer feature table rebuilt")