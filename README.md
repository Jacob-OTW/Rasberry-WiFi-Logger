# Rasberry-WiFi-Logger
This scipt is meant to run via crontab and a gmail account.
When log.py is run, it will check if a conncetion to google.com is possible, if so, it will add a boolean and timestamp to the all.csv file.
if the connection works, and the previous boolean value added to the all.csv file is False, it will add to the off-to-on.csv saying that the
connection was restored with a timestamp. It's the same the other way around, if the connection doesn't work but the previous boolean value was true it will
write that the connection was lost with a timestamp.

libs you'll need to install:
- pip install requests
- pip install secure-smtplib
- pip install email

steps:
- Clone the ropo to your rasberry with "git clone"
- Create a crontab task, crontab -e. add "* * * * * cd {dir}; python log.py" to the crontab file to run every minute.cd
