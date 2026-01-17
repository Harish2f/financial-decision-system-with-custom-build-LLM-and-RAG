from sqlalchemy import create_engine, inspect
import os

engine = create_engine(
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
    f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
)

inspector = inspect(engine)
columns = inspector.get_columns("customer_finance_features")

for c in columns:
    print(c["name"])