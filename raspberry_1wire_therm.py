

"""

This requires the 1-wire kernel module (w1-gpio) to be loaded and configured, as instructed below.

To load the 1-wire kernel modules needed:

sudo modprobe w1-gpio
sudo modprobe w1-therm

Then either,
sudo dtoverlay w1-gpio gpiopin=4 pullup=0

(
or:
cat "dtoverlay=w1-gpio" >> /boot/config.txt
reboot
)


to find the id of your connected 1-wire sensor:
ls /sys/bus/w1/devices/

this code is proudly inspired by:
https://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
Big thanks to The guys at modmypi!

"""

import os
import time

def osSetup():
    os.system("modprobe w1-gpio")
    os.system("modprobe w1-therm")
    os.system("dtoverlay w1-gpio gpiopin=4 pullup=0")


def read_sensor_raw(name):
    sensor_path = "/sys/bus/w1/devices/{}/w1_slave".format(name)
    f = open(sensor_path, "r")
    lines = f.readlines()
    f.close()
    return lines

def read_temperature(name):
    lines = read_sensor_raw(name)
    # wait until we have a line ending with "YES"
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_sensor_raw(name)
    
    # Then read the value after the t=
    temp_out = lines[1].find("t=")
    if temp_out != -1:
        temp_string = lines[1].strip()[temp_out+2:]
        return float(temp_string) / 1000.0

if __name__ == '__main__':
    temperature = read_temperature("28-00000588bf23")
    print(temperature)
