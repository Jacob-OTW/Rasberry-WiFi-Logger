import requests
import csv
import datetime
import os


def write(filename, row: list):
    with open(filename, 'a', newline='') as f:
        csv.writer(f).writerow(row)


def log():
    try:
        req = requests.get('https://google.com', timeout=10)
        connection = True
    except (requests.ConnectionError, requests.Timeout):
        req = None
        connection = False

    try:
        with open("all.csv") as file:
            for last_item in csv.DictReader(file):
                pass
        last_line_status = {"True": True, "False": False}.get(last_item.get("status"))
    except UnboundLocalError:
        last_line_status = connection

    get_dict = {(True, False): "Reconnected", (False, True): "Disconnected"}
    x = datetime.datetime.now()
    if connection is True:
        out = os.popen(r"/usr/sbin/iwconfig wlan0 | sed -n 's/.*Access Point: \([0-9\:A-F]\{17\}\).*/\1/p'")
        ap = out.read().replace('\n', '')
    else:
        with open("all.csv") as file:
            for line in csv.DictReader(file):
                pass
            try:
                ap = line.get("ap")
            except UnboundLocalError:
                ap = None
    if (connection, last_line_status) in get_dict:
        status = get_dict.get((connection, last_line_status))

        write('off-to-on.csv', [f'{status}', x.strftime("%d.%b.%Y %H:%M:%S"), ap])
    write('all.csv', [connection, round(req.elapsed.total_seconds() * 1000, 2) if req is not None else None,
                      x.strftime("%d.%b.%Y %H:%M:%S"), ap])


if __name__ == '__main__':
    log()
