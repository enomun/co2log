from datetime import datetime
import sqlite3
import time
import sys
import argparse

from matplotlib import pyplot as plt
import pandas as pd

def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", default="./co2.db")
    parser.add_argument("--outpath", default="co2concentrations.png")
    parser.add_argument("--interval", type=int,default=60)
    parser.add_argument("--t", action="store_true")

    args = parser.parse_args(argv[1:])
    return args

def read_df_from_db(dbpath):
    con = sqlite3.connect(dbpath)
    cur = con.cursor()

    sql = 'select * from co2'
    df = pd.read_sql_query(sql, con)
    con.close()
    return df

def update_figure(dbpath, outpath):
    df = read_df_from_db(dbpath)
    times = [datetime.strptime(date.strip(), "%Y-%m-%d %H:%M:%S.%f") for date in df["date"]]
    
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(times,df["co2"])
    plt.xticks(rotation=50)

    #ax.text(times[0],800,"Last updated:\n %s"%now)
    fig.suptitle("Last updated:\n %s"%now)
    fig.tight_layout()
    fig.savefig(outpath)

def main(args):
    while True:
        now = str(datetime.now())
        update_figure(args.dbpath, args.outpath)
        print("figure updated: %s"%now)
        time.sleep(args.interval)

if __name__ == "__main__":
    args = create_parser(sys.argv)
    print(args)
    main(args)