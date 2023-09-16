import pandas as pd
from sqlalchemy import create_engine, inspect
import urllib.parse
import pyodbc

class PostgresqlConnector:
    def __init__(self,hostname,port,username,password,database):
        self.type = 'postgresql'
        self.username = username
        self.password = urllib.parse.quote_plus(password)
        self.hostname = hostname
        self.port = port
        self.database = database
        self.conn_string = f'postgresql+psycopg2://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database}'
        self.engine = create_engine(self.conn_string)
    def get_results(self,sql):
        result = pd.read_sql(sql,con=self.engine)
        return result
    def list_tables(self):
        inspector = inspect(self.engine)
        out_tab = []
        schemas = inspector.get_schema_names()
        for schema in schemas:
            for table_name in inspector.get_table_names(schema=schema):
                out_tab.append(schema+'.'+table_name)
        return out_tab
    def __del__(self):
        self.engine.dispose()

class MSAccessConnector:
    def __init__(self,db_path):
        self.type = 'access'
        self.db_path = db_path
        self.conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' \
                                f'DBQ={self.db_path};'
        self.conn = pyodbc.connect(self.conn_string)
    def get_results(self,sql):
        result = pd.read_sql(sql,con=self.conn)
        return result
    def list_tables(self):
        return [table.table_name for table in self.conn.cursor().tables(tableType='TABLE')]
    def __del__(self):
        self.conn.close()