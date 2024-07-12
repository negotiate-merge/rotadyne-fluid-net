# rotadyne-fluid-net
Exploration in to the use of a chirpstack lorawan implementation to facilitate the monitoring and control of waste water pumping stations.

### Objectives - past and present
The current scada system in use is the scadapack 334 by schnieder. Need to look in to this to detirmine how it functions and how we can interface with it.
^ It's a client server model.

__Front end__
- [ ] Reading from presure sensor
- [ ] Unsure if this a real thing, will keep an eye on it. "react objects not updating when backend redirects to /devices"

__Back end__
- [x] Devise a method of removing a device from the controller logic when pump override is implemented.
- [x] Publish to an overrides topic the list overrided devices for retrieval on flask/react.
- [x] The flask application starts up with no knowledge of the status of the nodes. It will need to run a poll on each device in order to get thier current status. This should only run once on start-up possibly as part of the on con-connect or on-subsribe callback functions.
- [x] When device is overridden and pump is running with the high switch inactive, setting the mode back to automatic does not immediately turn the pump off. When the device is removed from the overridden list we need to poll it for its current status.
- [ ] Using the switch button to manually control the function of the pump does not produce mqtt messages and events are not logged. Not a major issue at present but worth noting.
- [ ] Incorporate security through mqtt and ssl. Deploy.
- [x] Restarting the controller on server requires a poll uplink at the end of the procedure to get curent status.

__Infrastructure__
- [ ] When the gateway goes offline and the node is unable to communicate the messages get quede' up due to having not recevied an ack. Once the node comes back online it spams chirpstack and by extension the mqtt feed which resluts in a preriod of sporadic behaviour. This should be avoided as we do not require unecessary switching of the machine in response to events of the past, we only care about the current state in this case. Perhaps we could look at a timestamp validity check?


### Next steps
- [X] Add pump control button functionality, might require another branch as is major overhaul.
- [X] Build out the Infowindow UI so that it incorporates all of the device object data.
- [X] Connect app to Flask backend so that the json object is able to be passed through in a consumable format.
- [X] Build out the flask-mqtt application in order to parse out information of relevance from the mqtt feed, update and return json objects.
- [X] Figure out how to get react to periodically retrieve data from the flask-mqtt endpoint

## Notes
IMPORTANT - I inadvertantly created a DOS on the end node by making changes to the react app that would send downlinks everytime the useEffect fucntion ran. This was due to onClick calling the function directly instead of as an arguement to an anonymous function thereby making it a handler or something. will need to look in to this, moral of the story though, be absolutely sure that your program does not spam the end node as it will easily be overwhelmed particularly if confirmed downlinks are used.

Youtube [tutorial](https://www.youtube.com/watch?v=YyuyqPVQNrs) detailing how to set map theme to dark mode or in our case aubergine.
React front end with flask back end, follow [this tutorial.](https://www.youtube.com/watch?v=7LNl2JlZKHA)

### Set up a React map web application
Installation of node is not straight forward. Follow this [freeCodeCamp tutorial](freecodecamp.org/news/how-to-install-node-js-on-ubuntu/) to get it done right.

There are are modifications to the ~/.bashrc file that may need correcting in order to function properly.

```sh
# Create a react app
$ npx create-react-app <app_name>

# Install the required library
$ npm install @vis.gl/react-google-maps
```

To run the react app
`$ npm start`

__After cloning this repo you will need to run the following to create and enable the controller service__
```sh
$ sudo ln -sf <PATH_TO_CLONED_REPO>/rotadyne-fluid-net/pump-controller.service /etc/systemd/system/pump-controller.service
$ sudo systemctl daemon-reload
$ sudo systemctl start pump-controller
$ sudo systemctl enable pump-controller
```

__Configuration of the hardware/software stack__ can be found at [setup.md](setup.md)

Application configs need to be populated in [config.py](config.py)

