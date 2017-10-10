from celery import Celery
import vk
import time


token = 'ce22102be4b0b9f00aecc83dbc8d76fda9cd013cb78378d8861a89b6a68fe6635aedd8b28e12fb385029f'


app = Celery('tasks', backend='amqp', broker='amqp://')
api = vk.API(vk.Session(access_token=token))


def return_humanity_time():
    return str(time.strftime('%H:%M:%S'))


@app.task
def send_notification(user_id, mess):
    try:
        api.messages.send(user_id=user_id, message=mess)
        print(return_humanity_time() + ' message sent: ' + mess + ' ids=' + str(user_ids_list))
    except Exception as inst:
        print("can\'t send notification")
