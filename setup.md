# Machine Setup
## Gateway
- Update frimware to version: lgw-5.4.1668567157
- Navigate to 'http://<GATEWAY_ADDRESS>:8000/cgi-bin/lora-lora.has'
  - Change the frequency plan to AU915
  - Set sub Band to 1: AU915, FSB1(915.2~916.6)
  - Current mode should say: :LoRaWAN Semtech UDP
  - Hit Save & apply
- Navigate to 'http://<GATEWAY_ADDRESS>:8000/cgi-bin/lorawan.has'
  - Select: Service Provider = custom
  - Set server address to IP address or hostname of chirpstack server.
  - Uplink and downlink port should be set to `1700`
  - Secondary Lorawan server = disabled
  Save & apply.
__Gateway ssh access command:__ `ssh -p 2222 root@<GATEWAY_ADDRESS>`
__List installed packages:__ `opkg list-installed`

## Server
- Install Ubuntu server 22.04 LTS
- Follow the [chirpstack ubuntu/debian getting started guide](https://www.chirpstack.io/docs/getting-started/debian-ubuntu.html)
- Modify `/etc/chirpstack/chirpstack.toml` to only include the regions that we 
  are working with. `enabled_regions = ["au915_0",]`
__Configure firewall__
- `$ sudo ufw enable`
- `$ sudo ufw enable 22 1700 1883 8080`
__Allow mqtt connections from external host__
Add the following two lines to a the file `/etc/mosquitto/conf.d/<filename>.config`
```
allow_anonymous true
listener 1883
```
__Useful commands__
Show the logs of the gateway-bridge `$ sudo journalctl -f -n 100 -u chirpstack-gateway-bridge`
Show the logs of chirpstack `$ sudo journalctl -f -n 100 -u chirpstack`

## Chirpstack
- Login to the web UI and add your gateway
- Create an application
- Follow [this guide](https://www.chirpstack.io/docs/chirpstack/use/device-profile-templates.html) to import the device profile templates.
- Go to device profiles, then add your device (end node). For the LT22222-L, I selected `Firmware version: 1.5.6`
- Go to Applications, then your application, and you will be able to add a device of the type that you just previously imported.

### A collection of failures
Bits and peices of these resources might have worked but for the most part the material was not required and or may have just not worked at all. Nevertheless there are bits of useful information scattered about in them.
https://www.chirpstack.io/docs/guides/connect-gateway.html
https://www.chirpstack.io/docs/chirpstack-gateway-bridge/install/dragino.html
In one of above tutorials the command `wget https://artifacts.chirpstack.io/vendor/dragino/LG308/chirpstack-gateway-bridge_4.0.9-r1_mips_24kc.ipk` failed, resource does not exist.
https://www.chirpstack.io/docs/chirpstack-mqtt-forwarder/install/dragino.html