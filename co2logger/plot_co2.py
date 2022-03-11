#!/usr/bin/env python
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date
import pandas as pd

from database import DB


def create_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpath", default="/db/co2.db")
    parser.add_argument("--outpath", default="./debug/co2concentrations.png")
    parser.add_argument("--interval", type=int, default=0)
    args = parser.parse_args(argv[1:])

    return args


def predict(xs, co2, now):
    time_fit_minute = 5
    time_pred_minute = 20

    time_fit = time_fit_minute / (60 * 24)
    time_pred = time_pred_minute / (60 * 24)
    num_pred = len(xs[xs > xs[-1] - time_fit])

    xs = xs[-num_pred:]
    ys = co2[-num_pred:]

    xs_pred = np.asarray([xs[0], now + time_pred])
    coef1 = np.polyfit(xs, ys, 1)
    ys_pred = coef1[0] * xs_pred + coef1[1]
    return xs_pred, ys_pred


def add_prediction(ax, times, co2, now):
    num_check = 1000
    xoff = 0.1 / 60 / 24
    yoff = 10

    xs = np.asarray([date2num(t) for t in times[-num_check:]])
    ys = co2

    # plot prediction
    xs_pred, ys_pred = predict(xs, ys, now)

    # add info about prediction
    ax.plot(xs_pred, ys_pred, linestyle="dotted")
    ax.scatter([xs_pred[-1]], [ys_pred[-1]], color="r")
    if ys_pred[-1] > 300:
        text = "%.1f\n@%s" % (ys_pred[-1], num2date(xs_pred[-1]).strftime("%H:%M"))
        ax.text(xs_pred[-1] + xoff, ys_pred[-1] + yoff, text, ha="left", va="bottom")

    # add info about now
    ax.scatter([xs[-1]], [ys[-1]], color="r", zorder=10)
    text = "%.1f" % (ys[-1])
    ax.text(xs[-1] + xoff, ys[-1] + yoff, text, ha="left", va="bottom")

    # adjust xlim
    xmin = now - 3 / 24
    xmax = now + 0.75 / 24
    ax.set_xlim([xmin, xmax])

    # adjust ylim
    idx_xmin = len(xs[xs > xmin])
    ys = co2[-idx_xmin:]

    ymin = min(ys.min(), ys_pred.min())
    ymax = max(ys.max(), ys_pred.max())

    ystep_approx = (ymax - ymin) / 6

    if ys_pred[-1] > ys.max():  # increasing
        ymax = ymin + 7 * ystep_approx
    else:
        ymin = ymax - 7 * ystep_approx
        ymin = max(ymin, 350)

    ymin = min(ymin, 350)
    ymax = max(ymax, 1150)
    ax.set_ylim([ymin, ymax])


def create_figure(times, co2, outpath, enlarged=False):
    threshold = 1000

    co2now = co2[-1]
    datenow = datetime.now()
    now = datenow.strftime("%Y-%m-%d %H:%M:%S")

    # comon settings
    fig = plt.figure()
    fig.suptitle("Last updated: %s" % (now))
    ax = fig.add_subplot(111)
    ax.grid(which="major", axis="y", color="k", alpha=0.2)
    ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
    ax.set_ylabel(r"$\mathrm{CO}_2$ concentration [ppm]")

    plt.xticks(rotation=50)

    # main plot
    ax.plot(times, co2)

    # add threshold line
    xlim = ax.get_xlim()
    tmin = date2num(times[0]) - 1
    tmax = date2num(times[-1]) + 1
    ax.plot([tmin, tmax], [threshold, threshold], "k--")
    ax.set_xlim(xlim)

    ymin, ymax = ax.get_ylim()
    ymin = min(ymin, 350)
    ymax = min(max(ymax, 1150), 1500)
    ax.set_ylim([ymin, ymax])

    if enlarged:
        now = date2num(datenow)
        add_prediction(ax, times, co2, now)

    fig.tight_layout()
    fig.savefig(outpath)
    fig.clf()
    plt.close(fig)


def read_data(args):
    sql = 'select * from co2'

    db = DB(args.dbpath)
    df = pd.read_sql_query(sql, db.con)
    db.close()

    times = [datetime.strptime(date.strip(), "%Y-%m-%d %H:%M:%S.%f") for date in df["date"]]
    co2 = df["co2"].values

    return times, co2


def main(args):
    while True:
        now = str(datetime.now())
        times, co2 = read_data(args)

        # create figures
        create_figure(times, co2, args.outpath)
        p = Path(args.outpath)
        outpath2 = p.parent / (p.stem + "2" + p.suffix)
        create_figure(times, co2, outpath2, enlarged="True")

        print("figure updated: %s" % now)

        if args.interval <= 0:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    args = create_parser(sys.argv)
    main(args)