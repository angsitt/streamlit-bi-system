import pyodbc
import pandas as pd
from credentials import DB_USERNAME, DB_PASSWORD

class DBConnection:

    def __init__(self, server, database, username, password):
        self.conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};' \
                           'SERVER='+server+';' \
                           'DATABASE='+database+';' \
                           'UID='+username+';' \
                           'PWD='+ password
        self.conn = pyodbc.connect(self.conn_string)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def exec_select(self, sql_query):
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def exec_command(self, sql_query):
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        self.conn.commit()
        cursor.close()

    def read_sql_to_df(self, sql_query):
        df = pd.read_sql(sql_query, self.conn)
        return df

if __name__ == '__main__':
    SERVER = 'localhost, 1433'
    DATABASE = 'epam_reviews'
    pd.set_option('display.max_columns', None)
    with DBConnection(SERVER, DATABASE, DB_USERNAME, DB_PASSWORD) as db:
        sql_query = 'SELECT * FROM hr_brand.company_reviews'
        df = db.read_sql_to_df(sql_query)
        print(df.head())