import time
from lib.switch import Switch
from lib.led import LED

class BaseState:
    def __init__(self, led):
        self.led = led

class ON(BaseState):
    def __str__(self):
        return "on"

    def run(self):
        print("state is ON")
        self.led.on()

    def change(self):
        return OFF(self.led)

class OFF(BaseState):
    def __str__(self):
        return "off"

    def run(self):
        print("state is OFF")
        self.led.off()

    def change(self):
        return ON(self.led)


class Context:
    def __init__(self):
        self.led = LED(17)
        self.state = ON(self.led)

    def change(self):
        self.state = self.state.change()

    def run(self):
        self.state.run()


def main():
    GPIONUM = 26
    switch = Switch(GPIONUM)

    model = Context()

    while True:
        if switch.is_on():
            model.change()

        model.run()
        time.sleep(0.5)

if __name__ == "__main__":
    main()