"""
	First example in connecting to a mqtt broker
    For documentation about the Paho mqtt client library check:
    https://pypi.python.org/pypi/paho-mqtt/
"""
import json
from pprint import pprint
import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, returncode):
    """ mqtt library callback on connect """
    mqttc.subscribe("#", 0)
    print("------------------------------------------")
    print("------------------------------------------")
    print("------------------------------------------")

    print("rc: " + str(returncode))


def on_message(client, userdata, message):
    """ mqtt library callback on incomming messages """
    print(message.topic + " " + str(message.qos))
    try:
        # print(msg.payload)
        jsondata = json.loads(str(message.payload))
        pprint(jsondata)
    except ValueError:
        print("not json, ValueError")
    except TypeError:
        print("not json, TypeError")


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, userdata, level, buf):
    print("Log: " + buf)


def startClient():
    print("starting client")
    cl = mqtt.Client()
    cl.on_message = on_message
    cl.on_connect = on_connect
    cl.on_publish = on_publish
    cl.on_subscribe = on_subscribe

    #cl.connect("test.mosquitto.org", 1883, 60)
    cl.connect("dev.openlabs.bth.se", 1883, 60)
    cl.loop_forever()

if __name__ == '__main__':
    startClient()
