# Raspberry-WiFi-Logger
This script is meant to run via crontab task and any ssl email service which supports SMTP from insecure sources, but could also easily be adapted to work with other forms of regularly retrieving the log files.
### Here's how it works
```log.py``` will check if a connection to google.com is possible, if so, it will add a boolean, latency, and a timestamp to the ```all.csv``` file. 
If a connection is possible, but the previous check failed, it will add to the ```off-to-on.csv``` saying that the
connection was restored with a timestamp. It's the same the other way around, if the connection doesn't work but the previous boolean value was true it will
write that the connection was lost with a timestamp.

Python libraries you'll need to install
```
pip install requests
pip install secure-smtplib
pip install email
```

## Setup
- Connect the raspberry pi to the wireless network. If you are trying to log an enterprise network, you'll need to go through a few more steps that are listed below to connect.
- Enable auto-reconnect for Wi-Fi, with ```cd /etc/ifplugd/action.d/``` followed by ```cp /etc/wpa_supplicant/ifupdown.sh /etc/ifplugd/action.d/ifupdown``` in the terminal.
- Clone the repo to your raspberry with ```git clone https://github.com/Jacob-OTW/Raspberry-WiFi-Logger.git```
- Fill out the ```config.py``` file. 
- (Optional, but recommended for remote maintenance) Enable SSH and set a static IP for the Raspberry, add the following lines to ```/etc/dhcpcd.conf```
```interface eth0
  static ip_address={ip}/24
  static routers={default_gateway}
  static domain_name_server={default_gateway}
  static domain_search=
  nogateway
  ```
Don't forget to replace the values with real ip addresses in your range.
If a gateway for eth0 was already created, run ```sudo ip route del default``` to delete it.

- Add the following crontabs
```
* * * * * cd Raspberry-WiFi-Logger; python log.py &
0 0 * * * cd Raspberry-WiFi-Logger; python mail.py &
0 1 * * * cd Raspberry-WiFi-Logger; python up-keep.py &
```
(if you didn't clone the repo to the default directory, you'll need to change the path for the ```cd``` command)
This will 
1. check for a connection every minute. 2. 
2. email you every day at midnight. 3. 
3. try email you every hour in case the email at midnight failed.

## Connecting to enterprise-networks:
- add the following lines to ```/etc/network/interfaces```
```
auto lo 
iface eth0 inet dhcp

auto wlan0
allow-hotplug wlan0
iface wlan0 net dhcp
 pre-up wpa_supplicant -B -D wext -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
 post-down killall -q wpa_supplicant
```

- add the following lines to ```/etc/dhcpcd.conf```
```
interface wlan0
env ifwireless = 1
env wpa_supplicant_driver = wext , nl80211
```

- Add the following lines to ```/etc/wpa_supplicant/wpa_supplicant.conf``` don't forget to change the values for SSID, identity, and password. 
```
network={
 ssid="{name}"
 priority=1
 proto=RSN
 key_mgmt=WPA-EAP
 pairwise=CCMP
 auth_alg=OPEN
 eap=PEAP
 identity="{username}"
 password="{your password}"
 phase1="peaplabel=0"
 phase2="auth=MSCHAPV2"
}
```




Should your Raspberry not automatically set its date and time, you can manually set it with "sudo date -s 'YYYY-MM-DD HH:MM:SS'" (example: 2nd of Mai 2022 at 12:30:00 --> "sudo date -s '2022-05-02 12:30:00'")
