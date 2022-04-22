import requests
import csv
import os
import datetime


def session_for_src_addr(addr: str) -> requests.Session:
    """
    Create `Session` which will bind to the specified local address
    rather than auto-selecting it.
    """
    session = requests.Session()
    for prefix in ('http://', 'https://'):
        session.get_adapter(prefix).init_poolmanager(
            # those are default values from HTTPAdapter's constructor
            connections=requests.adapters.DEFAULT_POOLSIZE,
            maxsize=requests.adapters.DEFAULT_POOLSIZE,
            # This should be a tuple of (address, port). Port 0 means auto-selection.
            source_address=(addr, 0),
        )

    return session


def write(filename, row: list):  # Write to csv file
    f = open(filename, 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()


# Ping google and store result as boolean
url = 'https://google.com'
timeout = 10

try:
    s = session_for_src_addr('192.168.186.95')
    s.get(url, timeout=timeout)
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
