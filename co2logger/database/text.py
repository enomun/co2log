from pathlib import Path
import pandas as pd

class TextDB:
    def __init__(self, fp ,header=["date","co2"]):
        self.fp = fp
        self.header = header


        if not Path(self.fp).exists():
            with open(self.fp, "w") as f:
                f.write(",".join(self.header) + "\n")

    def write(self, values):
        try:
            with open(self.fp, "a") as f:
                f.write(",".join([str(v) for v in values])+"\n")
        except OSError: 
                print("busy")

    def commit(self):
        pass
        
    def close(self):
        pass
    
    def read_sql_in_df(self, sql):
        df = pd.read_csv(self.fp)
        return df
        