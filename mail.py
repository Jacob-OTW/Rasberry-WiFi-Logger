import datetime
import smtplib
import ssl
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from log import write


def send_mail(*files, to_mail="<Mail Address>", subject=f"R2 Log files {datetime.datetime.now().strftime('%d.%b.%Y %H:%M:%S')}"):
    password = '<password>'
    from_mail = '<Mail Address>'
    body = 'Log from Raspberry'

    msg = MIMEMultipart()
    msg['from'] = from_mail
    msg['to'] = to_mail
    msg['subject'] = subject
    body = MIMEText(body, 'plain')
    msg.attach(body)

    for filename in files:
        filename: str
        with open(filename, 'r') as f:
            attachment = MIMEApplication(f.read(), Name=basename(filename))
            attachment['Content-Disposition'] = f'attachment; filename="{basename(filename)}"'

        msg.attach(attachment)
        
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL("<URL HERE>", 465, context=context)
    server.ehlo()
    server.login(from_mail, password)
    server.send_message(msg, from_addr=from_mail, to_addrs=[to_mail])


if __name__ == '__main__':
    try:
        send_mail('all.csv', 'off-to-on.csv')
    except Exception as e:
        write('waiting.csv', [True, e])
