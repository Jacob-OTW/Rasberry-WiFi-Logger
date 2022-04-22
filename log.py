import requests
import csv
import os
import datetime


def write(filename, row: list):  # Write to csv file
    f = open(filename, 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()


def log():
    # Ping google and store result as boolean
    url = 'https://google.com'
    timeout = 10

    try:
        requests.get(url, timeout=timeout)
        connection = True
    except (requests.ConnectionError, requests.Timeout) as exception:
        connection = False

    # Make sure file isn't emtpy
    if os.stat('all.csv').st_size != 0:
        with open("all.csv") as file:
            lines = file.readlines()
        last_line_status = lines[-1].split(',')[0]
    else:
        last_line_status = connection

    # Handle writing to file
    if connection:  # The ping worked
        x = datetime.datetime.now()
        if last_line_status == 'False':  # If last ping didn't work
            write('off-to-on.csv', ['Reconnected: ', x.strftime("%d.%b.%Y %H:%M:%S")])
        write('all.csv', [connection, x.strftime("%d.%b.%Y %H:%M:%S")])
    else:  # The ping didn't work
        x = datetime.datetime.now()
        if last_line_status == 'True':  # If last ping worked
            write('off-to-on.csv', ['disconnected: ', x.strftime("%d.%b.%Y %H:%M:%S")])
        write('all.csv', [connection, x.strftime("%d.%b.%Y %H:%M:%S")])


if __name__ == '__main__':
    log()
