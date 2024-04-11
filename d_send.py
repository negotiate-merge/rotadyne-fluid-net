import os
import sys

import grpc
from chirpstack_api import api
import config

API_PORT = '8080'

# This must point to the API interface.
server = config.cloud_server + ':' + API_PORT
# The API token (retrieved using the web-interface).
api_token = config.api_token_cloud

def switch(dev_eui:str, byte_object):
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    # Device-queue API client.
    client = api.DeviceServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    req = api.EnqueueDeviceQueueItemRequest()
    req.queue_item.confirmed = False
    req.queue_item.data = byte_object
    req.queue_item.dev_eui = dev_eui
    req.queue_item.f_port = 2

    resp = client.Enqueue(req, metadata=auth_token)

    # Print the downlink id
    print(resp.id)

if __name__ == '__main__':
    dev_eui = "a84041e081893e7f"
    data_string = input("Enter hex string: ").encode('ascii')

    while len(data_string) % 2 != 0:
        data_string = input("Length must be divisible by 2 - Enter valid hex string: ")

    byte_values = [int(data_string[i:i+2], 16) for i in range(0, len(data_string), 2)]
    byte_object = bytes(byte_values)

    print(f'Sending {byte_object} to {dev_eui}')
    switch(dev_eui, byte_object)
