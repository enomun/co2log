#!/usr/bin/env python
import sys
import argparse
import time
from datetime import datetime

from matplotlib import pyplot as plt
import pandas as pd

from database import DB

def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", default="./co2.db")
    parser.add_argument("--outpath", default="co2concentrations.png")
    parser.add_argument("--interval", type=int,default=0)
    args = parser.parse_args(argv[1:])
    return args

def create_figure(df, outpath):
    times = [datetime.strptime(date.strip(), "%Y-%m-%d %H:%M:%S.%f") for date in df["date"]]
    threshold = 1000

    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(times,df["co2"])
    ax.set_ylim([300,1200])

    ax.plot([times[0],times[-1]],[threshold,threshold], "k--")
    ax.grid(which="major", axis="y", color = "k", alpha=0.2)
    ax.tick_params(left=True, right =True, labelleft=True, labelright=True)

    plt.xticks(rotation=50)

    #ax.text(times[0],800,"Last updated:\n %s"%now)
    fig.suptitle("Last updated:\n %s"%now)
    fig.tight_layout()
    fig.savefig(outpath)
    fig.clf()
    plt.close(fig)

def main(args):
    while True:
        db = DB(args.dbpath)
        now = str(datetime.now())
        
        sql = 'select * from co2'
        df = pd.read_sql_query(sql, db.con)
        db.close()

        create_figure(df, args.outpath)
        print("figure updated: %s"%now)

        if args.interval <=0:
            break
        time.sleep(args.interval)

if __name__ == "__main__":
    args = create_parser(sys.argv)
    main(args)