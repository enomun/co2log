#!/usr/bin/env python
import sys
import argparse
from datetime import datetime
import time

# from database import DB
from sensors import DHT20


def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", default="./co2.db")
    args = parser.parse_args(argv[1:])
    return args


def main(args):
    sensor = DHT20(1)

    while True:
        tmp, hum = sensor.read()\
        # print(f"temperature: {tmp:.1f}, humidity: {hum:.1f}")

        with open(args.dbpath, "w") as f:
            f.writelines([f"temperature,humidity\n"
                        ,f"{tmp},{hum}\n"])
        time.sleep(20)

if __name__ == "__main__":
    args = create_parser(sys.argv)
    main(args)