# rotadyne-fluid-net
Initial exploration in to the use of a chirpstack lorawan implementation to facilitate the monitoring and control of waste water pumping stations.

### Objectives - past and present

- [ ] When the gateway goes offline and the node is unable to communicate the messages get quede up due to having not recevied an ack.. then once the node comes back online it spams chirpstack and by extension the mqtt feed which resluts in a preriod of sporadic behaviour. This should be avoided somehow as we do not require unecessary switching of the machine in response to events of the past we only care about the current state in this case. Perhaps we could look at a timestop validity check?
- [ ] Figure out how to run gui from desktop icon.
- [ ] Implement a [Logging window](https://tkdocs.com/tutorial/text.html#modifying) in to the gui app (not important)
- [ ] Use a  verticle 'progress bar' widgit to display tank level instead of light indicator. Eg( 40% for open 80% for closed)
- [x] Restarting the controller on server requires a poll uplink at the end of the procedure to get curent status.
- [x] Buttons display incorrectly at gui start up.
- [x] Hide the emergency light when emergency is not present but have the layout of the page maintained.
- [x] Incorporate threads in to gui app for remote procedure calls / remote commands. Connect logic to live data feeds.
- [x] Build a simple gui UI that shows switch states, pump state, button to control pump. 
- [x] Sub process ssh issues resulting apparently from 32bit version of python, have installed 64 bit version. See the [stack-overflow post](https://stackoverflow.com/questions/65928671/python-subprocess-cant-call-ssh)
- [x] Device a way to suspend and resume pump-controller.service remotely to enable manual overide gui app. 
- [x] Increase QoS of all messaging to level 1. This is active by default in trigger mode on the end nodes. 
- [x] Automate pump controller via the use of systemd service - named 'pump-controller.service'


We are using python 3.11 64 bit. Could not run ssh via subprocess as we had 32 bit pythonn installed and the ssh program was 64 bit.

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
