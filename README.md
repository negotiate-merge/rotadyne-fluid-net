# rotadyne-fluid-net
Initial exploration in to the use of a chirpstack lorawan implementation to facilitate the monitoring and control of waste water pumping stations.

### Objectives - past and present

- [ ] Build a simple gui app that shows (switch states, pump state, button to control pump, simple log output for verification) Use a regex on return code from systemctl status to search for active/inactive and update service state according to that. Run a status query at the end of any state change. (In Progress)
- [x] Sub process ssh issues resulting apparently from 32bit version of python, have installed 64 bit version. See the [stack-overflow post](https://stackoverflow.com/questions/65928671/python-subprocess-cant-call-ssh)
- [x] Device a way to suspend and resume pump-controller.service remotely to enable manual overide gui app. 
- [x] Increase QoS of all messaging to level 1. This is active by default in trigger mode on the end nodes. 
- [x] Automate pump controller via the use of systemd service - named 'pump-controller.service'




To use this repository it is a requirement that you have the sensitive information stored in a file named 'config.py' in the following format.
Only one is required, cloud or local.
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
