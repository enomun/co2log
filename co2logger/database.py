import time
import sqlite3
import pathlib

class DB:
    def __init__(self, dbpath):
        self.con = sqlite3.connect(dbpath)
        self.cur = self.con.cursor()
    
        if not pathlib.Path(dbpath).exists():
            self.cur.execute('''CREATE TABLE co2
                   (date text, co2 real)''')
            self.con.commit()
        self.lastdump =  time.time()

    def write(self, values):
        self.cur.execute("INSERT INTO co2 VALUES %s"%str(values))

    def commit(self):
        self.con.commit()

    def write_interval(self, values, dump_interval):
        self.write(values)    
        if time.time()- self.lastdump >=dump_interval:
            self.con.commit()
            lastdump = time.time()

    def read_sql(self,sql):
        self.cur.execute(sql)            
    
    def close(self):
        self.con.close()
