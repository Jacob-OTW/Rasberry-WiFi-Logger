import datetime
import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_mail(*files):
    password = ''
    from_mail = ''
    to_mail = ''
    x = datetime.datetime.now()
    subject = f'Log files {x.strftime("%d.%b.%Y %H:%M:%S")}'
    body = 'Text'

    msg = MIMEMultipart()
    msg['from'] = from_mail
    msg['to'] = to_mail
    msg['subject'] = subject
    body = MIMEText(body, 'plain')
    msg.attach(body)

    for file in files:
        filename = file
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
    send_mail('all.csv', 'off-to-on.csv')
