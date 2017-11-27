

"""

Testing to get rpi gpio to work

"""

import os
import time

import RPi.GPIO as GPIO

digital_pin = 17

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(digital_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_gpio():
    return GPIO.input(digital_pin)

if __name__ == '__main__':
    setup_gpio()
    while True:
        binary = read_gpio()
        print(binary)
        time.sleep(1.0)
