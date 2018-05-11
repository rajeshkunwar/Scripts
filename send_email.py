#!/usr/local/bin/python3.6

import getpass
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(*args, **kwargs):
        user = getpass.getuser()
        hostname = socket.gethostname()
        sender = user + '@' + hostname
        smtp_server = 'smtp.server.com'

        for k, v in kwargs.items():

                if k == 'subject':
                        subject = v

                if k == 'body':
                        body = v

        for arg in args:
                msg = MIMEMultipart()
                msg.attach(MIMEText(body, 'plain'))
                msg['From'] = sender
                msg['To'] = arg
                msg['Subject'] = subject

                smtpobj = smtplib.SMTP(smtp_server)
                smtpobj.send_message(msg)
