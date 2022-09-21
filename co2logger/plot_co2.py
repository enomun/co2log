#!/usr/bin/env python
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime, timedelta

from database import DB
from lib import plot


def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", default="/db/co2.db")
    parser.add_argument("--outpath", default="./debug/co2concentrations.png")
    parser.add_argument("--interval", type=int, default=0)
    args = parser.parse_args(argv[1:])

    return args


def read_data(dbpath, sql='select * from co2'):
    db = DB(dbpath)
    df = db.read_sql_in_df(sql)
    db.close()

    times = [datetime.strptime(date.strip().split(".")[0], "%Y-%m-%d %H:%M:%S") for date in df["date"]]
    co2 = df["co2"].values

    return times, co2


def main(args):
    while True:
        # set sql conditions
        now = datetime.now()
        cnd = (now - timedelta(days=100)).date()
        sql = f"select * from co2 where date > '{cnd}'"

        # read data
        times, co2 = read_data(args.dbpath, sql)

        # create figures
        plot.create_figure(times, co2, args.outpath)
        p = Path(args.outpath)
        outpath2 = p.parent / (p.stem + "2" + p.suffix)
        plot.create_figure(times, co2, outpath2, enlarged="True")

        print("figure updated: %s" % now)

        if args.interval <= 0:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    args = create_parser(sys.argv)
    main(args)