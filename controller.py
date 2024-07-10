# Connect to Chirpstack MQTT Server and receive uplink messages using the Paho MQTT Python client library
#
# Original source:
# https://github.com/descartes/TheThingsStack-Integration-Starters/blob/main/MQTT-to-Tab-Python3/TTS.MQTT.Tab.py
#
# Instructions to use Eclipse Paho MQTT Python client library:
# https://www.thethingsindustries.com/docs/integrations/mqtt/mqtt-clients/eclipse-paho/)
#
import dm
import sys
import logging
from paho.mqtt import client as mqtt
import json
import config
import random
import re
from d_send import switch
from datetime import datetime

# Chirpstack connection details
PUBLIC_TLS_ADDRESS = config.server
APP_ID = config.app_id

PUBLIC_TLS_ADDRESS_PORT = 1883


# Meaning Quality of Service (QoS)
# QoS = 0 - at most once
# The client publishes the message, and there is no acknowledgement by the broker.
# QoS = 1 - at least once
# The broker sends an acknowledgement back to the client.
# The client will re-send until it gets the broker's acknowledgement.
# QoS = 2 - exactly once
# Both sender and receiver are sure that the message was sent exactly once, using a kind of handshake
QOS = 0
DEBUG = False

def get_value_from_json_object(obj, key):
    try:
        return obj[key]
    except KeyError:
        return '-'


def stop(client):
    client.disconnect()
    print("\nExit")
    logging.info("Controller process terminated")
    sys.exit(0)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nConnected successfully to MQTT broker")
    else:
        print("\nFailed to connect, return code = " + str(rc))

pumping = False
overrides = []

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print("\nMessage received on topic '" + message.topic + "' with QoS = " + str(message.qos))

    global pumping
    global overrides

    parsed_json = json.loads(message.payload)
    # print("length of json [object] is", len(parsed_json['object']))

    # Get device ID from message topic
    device_id = re.search("/device/(.{16})", message.topic)
    device_id = str(device_id[1])

    # Toggle override logic
    if 'mode' in message.topic:
        try:
            if parsed_json['override'] == 'True' and device_id not in overrides: overrides.append(device_id)
            if parsed_json['override'] == 'False': overrides.remove(device_id)
        except ValueError:
            print('Device not on overrides list.')
        print("Overriden devices:")
        print(overrides)

        override_topic = 'application/f65551c8-a6d4-48aa-b177-7567744a9540/overrides'
        override_message = json.dumps(overrides)
        mqttc.publish(override_topic, override_message)
        
    if 'event/up' in message.topic and device_id not in overrides:
        try:
            if len(parsed_json['object']) == 12:
                # Extract state from json 
                pumping = True if parsed_json['object']['RO2_status'] == 'ON' else False     # RO2
                emergency_switch = parsed_json['object']['DI1_status']      # DI1
                control_switch = parsed_json['object']['DI2_status']        # DI2
                pump = parsed_json['object']['RO2_status']                  # RO2

                """ Values are inverted - L indicates high, H indicates low """
                print(f'emergency = {emergency_switch}  control = {control_switch}  pump = {pump}\npumping = {pumping}')
                if emergency_switch == 'L' and control_switch == 'L' and not pumping:
                    switch(device_id, dm.r2On)              # Switch pump on
                    print("Switching pump on")
                    logging.info(f'{device_id} pumping activated')
                elif pumping:
                    if control_switch == 'H':
                        switch(device_id, dm.r2Off)             # Switch pump off
                        print("Switching pump off")
                        logging.info(f'{device_id} pumping de-activated')
                    if emergency_switch == 'H':
                        switch(device_id, dm.r2Off)             # Switch pump off
                        print("Pump turned off - emergency")
                        logging.warning(f'{device_id} pumping stopped due to emergency switch')
        except KeyError:
            # We have a different response that we want to read the output of
            print("Payload (Expanded): \n" + json.dumps(parsed_json, indent=4))    

    if DEBUG:
        # print("Payload (Collapsed): " + str(message.payload))
        print("Payload (Expanded): \n" + json.dumps(parsed_json, indent=4))

    #save_to_file(parsed_json)

# mid = message ID
# It is an integer that is a unique message identifier assigned by the client.
# If you use QoS levels 1 or 2 then the client loop will use the mid to identify messages that have not been sent.

def on_subscribe(client, userdata, mid, granted_qos):
    print("\nSubscribed with message id (mid) = " + str(mid) + " and QoS = " + str(granted_qos))


def on_disconnect(client, userdata, rc):
    print("\nDisconnected with result code = " + str(rc))


'''
def on_log(client, userdata, level, buf):
    print("\nLog: " + buf)
    logging_level = client.LOGGING_LEVEL[level]
    logging.log(logging_level, buf)
'''
# Configure logging - removed the encoding='utf-8' arg
logging.basicConfig(filename='controller.log', level=logging.INFO, \
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

print("Create new mqtt client instance")
# Added first arguement due to breaking Changes migrating to version 2 paho
# mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
mqttc = mqtt.Client(client_id) 

print("Assign callback functions")
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_disconnect = on_disconnect
# mqttc.on_log = on_log  # Logging for debugging OK, waste

logging.info("Controller process started")
print("Connecting to broker: " + PUBLIC_TLS_ADDRESS + ":" + str(PUBLIC_TLS_ADDRESS_PORT))
logging.info("Connecting to broker: " + PUBLIC_TLS_ADDRESS + ":" + str(PUBLIC_TLS_ADDRESS_PORT))
mqttc.connect(PUBLIC_TLS_ADDRESS, PUBLIC_TLS_ADDRESS_PORT, 60)

topic = [
    ("application/" + APP_ID + "/device/" + "+" + "/event/up", QOS),
    ("application/" + APP_ID + "/device/" + "+" + "/mode", QOS)
]
mqttc.subscribe(topic)
print("subscribed to topics")
for t in topic:
    print(t[0] + " with QOS = " + str(t[1]))
    logging.info("subscribed to topic " + t[0] + " with QOS = " + str(t[1]))  

print("Controller loop running")
try:
    run = True
    while run:
        mqttc.loop(10)  # seconds timeout / blocking time
        # print(".", end="", flush=True)  # feedback to the user that something is actually happening
except KeyboardInterrupt:
    stop(mqttc)
