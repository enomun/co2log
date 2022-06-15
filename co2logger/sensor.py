import serial
import random


class CO2Reader:
    """
    for MH-Z14
    """

    def __init__(self, device, debug=False):
        print("initializing CO2 reader")
        if not debug:
            self.s = serial.Serial(device, baudrate=9600, timeout=0.1)
            self.stop_auto_calibration()
            self.read = self.read_co2
        else:
            self.read = self.read_dummy

    def stop_auto_calibration(self):
        print("sending stop auto calibration command")
        self.s.write(bytes([0xFF, 0x01, 0x79, 0x00, 0x00, 0x00, 0x00, 0x00, 0x86]))

    def start_auto_calibration(self):
        print("sending start auto calibration command")
        self.s.write(bytes([0xFF, 0x01, 0x79, 0xA0, 0x00, 0x00, 0x00, 0x00, 0xE6]))

    def calibrate(self):
        print("sending calibration command")
        self.s.write(bytes([0xFF, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78]))
        print("CO2 concentration after calibration: ", self.read_co2())

    def read_co2(self):
        print("Reading sensor information")
        # Send command to
        self.s.write(bytes([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]))
        # Read response
        data = self.s.read(9)

        # Is response length correct?
        if len(data) != 9:
            print("Response length is not correct.")
            self.s.reset_input_buffer()
            return None

        # Is this a valid command response?
        if data[0] != 0xFF or data[1] != 0x86:
            print("Not a valid response")
            self.s.reset_input_buffer()
            return None

        # Checksum
        checksum = 0xFF - (sum(data[1:7]) & 0xFF) + 1
        if checksum != data[8]:
            print("Checksum error!")
            self.s.reset_input_buffer()
            return None

        # Return CO2 level [ppm]
        return data[2] * 256 + data[3]

    def read_dummy(self):
        default = 400
        return default + random.random() * 50
