#!/bin/python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

password = <password>
server_email = <email>


def notify_via_email(email_address, subject, message):
    msg = MIMEMultipart('alternative')
    # msg['FROM'] = server_email
    # msg['To'] = email_address
    msg['Subject'] = Header(subject, "utf-8")
    msg.attach(MIMEText(message, _charset="UTF-8"))

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(server_email, password)
    server.sendmail(server_email, email_address, msg.as_string())
    server.quit()


def main():
    notify_via_email(<email>, 'тема', 'сообщение')


if  __name__ ==  "__main__" :
    main()
