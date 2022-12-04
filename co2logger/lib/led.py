import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート

class LED:
    def __init__(self, gpio_id):
        self.gpio_id =gpio_id            

        GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
        GPIO.setup(gpio_id, GPIO.OUT)       #GPIO18を出力モードに設定

    def on(self):
        GPIO.output(self.gpio_id, GPIO.HIGH)
        
    def off(self):
        GPIO.output(self.gpio_id, GPIO.LOW)
