import requests
import csv
import os
import datetime


def write(filename, row: list):  # Write to csv file
    with open(filename, 'a', newline='') as f:
        csv.writer(f).writerow(row)
        f.close()


def log():
    url = 'https://google.com'
    timeout = 10

    req = None
    try:
        req = requests.get(url, timeout=timeout)
        connection = True
    except (requests.ConnectionError, requests.Timeout) as exception:
        connection = False

    if os.stat('all.csv').st_size != 0:  # Make sure file isn't emtpy
        with open("all.csv") as file:
            lines = file.readlines()
        last_line_status = lines[-1].split(',')[0]
    else:
        last_line_status = connection

    # Handle writing to file
    get_dict = {(True, "False"): "Reconnected", (False, "True"): "Disconnected"}
    x = datetime.datetime.now()
    if (connection, last_line_status) in get_dict:
        status = get_dict.get((connection, last_line_status))
        write('off-to-on.csv', [f'{status}', x.strftime("%d.%b.%Y %H:%M:%S")])
    write('all.csv', [connection, round(req.elapsed.total_seconds() * 1000, 2) if req is not None else None, x.strftime("%d.%b.%Y %H:%M:%S")])


if __name__ == '__main__':
    log()
