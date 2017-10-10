#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import vk
# import re
from tasks import send_notification
# from datetime import datetime, timedelta
import socket
from config_parser import get_string
from volume import stl_mass
import urllib.request
from os import remove


REMOTE_SERVER = "www.google.com"

token = '<token>'
count = 10  # How many messages must be readed (max - 200)
debug = 0
# maximum_stl_size = 21474836480 # 20MiB
stl_path = '/tmp'
density = 1.05 # g/cm^3


my_timeformat = '%Y.%m.%d_%H:%M:%S'


def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        socket.create_connection((host, 80), 2)
    except Exception:
        return False
    else:
        return True


def save_file(url, filename):
    urllib.request.urlretrieve(url, filename)


def rm_file(filename):
    remove(filename)


def get_unread_messages(api):
    try:
        messages = api.messages.get(count=count)
    except Exception:
        return []
    del messages[0]
    unread_messages_list = list()

    # GET UNREAD LIST
    for i in messages:
        if i['read_state'] == 0:
            unread_messages_list.append(i)

    return unread_messages_list


def return_list_of_uids_and_messages(messages_list):
    ids_list = list()
    mes_list = list()

    for i in messages_list:
        ids_list.append(i['body'])
        mes_list.append(i['uid'])
    return {'uid': ids_list, 'messages': mes_list}


def return_list_of_price_messages(messages_list):
    list_of_price_messages = list()

    for message in messages_list:
        if message['body'] == 'price':
            user_id = message['uid']
            try:
                attachment = message['attachment']
            except Exception:
                message = get_string('strings', 'no_attachments')
                send_notification.delay(user_id, message)
                continue
            else:
                if attachment['type'] == 'doc':
                    doc = attachment['doc']
                    size = doc['size']
                    ext = doc['ext']
                    url = doc['url']
                    title = doc['title']

                    if ext == 'stl':
                        list_of_price_messages.append(message)
                    else:
                        message = get_string('strings', 'no_stl_file')
                        send_notification.delay(user_id, message)
                else:
                    message = get_string('strings', 'unknown_error')
                    send_notification.delay(user_id, message)

    return list_of_price_messages


def main():
    api = vk.API(vk.Session(access_token=token))
    while True:
        list_of_unread_messages = get_unread_messages(api)
        list_of_price_messages = return_list_of_price_messages(list_of_unread_messages)
        for message in list_of_price_messages:
            user_id = message['uid']
            att_url = message['attachment']['doc']['url']
            att_title = message['attachment']['doc']['title']
            file_path = stl_path + '/' + att_title

            save_file(att_url, file_path)

            # try calculate volume and price
            try:
                mass = stl_mass(file_path, density)

            except Exception:
                # Can't get mass of STL
                message = get_string('strings', 'cant_calculate_price')
                send_notification.delay(user_id, message)





        time.sleep(5)

        if debug:
            break


main()
