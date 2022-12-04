#!/usr/bin/env python
import sys
import argparse
from datetime import datetime, timedelta
import time

from database import DB

from lib.i2clcda import lcd_init,lcd_string, lcd_end


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
    lcd_init()

    LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

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
        lcd_string("time: %s"%times[-1].strftime("%H:%M:%S"),LCD_LINE_1)
        lcd_string("CO2: %.1f ppm"%co2[-1],LCD_LINE_2)

        time.sleep(args.interval)


if __name__ == "__main__":
    args = create_parser(sys.argv)
    try:
        main(args)
    finally:
        lcd_end()
