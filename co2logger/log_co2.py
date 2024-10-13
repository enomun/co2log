#!/usr/bin/env python
import sys
import argparse
from datetime import datetime
import time

from sensors import CO2Reader
from database import DB, TextDB

def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--logpath", default="./co2.db")
    parser.add_argument("--out", default="./out.txt")
    parser.add_argument("--interval", type=int, default=10, help="log interval [sec]")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--calibrate", action="store_true")

    args = parser.parse_args(argv[1:])
    return args


def main(args):
    print("start db initialization")
    # dbcls = DB(args.dbpath)
    dbcls = TextDB(args.logpath)
    print("db initialization completed")

    co2sensor = CO2Reader(device="/dev/ttyS0", debug=args.debug)

    print("start reading sensor")
    if args.calibrate:
        co2sensor.calibrate()

    try:
        while True:
            co2 = co2sensor.read()
            if not co2:
                continue
            now = str(datetime.now())
            values = [now, co2]
            dbcls.write(values)
            dbcls.commit()

            try:
                with open(args.out, "w") as f:
                    f.writelines([f"date,co2\n"
                                ,f"{now},{co2}\n"])
            except OSError: 
                print("busy")
                pass
            time.sleep(args.interval)




    finally:
        dbcls.close()

if __name__ == "__main__":
    args = create_parser(sys.argv)
    main(args)