#!/usr/bin/env python
import sys
import argparse
import datetime
import time

from database import DB
from sensor import CO2Reader

def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", default="./co2.db")
    parser.add_argument("--interval", type=int,default=10)
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args(argv[1:])
    return args


def main(args):
    dbcls = DB(args.dbpath)
    co2sensor = CO2Reader(device="/dev/ttyS0",debug=args.debug)

    while True:
        co2 = co2sensor.read()
        if not co2:
            continue
        now = str(datetime.datetime.now())
        values = (now, co2)
        print(values)    
        dbcls.write(values)
        dbcls.commit()
        time.sleep(args.interval)

if __name__ == "__main__":
    args = create_parser(sys.argv)
    main(args)