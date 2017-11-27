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

import raspberry_1wire_therm as therm

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
            "value": therm.read_temperature("28-00000588bf23"),
            "name": "28-00000588bf23",
        }
        self.mqttclient.publish(deviceTopic(self.client_id), json.dumps(payload), 1)

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(deviceTopic(self.client_id))

    def on_message(self, client, userdata, message):
        """ mqtt library callback on incomming messages """
        print(message.topic + " " + str(message.qos))
        try:
            # print(msg.payload)
            jsondata = json.loads(str(message.payload))
            print(jsondata)
            self.on_command(jsondata)
        except ValueError:
            print("not json, ValueError")
        except TypeError:
            print("not json, TypeError")

    def on_command(self, payload):
        if not "lights" in payload:
            return
        if payload["lights"] == "on":
            print("TURN THE LIGHTS ON")
        if payload["lights"] == "off":
            print("TURN THE LIGHTS OFF!!")

def startClient():
    print("starting client")
    cl = mqtt.Client()

    cl.connect("dev.openlabs.bth.se", 1883, 60)
    cl.loop_start()

    sensor = MqttSensor("johans_andra_sensor", cl)

    cl.on_connect = sensor.on_connect
    cl.on_message = sensor.on_message

    running = True

    while running:
        try:
            sensor.report()
            time.sleep(10)
        except KeyboardInterrupt:
            print("stop?")
            running = False
    
    sensor.stop()
    cl.loop_stop()

if __name__ == '__main__':
    startClient()

