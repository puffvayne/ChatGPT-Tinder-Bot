# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 5/17/23
"""
import requests

LINE_NOTIFY_TOKEN = 'B55Vq8lk9RTaooaZWbaAGzGsRlVj8FOyDQmM51kg3rQ'
DO_NOTIFICATION = True


def send_message_by_line_notify(msg, token=LINE_NOTIFY_TOKEN):
    if not DO_NOTIFICATION:
        return

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    try:
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
        return r.status_code
    except Exception as e:
        msg = f"Failed to send LINE Notifycation, Error: {e}"
        print(msg)


def turn_off_line_notify():
    global DO_NOTIFICATION
    DO_NOTIFICATION = False


def turn_on_line_notify():
    global DO_NOTIFICATION
    DO_NOTIFICATION = True
