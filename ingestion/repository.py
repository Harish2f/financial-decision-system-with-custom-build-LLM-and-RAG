import psycopg2

class FinanceRepository:
    def __init__(self, conn_string):
        self.conn_string = conn_string

    def save(self, table, df):
        conn = psycopg2.connect(self.conn_string)
        df.to_sql(table, conn, if_exists="append", index=False)
        conn.close()