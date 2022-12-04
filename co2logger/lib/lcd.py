import time

import RPi.GPIO as GPIO  

from . import i2clcda


class LCD:
    def __init__(self, gpio_id=None):
        self.gpio_id =gpio_id            

        if gpio_id is not None:
            print("using gpio for display: %d"%self.gpio_id)

            GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
            GPIO.setup(self.gpio_id, GPIO.OUT) 

        LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
        self.rows = [LCD_LINE_1, LCD_LINE_2]
        self.init()


    def init(self):
        if self.gpio_id is not None:
            GPIO.output(self.gpio_id, GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.gpio_id, GPIO.HIGH)
            time.sleep(1)
        i2clcda.lcd_init()

    def show(self, string, row=1):
        i2clcda.lcd_string(string, self.rows[row])

    def clear(self):
        print("clearning")
        i2clcda.lcd_end()
        if self.gpio_id is not None:
            GPIO.output(self.gpio_id, GPIO.LOW)

