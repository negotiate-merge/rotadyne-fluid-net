# rotadyne-fluid-net
Initial exploration in to the use of a chirpstack lorawan implementation to facilitate the monitoring and control of waste water pumping stations.

To use this repository it is a requirement that you have the sensitive information stored in a file named 'config.py' in the following format
```sh
cloud_server = "<ip-address>"
local_server = "<ip-address>"

# d_send.py sensitive config info
api_token_cloud = "<api-token-from chirpstack>"
api_token_local = "<api-token-from chirpstack>"

#controller.py sensitive config info
local_appID = "<app-id-from-chirpstack>"
cloud_appID = "<app-id-from-chirpstack>"
```

Set up a venv (not covered here) and run the following to install the required dependencies.
```sh
pip install -r requirements.txt
```
