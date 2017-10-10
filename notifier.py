#!/bin/python3
# -*- coding: utf-8 -*-

import smtplib

password = "8E4Cg1bp"
server_email = "<email>"

def notify_via_email(email_address, message):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(server_email, password)
    server.sendmail(server_email, email_address, message)
