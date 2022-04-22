# Rasberry-WiFi-Logger
This scipt is meant to run via crontab task and a gmail account.
When log.py is run, it will check if a conncetion to google.com is possible, if so, it will add a boolean and timestamp to the all.csv file.
if the connection works, and the previous boolean value added to the all.csv file is False, it will add to the off-to-on.csv saying that the
connection was restored with a timestamp. It's the same the other way around, if the connection doesn't work but the previous boolean value was true it will
write that the connection was lost with a timestamp.

libs you'll need to install:
- pip install requests
- pip install secure-smtplib
- pip install email

steps:
- Connect to the internet via Wi-Fi or ethernet.
- Clone the ropo to your rasberry with "git clone https://github.com/Jacob-OTW/Raspberry-WiFi-Logger.git"
- set the password, from_mail and to_mail variables to your desired addreses, if you use a diffrent SMTP server than google you'll
  have to change the arguments for the "smtplib.SMTP" and "server.connect" lines.
-(Optional) enable SSH and set a static IP for the Raspberry in your router.
- Create a crontab task, crontab -e. add "* * * * * cd {dir}; python log.py" to the crontab file to run every minute.cd
- Create a crontab task for the emails, "0 0 * * * cd {dir}; python mail.py" to send an email with the 2 csv files every day at midnight. (0 0 * * 6 for every Saturday at midnight)
