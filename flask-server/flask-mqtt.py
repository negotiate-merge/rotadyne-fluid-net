import json
import sys
import os
import sys

root_dir = os.path.abspath(os.path.dirname('../d_send.py'))
sys.path.append(root_dir)
# print(sys.path)

from flask import Flask, redirect, request, jsonify
from flask_mqtt import Mqtt
from d_send import switch, pump_on, pump_off

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = '34.87.236.101'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
# Replaced device id with '+' wildcard operator. Expanding demo to muliple devices.
# topic = 'application/f65551c8-a6d4-48aa-b177-7567744a9540/device/+/event/up'
topic = [
    ('application/f65551c8-a6d4-48aa-b177-7567744a9540/device/+/event/up', 0),
    ('application/f65551c8-a6d4-48aa-b177-7567744a9540/overrides', 0)
]

mqtt_client = Mqtt(app)

devices = [
    {
        "devId": "a84041e081893e7f", 
        "title": "Demo unit",
        "lat": -33.707055119346386, 
        "lng": 151.14593296712843,
        "full": False,
        "emergency": False,
        "pumping": False,
        "override": False,
        "current": 0,
    },
    {
        "devId": "a84041e081893e80", 
        "title": "Fake unit",
        "lat": -33.703436,
        "lng": 151.152421,
        "full": False,
        "emergency": False,
        "pumping": False,
        "override": False,
        "current": 0,
    }
]

inactive = []

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    parsed_json = json.loads(message.payload)
    print('message topic -> ', message.topic)
    # Overrides section
    if 'overrides' in message.topic:
        print('override payload -> ', parsed_json)
        global inactive

        for device in devices:
            devID = device['devId']
            if devID in parsed_json: 
                device['override'] = True       # Sets the device object override variable
                inactive.append(devID)
            else: 
                device['override'] = False
                if devID in inactive: inactive.remove(devID)
        
        return redirect('/devices')
    # Device info section
    else:
        communicator = parsed_json['deviceInfo']['devEui']
        try:
            if len(parsed_json['object']) == 12:
                for d in devices:
                    if communicator == d['devId']:
                        d['pumping'] = True if parsed_json['object']['RO2_status'] == 'ON' else False     # RO2
                        d['emergency'] = True if parsed_json['object']['DI1_status'] == 'H' else False      # DI1
                        d['full'] = True if parsed_json['object']['DI2_status'] == 'L' else False        # DI2
                        
        except KeyError as e:
            # We have a different response that we want to read the output of
            # print("Payload (Expanded): \n" + json.dumps(parsed_json, indent=4))
            print('Error', e)

        # print('Received message on topic: {topic} with payload: {payload}'.format(**data))


@app.route("/devices", methods=['GET'])
def device_map():
   return devices

@app.route('/pump_overide', methods=['POST'])
def pump_overide():
    pump = request.get_json()
    # Publish device override message to mqtt topic
    o_topic = f"application/f65551c8-a6d4-48aa-b177-7567744a9540/device/{pump['devId']}/mode"
    o_message = '{"override": "%s"}'%(pump['override']) # TODO set the value here
    mqtt_client.publish(o_topic, o_message, 0)
    return redirect("/devices")

@app.route('/pump_switch', methods=['POST'])
def pump_switch():
    global inactive
    pump = request.get_json()
    try:
        if pump['devId'] in inactive:
            switch(pump['devId'], (pump_off if pump['pumping'] else pump_on))
    except:
        print('grpc call failed - no valid device at head end')
    # print(pump)

    return redirect("/devices")


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)


# Random things 
'''     # Use mosquitto_pub command via subprocess to publish override messages
subprocess.run(["mosquitto_pub", 
                "-h", "34.87.236.101", 
                "-p", "1883",
                "-t", f"application/f65551c8-a6d4-48aa-b177-7567744a9540/device/{pump['devId']}/mode",
                "-m", '{"override": "%s"}'%(value)]) #("override" if pump['pumping'] else "normal")])
'''

''' Use next and enumerate to get an object from a list by value in the object
# Get index of device
# device_index = next((index for (index, d) in enumerate(devices) if d['devId'] == devID), None)      # Find index of device
# devices[device_index]['override'] = pump['override']            # Set the objects overide value
'''

'''     Tutorial boiler plate - publish to mqtt topic
@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})
'''