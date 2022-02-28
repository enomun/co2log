import pathlib
import datetime
from re import L
import time
import sqlite3
import time

import serial

s = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.1)

def read_co2():
    # Send command to MH-Z14A
    s.write(bytes([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]))
    # Read response
    data = s.read(9)

    # Is response length correct?
    if len(data) != 9:
        print("Response length is not correct.")
        s.reset_input_buffer()
        return None

    # Is this a valid command response?
    if data[0] != 0xFF or data[1] != 0x86:
        print("Not a valid response")
        s.reset_input_buffer()
        return None

    # Checksum
    checksum = 0xFF - (sum(data[1:7]) & 0xFF) + 1
    if checksum != data[8]:
        print("Checksum error!")
        s.reset_input_buffer()
        return None

    # Return CO2 level [ppm]
    return data[2] * 256 + data[3]


def init_db(dbpath):
    conn = sqlite3.connect(dbpath)
    cur =    conn.cursor()
    cur.execute('''CREATE TABLE co2
               (date text, co2 real)''')
    conn.close()

def main():
    dbpath = "./co2.db"
    dbpath = pathlib.Path(dbpath)
    if not dbpath.exists():
        init_db(dbpath)

    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    lastdump = time.time()
    dump_interval = 10 # sec
    log_interval = 10 # sec

    while True:
        co2 = read_co2()
        if not co2:
            continue
        now = str(datetime.datetime.now())
        values = (now, co2)
        print(values)    
        cur.execute("INSERT INTO co2 VALUES %s"%str(values))

        if time.time()- lastdump >=dump_interval:
            conn.commit()
            lastdump = time.time()
        time.sleep(log_interval)



if __name__ == "__main__":
    main()