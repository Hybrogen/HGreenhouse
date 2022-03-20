#-*- coding:utf-8 -*-

import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

class HRELAY(object):
    def __init__(self, pin :int, tigger :bool = False):
        self.pin = pin
        GPIO.setup(self.p, GPIO.OUT)
        self.trigger = trigger

    def set_pin(self, pin :int):
        GPIO.cleanup()
        self.pin = pin

    def set_output(self, state :bool):
        GPIO.output(self.pin, state)

    def __del__(self):
        GPIO.cleanup()

if __name__ == '__main__':
    print('这个包含了继电器控制液泵操作的类')

