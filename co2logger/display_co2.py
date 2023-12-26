#!/usr/bin/env python
import sys
import argparse
from datetime import datetime, timedelta
import time

from database import DB
from lib.lcd import LCD


def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", default="./co2.db")
    parser.add_argument("--interval", type=int, default=10, help="log interval [sec]")

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
    gpio_display=None
    gpio_display=17

    print("init lcd")
    lcd = LCD(gpio_id=gpio_display)

    print("main")
    try:
        while True:
            # set sql conditions
            now = datetime.now()
            cnd = (now - timedelta(minutes=5)).date()
            sql = f"select * from co2 where date > '{cnd}'"

            # read data
            times, co2 = read_data(args.dbpath, sql)

            if args.interval <= 0:
                break

            # Display
            lcd.show("time: %s"%times[-1].strftime("%H:%M:%S"),row=0)
            lcd.show("CO2: %.1f ppm"%co2[-1],row=1)
            time.sleep(args.interval)
    finally:
        lcd.clear()


if __name__ == "__main__":
    args = create_parser(sys.argv)
    main(args)
