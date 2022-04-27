# Raspberry-WiFi-Logger
This script is meant to run via crontab task and a Gmail account.
When log.py is run, it will check if a connection to google.com is possible, if so, it will add a boolean and timestamp to the all.csv file.
if the connection works and the previous boolean value added to the all.csv file is False, it will add to the off-to-on.csv saying that the
connection was restored with a timestamp. It's the same the other way around, if the connection doesn't work but the previous boolean value was true it will
write that the connection was lost with a timestamp.

libs you'll need to install:
- pip install requests
- pip install secure-smtplib
- pip install email

steps:
- Connect to the internet via Wi-Fi or ethernet.
- (Opptional) If you are trying to log an enterprise wifi network, you'll need to go through a few more steps to connect. In the enterprise.txt file you'll find all the lines that need to be added.
 
- Enable auto-reconnect for Wi-Fi, "cd /etc/ifplugd/action.d/" "cp /etc/wpa_supplicant/ifupdown.sh /etc/ifplugd/action.d/ifupdown"
- Clone the repo to your raspberry with "git clone https://github.com/Jacob-OTW/Raspberry-WiFi-Logger.git"
- set the password, from_mail, and to_mail variables to your desired address, if you use a different SMTP server than google you'll
  have to change the arguments for the "smtplib.SMTP" and "server.connect" lines.
- (Optional) enable SSH and set a static IP for the Raspberry in your router.
- Create a crontab task, crontab -e. add "* * * * * cd {dir}; python log.py" to the crontab file to run every minute
- Create a crontab task for the emails, "0 0 * * * cd {dir}; python mail.py" to send an email with the 2 CSV files every day at midnight. (0 0 * * 6 for every Saturday at midnight)
- Create a crontab task for the lost emails, "0 1 * * * cd {dir}; python up-keep.py" to send any lost emails.
