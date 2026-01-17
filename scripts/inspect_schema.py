# scripts/inspect_schema.py
import os
from sqlalchemy import create_engine, inspect


def get_engine():
    return create_engine(
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    )


def run():
    engine = get_engine()
    insp = inspect(engine)

    for table in ["customers", "invoices", "payments"]:
        print(f"\nTABLE: {table}")
        for c in insp.get_columns(table):
            print(f"  {c['name']}  {c['type']}")


if __name__ == "__main__":
    run()