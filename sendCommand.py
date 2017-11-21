"""
	First example in connecting to a mqtt broker
    For documentation about the Paho mqtt client library check:
    https://pypi.python.org/pypi/paho-mqtt/
"""
import json
import random

import sys
import time
import paho.mqtt.client as mqtt

def startClient():

    if len(sys.argv) < 2:
        sys.exit()

    device = sys.argv[1]
    status = sys.argv[2]

    print("starting client")
    cl = mqtt.Client()

    cl.connect("dev.openlabs.bth.se", 1883, 60)
    cl.loop_start()

    topic = "/devices/{}".format(device)

    payload = { "lights": status }

    cl.publish(topic, json.dumps(payload))

    cl.loop_stop()

if __name__ == '__main__':
    startClient()

