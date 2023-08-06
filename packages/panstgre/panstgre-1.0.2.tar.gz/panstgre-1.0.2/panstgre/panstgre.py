from psycopg2 import extras,connect
from enum import Enum
import pandas as pd

class DataBase:
    def __init__(self, user:str, host:str, port:str, database:str, password:str, schema:str = 'public'):
        self.user, self.host, self.port, self.database, self.password = user, host, port, database, password
        self.schema = schema
        self.conn = self._connect()

    def __str__(self):
        return f"{self.user}.{self.schema}"

    def _connect(self):
        return connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)

    def tables(self) -> list[str]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.schema}'")
        return [x[0] for x in cur.fetchall()]

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

class Table:
    def __init__(self, database:DataBase, table:str):
        self.database = database
        self.name = table
        self.cur = self.database.conn.cursor()

    def __str__(self):
        return f"{str(self.database)}.{self.name}"
    
    def columns(self) -> dict[str,str]:
        self.cur.execute(f"SELECT column_name,data_type FROM information_schema.columns WHERE table_schema='{self.database.schema}' AND TABLE_NAME='{self.name}'")
        return {k:v for k,v in self.cur.fetchall()}
    
    def keys(self) -> list[str]:
        self.cur.execute(f"SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum=ANY(i.indkey) WHERE i.indrelid='{self.name}'::regclass AND i.indisprimary")
        return [x[0] for x in self.cur.fetchall()]
    
class _pstypes(Enum):
    character = "str"
    integer = "int32"
    date = "datetime64[ns]"
    numberic = "int64"
    boolean = "bool"

class Panstgre:
    def __init__(self, table:Table):
        self.database = table.database
        self.table = table
        self.columns = table.columns()
        self.keys = table.keys()
        self.cur = self.table.cur

    def begin(self):
        self.cur.execute("begin")

    def commit(self):
        self.cur.execute("commit")

    def rollback(self):
        self.cur.execute("rollback")

    def close(self):
        self.cur.close()

    def count(self) -> int:
        self.cur.execute(f"SELECT COUNT(*) FROM {self.table}")
        return int(self.cur.fetchall()[0][0])
    
    def delete(self, condition:str=""):
        sqltext = f"DELETE FROM {self.table.name} WHERE {condition}" if condition else f"DELETE FROM {self.table.name}"
        self.cur.execute(sqltext)
        self.commit()

    def pdread(self, cols:list[str]=[], condition:str="", offset:int=0, limit:int=0) -> pd.DataFrame:
        columns = cols if cols else list(self.columns.keys())
        lmt = "" if limit==0 else f"OFFSET {offset} LIMIT {limit}"
        condition = f"WHERE {condition}" if condition else ""
        sqltext = f"SELECT {','.join(columns)} FROM {self.table.name} {condition} ORDER BY {','.join(self.keys)} {lmt}"
        self.cur.execute(sqltext)
        return Panstgre.adjtypes(pd.DataFrame(data=self.cur.fetchall(), columns=columns, dtype=str), self.columns)

    def upset(self, df:pd.DataFrame, upcols:list[str]=[]):
        columns = list(self.columns.keys())
        upcols = upcols if upcols else columns.copy()
        for col in self.keys : upcols.remove(col)
        sql_text = f"INSERT INTO {self.table.name} ({','.join(self.columns)}) VALUES %s ON CONFLICT ({','.join(self.keys)}) DO UPDATE SET {','.join([f'{x} = EXCLUDED.{x}' for x in upcols])}"        
        df.drop_duplicates(subset=self.keys,inplace=True)
        extras.execute_values(self.cur, sql_text, df[columns].values)
        self.commit()

    @classmethod
    def adjtypes(cls, df:pd.DataFrame, columns:dict[str,str]) -> pd.DataFrame:
        for c_name, c_type in columns.copy().items():
            for db_type, df_type in _pstypes.__members__.items():
                if c_type.startswith(db_type) : columns.update({c_name : df_type.value}) 
        for col in columns.copy().keys():
            if not (col in df.columns) : del columns[col]
        return df.astype(columns)
    
    @classmethod
    def createpts(cls, tables:dict[str,list[str]]) :
        return tuple(list(set([Panstgre(x) for x in [Table(DataBase(k),x) for k, v in tables.items() for x in v]])))
    
    @classmethod
    def csv_2df(cls, path:str, cols:list[str]=None) -> pd.DataFrame:
        return pd.read_csv(filepath_or_buffer=path, sep=",", encoding="utf-8", dtype=str, usecols=cols, keep_default_na=False)