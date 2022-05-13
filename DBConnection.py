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

    def read_reviews_to_df(self, lang):
        sql_query = f'SELECT r.title, r.review, r.advantage, r.disadvantage, r.score, r.sentiment, r.review_date ' \
                    'FROM hr_brand.reviews  r ' \
                    f'WHERE r.review is not NULL AND r.lang = \'{lang}\' ' \
                    'ORDER BY r.review_date DESC'
        df = pd.read_sql(sql_query, self.conn)
        return df

    def update_sentiment(self, df):
        # quickly stream records into the temp table
        cursor = self.conn.cursor()
        cursor.fast_executemany = True
        statement = "CREATE TABLE [#update_sentiment] (id INT PRIMARY KEY, sentiment VARCHAR(10))"
        cursor.execute(statement)
        subset = df[['id', 'sentiment']]
        # form SQL insert statement
        columns = ", ".join(subset.columns)
        values = '(' + ', '.join(['?'] * len(subset.columns)) + ')'
        # insert
        statement = "INSERT INTO [#update_sentiment] (" + columns + ") VALUES " + values
        insert = [tuple(x) for x in subset.values]
        cursor.executemany(statement, insert)
        statement = '''
        UPDATE
             hr_brand.reviews
        SET
             sentiment = u.sentiment
        FROM
             hr_brand.reviews AS t
        INNER JOIN 
             [#update_sentiment] AS u 
        ON
             u.id=t.id and t.sentiment is NULL;
        '''
        cursor.execute(statement)
        self.conn.commit()
        cursor.execute("DROP TABLE [#update_sentiment]")
        cursor.close()

if __name__ == '__main__':
    SERVER = 'localhost, 1433'
    DATABASE = 'epam_reviews'
    pd.set_option('display.max_columns', None)
    with DBConnection(SERVER, DATABASE, DB_USERNAME, DB_PASSWORD) as db:
        sql_query = 'SELECT id, \'POSITIVE\' as sentiment FROM hr_brand.reviews'
        df = db.read_sql_to_df(sql_query)
        db.update_sentiment(df)