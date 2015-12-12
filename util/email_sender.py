#!/bin/usr/env python
#-*-coding:utf-8-*-

import smtplib
from email.mime.text import MIMEText

def send_email(sender, pwd, receiver, subject, msg, \
    msg_format='plain', smtp_server_port=25):

    msg = MIMEText(msg, msg_format, 'utf-8')
    msg['From'] = '<%s>' % sender
    msg['To'] = '<%s>' % receiver
    msg['Subject'] = subject

    pos = sender.find('@')
    smtp_server = 'smtp.' + sender[pos+1:]
    smtpobj = smtplib.SMTP(smtp_server, smtp_server_port)
    smtpobj.login(sender, pwd)
    smtpobj.sendmail(sender, [receiver], msg.as_string())
