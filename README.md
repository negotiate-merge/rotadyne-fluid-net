# rotadyne-fluid-net
Initial exploration in to the use of a chirpstack lorawan implementation to facilitate the monitoring and control of waste water pumping stations.

### Objectives - past and present

#### Next steps
Main objectives
- Build a web app that displays pump locations and allows reading of status and manual pump control as follows: 
- High importance items
  1. Verification of high high level
  2. Remote turn off
  3. Reading from presure sensor

- For the Ui the following things need to be considered.
  1. The page should have a google map type view and the pump locations should be indicated by a dot.
  2. These dots should be coloured { green: pump-running, orange: standby, red: emergency }
  3. Hover over or clicking on a dot should bring up the information on the pump (Water pressure, amps drawn) or take to an independant screen where these actions can be triggered.



The current scada system in use is the scadapack 334 by schnieder. Need to look in to this to detirmine how it functions and how we can interface with it.


- [ ] When the gateway goes offline and the node is unable to communicate the messages get quede' up due to having not recevied an ack. Once the node comes back online it spams chirpstack and by extension the mqtt feed which resluts in a preriod of sporadic behaviour. This should be avoided as we do not require unecessary switching of the machine in response to events of the past, we only care about the current state in this case. Perhaps we could look at a timestamp validity check?
- [ ] Having issue with config.py and pump-controller.service remaining as a default file (without specific info) in github. Only want it to be pulled on initial clone, then to be configured by user, but do not want the file pushed or pulled beyond that point.
- [x] Restarting the controller on server requires a poll uplink at the end of the procedure to get curent status.
- [x] Sub process ssh issues resulting apparently from 32bit version of python, have installed 64 bit version. See the [stack-overflow post](https://stackoverflow.com/questions/65928671/python-subprocess-cant-call-ssh)

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
