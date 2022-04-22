from mail import send_mail
import requests
import os

url = 'https://google.com'
timeout = 10

try:
    requests.get(url, timeout=timeout)
    connection = True
except (requests.ConnectionError, requests.Timeout) as exception:
    connection = False

if connection and os.stat('waiting.csv').st_size != 0:
    with open('waiting.csv') as file:
        lines = file.readlines()
    if lines[-1].split(',')[0] == 'True':
        send_mail('all.csv', 'off-to-on.csv', 'waiting.csv')
        f = open('waiting.csv', 'w', newline='')
        f.close()
