import datetime
import smtplib
import ssl
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from log import write
from config import sending_email, sending_email_password, receiving_email, smtp_server, smtp_port


def send_mail(*files, to_mail=receiving_email, subject=f"Log files {datetime.datetime.now().strftime('%d.%b.%Y %H:%M:%S')}"):
    body = 'Log files from Raspberry Pi'
    msg = MIMEMultipart()
    msg['from'] = sending_email
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

    server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
    server.ehlo()
    server.login(sending_email, sending_email_password)
    server.send_message(msg, from_addr=sending_email, to_addrs=[to_mail])


if __name__ == '__main__':
    try:
        send_mail('all.csv', 'off-to-on.csv')
    except Exception as e:
        write('waiting.csv', [True, e])
