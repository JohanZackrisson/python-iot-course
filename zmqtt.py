""" Helper class for handling subscriptions and triggers to mqtt """

import ast
import json
import paho.mqtt.client as mqtt

def unicode2utf8(input):
    if isinstance(input, dict):
        return {unicode2utf8(key): unicode2utf8(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [unicode2utf8(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


class zmqtt(object):

    def __init__(self, host=None, port=None, clientId=""):
        #pprint("__init__")
        #pprint(self)
        self.triggers = []
        self.isConnected = False

        self.mqtt = mqtt.Client(clientId)
        self.mqtt.on_message = self._callback(self._on_message)
        self.mqtt.on_connect = self._callback(self._on_connect)
        self.mqtt.on_disconnect = self._callback(self._on_disconnect)
        self.mqtt.on_publish = self._callback(self._on_publish)
        self.mqtt.on_subscribe = self._callback(self._on_subscribe)
        #self.mqtt.on_log = self._callback(self._on_log)

        if host and port:
            self.connect(host, port)

    def _callback(self, fn):
        def wrapper(*v):
            fn(*v)
        return wrapper

    # handler functions
    def _on_message(self, mqttc, obj, msg):
        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        self._callTriggers(msg.topic, msg.payload)
        pass

    def _on_connect(self, mqttc, userdata, flags, result):
        #print("connected")
        #pprint(self)
        self.isConnected = True
        self._subscribeTriggers()
        #self.mqtt.subscribe("#")
        print("connect result: ", result)

    def _on_disconnect(self, client, userdata, rc):
        print(client, userdata, rc)

    def _on_publish(self, mqttc, obj, mid):
        pass

    def _on_subscribe(self, mqttc, obj, mid, granted_qos):
        pass

    def _on_log(self, client, userdata, level, buf):
        print("Log: ", client, userdata, level, buf)

    def _decodeJSON(self, jsondata):
        try:
            return json.loads(jsondata)
        except ValueError:
            try:
                return ast.literal_eval(jsondata)
            except ValueError:
                print("data is not recognized")
                return None
            #print("data is not json")
            #return None

    # external functions
    def connect(self, host, port):
        self.mqtt.connect(host, port, 60)

    # Decorator
    def trigger(self, topic, json=True):
        #print("trigger added: %s %s" % (topic, json))
        def triggerdecorator(func):
            def triggerwrapper(*v, **kv):
                #print("triggerwrapper")
                func(*v, **kv)
            self.triggers.append([topic, func, json])
            return triggerwrapper
        return triggerdecorator

    def _callTriggers(self, topic, data):
        for t in self.triggers:
            #print("testing topic: %s %s" % (t[0], topic) )
            if mqtt.topic_matches_sub(t[0], topic):
                #print "Trigger matches: %s %s" % (t[0] , t[1] )
                if (t[2]):  # wants json
                    #print("decoding json")
                    #pprint(data)
                    data = self._decodeJSON(str(data))
                    #pprint(data)
                t[1](topic, data)

    def _subscribeTriggers(self):
        for t in self.triggers:
            print("subscribeTriggers: ", t)
            self.mqtt.subscribe(t[0])

    def publish(self, topic, data, format="json", qos=0, retain=False):
        if format == "json":
            # encode as json before publishing
            data = unicode2utf8(json.dumps(data))

        self.mqtt.publish(topic, data, qos, retain)
        #print("%s %s" % (topic, data))

    '''
        spins forever
        TODO: run the loop on its own thread?
    '''

    def start(self):
        self.mqtt.loop_forever()

    def startInBackground(self):
        self.mqtt.loop_start()

    def stop(self):
        self.mqtt.loop_stop()


def test():
    mq = zmqtt()

    @mq.trigger("#", False)
    def all(topic, data):
        print("debug trigger: %s %s" % (topic, data))

    mq.connect("test.mosquitto.org", 1883)
    mq.start()

if __name__ == '__main__':
    test()
