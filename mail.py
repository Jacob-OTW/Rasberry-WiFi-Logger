import datetime
import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from log import write


def send_mail(*files, subject=f'Log files {datetime.datetime.now().strftime("%d.%b.%Y %H:%M:%S")}'):
    password = ''
    from_mail = ''
    to_mail = ''
    body = 'Leer hier...'

    msg = MIMEMultipart()
    msg['from'] = from_mail
    msg['to'] = to_mail
    msg['subject'] = subject
    body = MIMEText(body, 'plain')
    msg.attach(body)

    for filename in files:
        with open(filename, 'r') as f:
            attachment = MIMEApplication(f.read(), Name=basename(filename))
            attachment['Content-Disposition'] = f'attachment; filename="{basename(filename)}"'

        msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_mail, password)

    server.send_message(msg, from_addr=from_mail, to_addrs=[to_mail])


if __name__ == '__main__':
    try:
        send_mail('all.csv', 'off-to-on.csv')
    except Exception as e:
        write('waiting.csv', [True, e])
