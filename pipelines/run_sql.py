import sys
import pathlib
import sqlalchemy
from sqlalchemy import text

# Ensure repository root is on sys.path so `import config` works
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import config

engine = sqlalchemy.create_engine(
    f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    f"?sslmode={config.DB_SSLMODE}"
)

def run_sql_file(path):
    print("Running:", path)
    with open(path) as f:
        sql = f.read()

    statements = [s.strip() for s in sql.split(";") if s.strip()]

    with engine.begin() as conn:   # guaranteed transaction
        for stmt in statements:
            conn.execute(text(stmt))

for file in [
    "pipelines/build_customer_features.sql",
    "pipelines/build_baseline.sql"
]:
    try:
        run_sql_file(file)
    except Exception as e:
        print("Error executing SQL:", file)
        raise

print("Features and labels rebuilt")