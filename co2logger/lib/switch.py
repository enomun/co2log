import RPi.GPIO as GPIO


class Switch:
    def __init__(self, gpio_id):
        self.gpio_id = gpio_id
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_on(self):
        sw_status = GPIO.input(self.gpio_id)
        if sw_status==0:
            return True
        else:
            return False