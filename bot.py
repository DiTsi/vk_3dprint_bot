#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import vk
import socket
from config_parser import get_string
from volume import stl_mass, stl_volume
import urllib.request
from os import remove
from notifier import notify_via_email
from time import sleep


REMOTE_SERVER = "www.google.com"
EMAIL = '<email>'
TOKEN = '<token>'
MESSAGES_COUNT = 50  # How many messages must be readed (max - 200)
DEBUG = 1
# MAXIMUM_STL_SIZE = 21474836480 # 20MiB
STL_PATH = '/tmp'
DENSITY = 1.05 # g/cm^3
PRICE = 7 # rub/gram


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


def send_notification(vk_api, user_id, message):
    try:
        vk_api.messages.send(user_id=user_id, message=message)
        sleep(0.5)
    except Exception as inst:
        username = get_username(vk_api, user_id, 'nom')
        to_username = get_username(vk_api, user_id, 'gen')
        email_subject = get_string('strings', 'email_vksend_error')
        email_message = 'Проверь сообщение пользователя "' + username + '"'
        full_email_message = 'Subject: {}\n\n{}'.format(email_subject, email_message)
        notify_via_email(EMAIL, full_email_message)
        print("can\'t send notification to " + to_username)


def get_username(vkapi, user_id, name_case):
    user = vkapi.users.get(name_case=name_case, user_ids=[user_id])[0]
    sleep(0.5)
    user_name = user['first_name'] + ' ' + user['last_name']
    return user_name


def get_unread_messages(api):
    try:
        messages = api.messages.get(count=MESSAGES_COUNT)
        sleep(0.5)
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


def return_list_of_price_messages(vkapi, messages_list):
    list_of_price_messages = list()

    for message in messages_list:
        if message['body'] == 'price':
            user_id = message['uid']
            try:
                attachment = message['attachment']
            except Exception:
                message = get_string('strings', 'no_attachments')
                send_notification(vkapi, user_id, message)
                continue
            else:
                if attachment['type'] == 'doc':
                    doc = attachment['doc']
                    # size = doc['size']
                    ext = doc['ext']
                    # url = doc['url']
                    # title = doc['title']

                    if ext == 'stl':
                        list_of_price_messages.append(message)
                    else:
                        message = get_string('strings', 'no_stl_file')
                        send_notification(vkapi, user_id, message)
                else:
                    message = get_string('strings', 'unknown_error')
                    send_notification(vkapi, user_id, message)
    return list_of_price_messages


def main():
    vkapi = vk.API(vk.Session(access_token=TOKEN))
    sleep(0.5)
    while True:
        list_of_unread_messages = get_unread_messages(vkapi)
        list_of_price_messages = return_list_of_price_messages(vkapi, list_of_unread_messages)
        for message in list_of_price_messages:
            user_id = message['uid']
            att_url = message['attachment']['doc']['url']
            att_title = message['attachment']['doc']['title']
            file_path = STL_PATH + '/' + att_title

            save_file(att_url, file_path)

            # try calculate volume and price
            try:
                volume = stl_volume(file_path)
                mass = stl_mass(volume, DENSITY)
            except Exception:
                # Can't get mass of STL
                user_name = get_username(vkapi, user_id, 'gen')

                mes = get_string('strings', 'cant_calculate_price')
                send_notification(vkapi, user_id, mes)

                email_subject = get_string('strings', 'email_cost_error')
                email_message = 'Проверь сообщение от ' + user_name + '.'
                full_email_message = 'Subject: {}\n\n{}'.format(email_subject, email_message)
                notify_via_email(EMAIL, full_email_message)
            else:
                send_notification(vkapi, user_id, 'масса = ' + str(mass) + 'г.')

        time.sleep(5)

        if DEBUG:
            break


main()
