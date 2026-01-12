import sys
import pathlib
import sqlalchemy
from sqlalchemy import text

# Ensure repository root is on sys.path so `import config` works
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import config

engine = sqlalchemy.create_engine(
    f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
)

for file in [
    "pipelines/build_customer_features.sql",
    "pipelines/build_baseline.sql"
]:
    print("Running:", file)
    with open(file) as f:
        sql = f.read()
    def _exec_sql_text(conn, sql_text):
        # Split into statements on semicolon and execute non-empty ones.
        statements = [s.strip() for s in sql_text.split(";") if s.strip()]
        for stmt in statements:
            conn.execute(text(stmt))

    with engine.connect() as conn:
        try:
            _exec_sql_text(conn, sql)
            conn.commit()
        except Exception as e:
            print("Error executing SQL:", file, e)
            raise #conn.rollback()

print("Features and labels rebuilt")