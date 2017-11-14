"""
	First example in connecting to a mqtt broker
    For documentation about the Paho mqtt client library check:
    https://pypi.python.org/pypi/paho-mqtt/
"""
import json
#from pprint import pprint
import random

#import signal
#import sys
import time
#import threading
import paho.mqtt.client as mqtt

def presenceTopic(device):
    return "/presence/{}".format(device)

def deviceTopic(device):
    return "/devices/{}".format(device)

class MqttPresence(object):
    """ This class reports when a sensor connects and disconnects """

    def __init__(self, client_id, mqttclient):
        self.mqttclient = mqttclient
        self.client_id = client_id
        self.mqttclient.publish(presenceTopic(self.client_id), json.dumps({"status": "online"}), 1)

    def stop(self):
        self.mqttclient.publish(presenceTopic(self.client_id), json.dumps({"status": "offline"}), 1)

class MqttSensor(MqttPresence):
    """ This is a sensor that reports randomized values """

    def __init__(self, client_id, mqttclient):
        super(MqttSensor, self).__init__(client_id, mqttclient)
        self.client_id = client_id
        self.mqttclient = mqttclient

    def report(self):
        payload = {
            "type": "temperature",
            "value": random.randint(15, 25)
        }
        self.mqttclient.publish(deviceTopic(self.client_id), json.dumps(payload), 1)

def startClient():
    print("starting client")
    cl = mqtt.Client()

    cl.connect("dev.openlabs.bth.se", 1883, 60)
    cl.loop_start()

    sensor = MqttSensor("johans_sensor", cl)

    running = True

    while running:
        try:
            sensor.report()
            time.sleep(1)
        except KeyboardInterrupt:
            print("stop?")
            running = False
    
    sensor.stop()
    cl.loop_stop()

if __name__ == '__main__':
    startClient()

