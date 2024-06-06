from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
import json

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = '34.87.236.101'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
# Replaced device id with '+' wildcard operator. Expanding demo to muliple devices.
topic = 'application/f65551c8-a6d4-48aa-b177-7567744a9540/device/+/event/up'

mqtt_client = Mqtt(app)

devices = [
    {
        "devId": "a84041e081893e7f", 
        "title": "Demo unit",
        "lat": -33.707055119346386, 
        "lng": 151.14593296712843,
        "full": False,
        "emergency": False,
        "current": 0,
    },
    {
        "devId": "a84041e081893e80", 
        "title": "Fake unit",
        "lat": -33.703436,
        "lng": 151.152421,
        "full": False,
        "emergency": False,
        "current": 0,
    }
]

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    # data = dict(
    #     topic=message.topic,
    #     payload=message.payload.decode()
    # )

    parsed_json = json.loads(message.payload)
    communicator = parsed_json['deviceInfo']['devEui']
    # print("length of json [object] is", len(parsed_json['object']))

    # print(f"communicator: {communicator}\tDevices: {devices}")
    try:
        if len(parsed_json['object']) == 12:
            for d in devices:
                print(communicator, d['devId'])
                pass
                if communicator == d['devId']:
                    d['pumping'] = True if parsed_json['object']['RO2_status'] == 'ON' else False     # RO2
                    d['emergency'] = True if parsed_json['object']['DI1_status'] == 'H' else False      # DI1
                    d['full'] = True if parsed_json['object']['DI2_status'] == 'L' else False        # DI2
                    
                    line = f"Devices dict has:\n\
                        Pumping: {d['pumping']}\n\
                        Emergency: {d['emergency']}\n\
                        Full: {d['full']}\n\
Returned JSON has:\n\
                        Pumping: {parsed_json['object']['RO2_status']}\n\
                        Emergency: {parsed_json['object']['DI1_status']}\n\
                        Full: {parsed_json['object']['DI2_status']}\n"
                    # print(line)

        # print(devices[communicator])

    except KeyError as e:
        # We have a different response that we want to read the output of
        # print("Payload (Expanded): \n" + json.dumps(parsed_json, indent=4))
        print('Error', e)

    # print('Received message on topic: {topic} with payload: {payload}'.format(**data))
    # return devices


@app.route("/devices")
def device_map():
#    print(devices)
   return devices


@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
