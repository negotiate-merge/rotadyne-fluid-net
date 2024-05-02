# rotadyne-fluid-net
Initial exploration in to the use of a chirpstack lorawan implementation to facilitate the monitoring and control of waste water pumping stations.

### Objectives - past and present

- [ ] Configure Port forwarding rules from WAN -> LAN to allow for control behind the gateway NAT
  - ssh WAN:2223 -> 10.130.1.210:22
  - http WAN:8080 -> 10.130.1.210:8080
  - mqtt WAN:1883 -> 10.130.1.210:1883
- [ ] When the gateway goes offline and the node is unable to communicate the messages get quede' up due to having not recevied an ack. Once the node comes back online it spams chirpstack and by extension the mqtt feed which resluts in a preriod of sporadic behaviour. This should be avoided as we do not require unecessary switching of the machine in response to events of the past, we only care about the current state in this case. Perhaps we could look at a timestamp validity check?
- [ ] Figure out how to run gui from desktop icon.
- [ ] Implement a [Logging window](https://tkdocs.com/tutorial/text.html#modifying) in to the gui app (not critical)
- [ ] Use a  verticle 'progress bar' widgit to display tank level instead of light indicator. Eg( 40% for open 80% for closed) (not critical)
- [x] Organize ssh keys for local server and fix gui usage of config.py.
- [x] Restarting the controller on server requires a poll uplink at the end of the procedure to get curent status.
- [x] Buttons display incorrectly at gui start up.
- [x] Hide the emergency light when emergency is not present but have the layout of the page maintained.
- [x] Incorporate threads in to gui app for remote procedure calls / remote commands. Connect logic to live data feeds.
- [x] Build a simple gui UI that shows switch states, pump state, button to control pump. 
- [x] Sub process ssh issues resulting apparently from 32bit version of python, have installed 64 bit version. See the [stack-overflow post](https://stackoverflow.com/questions/65928671/python-subprocess-cant-call-ssh)
- [x] Device a way to suspend and resume pump-controller.service remotely to enable manual overide gui app. 
- [x] Increase QoS of all messaging to level 1. This is active by default in trigger mode on the end nodes. 
- [x] Automate pump controller via the use of systemd service - named 'pump-controller.service'

__After cloning this repo you will need to run the following to create and enable the controller service__
```sh
$ sudo ln -sf <PATH_TO_CLONED_REPO>/rotadyne-fluid-net/pump-controller.service /etc/systemd/system/pump-controller.service
$ sudo systemctl daemon-reload
$ sudo systemctl start pump-controller
$ sudo systemctl enable pump-controller
```

__Configuration of the hardware/software stack__ can be found at [setup.md](setup.md)

Application configs need to be populated in [config.py](config.py)

Set up a venv (not covered here) and run the following to install the required dependencies.
```sh
pip install -r requirements.txt
```
