#!/usr/bin/env python
import sys
import argparse
import time
from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date
import pandas as pd

from database import DB


def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", default="/db/co2.db")
    parser.add_argument("--outpath", default="co2concentrations.png")
    parser.add_argument("--interval", type=int, default=0)
    args = parser.parse_args(argv[1:])

    return args


def create_figure(times, co2, outpath, enlarged=False):
    threshold = 1000

    co2now = co2[-1]
    datenow = datetime.now()
    now = datenow.strftime("%Y-%m-%d %H:%M:%S")

    fig = plt.figure()
    fig.suptitle("CO2 concentration: %d\nLast updated: %s" % (co2now, now))
    ax = fig.add_subplot(111)
    ax.grid(which="major", axis="y", color="k", alpha=0.2)
    ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
    plt.xticks(rotation=50)

    # main plot
    ax.plot(times, co2)

    # add threshold line
    xlim = ax.get_xlim()
    tmin = date2num(times[0]) - 1
    tmax = date2num(times[-1]) + 1
    ax.plot([tmin, tmax], [threshold, threshold], "k--")
    ax.set_xlim(xlim)

    if enlarged:
        # fit data
        num_pred = 100
        xs = np.asarray([date2num(t) for t in times[-num_pred:]])
        ys = co2[-num_pred:]
        coef1 = np.polyfit(xs, ys, 1)

        # add prediction
        time_pred = 20 / 60 / 24
        now = date2num(datenow)

        xs_plot = np.asarray([xs[0], now + time_pred])
        ys_plot = coef1[0] * xs_plot + coef1[1]
        ax.plot(xs_plot, ys_plot, linestyle="dotted")

        text = num2date(xs_plot[-1]).strftime("%H:%M")
        ax.scatter([xs_plot[-1]], [ys_plot[-1]], color="r")
        ax.text(xs_plot[-1] - 10 / 60 / 24, ys_plot[-1] + 30,
                "%.1f\n@%s" % (ys_plot[-1], text))

        ax.set_xlim([now - 3 / 24, now + 0.7 / 24])

    ymin, ymax = ax.get_ylim()
    ymin = min(ymin, 350)
    ymax = min(max(ymax, 1150), 1500)
    ax.set_ylim([ymin, ymax])

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

        times = [
            datetime.strptime(date.strip(), "%Y-%m-%d %H:%M:%S.%f")
            for date in df["date"]
        ]
        co2 = df["co2"].values

        create_figure(times, co2, args.outpath)
        spl = args.outpath.split(".")
        print(spl)
        outpath2 = ".".join([spl[0] + "2", spl[1]])
        print(outpath2)

        create_figure(times, co2, outpath2, enlarged="True")

        print("figure updated: %s" % now)

        if args.interval <= 0:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    args = create_parser(sys.argv)
    main(args)