import os
import time
import requests
import json
from flask import Flask, request
from pymessenger import Bot

from commands import WELCOME_COMMAND, DETAILS, WEBSITE_LINK, HELP_COMMAND
from responses import WELCOME_MESSAGE, HELP_RESPONSE, NOT_IMPLEMENTED_YET, WEBSITE_RESPONSE, ERROR_MESSAGE,\
    SUCCESSFUL_IMAGE_RECOGNITION_RESPONSE, ERROR_IMAGE_RECOGNITION_RESPONSE, CLASSIFICATION_STARTED, AUTHENTICATION_ERROR, TO_MANY_ATTACHMENTS, TO_LITTLE_ATTACHMENTS, UNKNOWN_CLASSIFICATION_ERROR, BAD_ATTACHMENT_TYPE
from system_properties import LOGIN_ADDRESS, SIGN_IN_ADDRESS, CLASSIFICATION_FORWARD_ADDRESS

app = Flask(__name__)
ACCESS_TOKEN = 'EAAECfzD3f4EBACw3TVuZClCSpZBHZC49qDcSJPIROZBUnI0kwHZCxT1UMXks46l0t7ZA3crmdOZBGX1g2eebD92TWB3joT5RKUyncfZBqR03gFdcrhBQ9pGVNqgRMJlhUin3jXggDUtEvtVZCJy4uU7ijIknu5SkfcQ4waQNAMhJh4AZDZD'
VERIFY_TOKEN = 'SUPER123SAFE_KAPPA'
bot = Bot(ACCESS_TOKEN)

cached_users = {}

@app.route("/check", methods=['GET'])
def availability_check():
    return "Ok, server is up, and listening!"


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    else:
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    msg = message['message'].get('text').strip().lower()
                    if msg == WELCOME_COMMAND:
                        send_message(recipient_id, WELCOME_MESSAGE % message['sender'])
                    if msg == HELP_COMMAND:
                        send_message(recipient_id, HELP_RESPONSE)
                    if msg == DETAILS:
                        send_message(recipient_id, NOT_IMPLEMENTED_YET)
                    if msg == WEBSITE_LINK:
                        send_message(recipient_id, WEBSITE_RESPONSE)
                    else:
                        send_message(recipient_id, ERROR_MESSAGE)
                if message['message'].get('attachments'):
                    try:
                        print("Hmm I got an image")
                        send_message(recipient_id, CLASSIFICATION_STARTED)
                        attachments = message['message'].get('attachments')
                        print(attachments)
                        if len(attachments) > 1:
                            send_message(recipient_id, TO_MANY_ATTACHMENTS)
                        elif len(attachments) < 1:
                            send_message(recipient_id, TO_LITTLE_ATTACHMENTS)
                        else:
                            print("ok length is ok")
                            attachment = attachments[0]
                            if attachment['type'] != 'image':
                                send_message(recipient_id, BAD_ATTACHMENT_TYPE)
                            else:
                                print("ok type is ok!")
                                print(attachment)
                                img_url = attachment['payload']['url']
                                print("Classification started for image %s" % str(img_url))
                                response = forward_request(recipient_id, img_url)
                                if response is not None:
                                    send_message(recipient_id, response)
                                else:
                                    send_message(recipient_id, ERROR_IMAGE_RECOGNITION_RESPONSE)
                    except Exception as e:
                        print(str(e))
                        send_message(recipient_id, ERROR_IMAGE_RECOGNITION_RESPONSE)
    return "Message Processed"


def forward_request(recipient_id, img_url):
    try:
        user_token = cached_users[recipient_id]
        print("User token found in cache")
    except KeyError:
        print("User token not found")
        user_token = None
    if user_token is None:
        signin_result = try_sign_in(recipient_id, recipient_id)
        token = login(recipient_id, recipient_id)
        if token is not None:
            classification_result = do_classification(token, img_url)
            return classification_result
        else:
            return None
    else:
        classification_result = do_classification(user_token, img_url)
        if classification_result is None:
            token = login(recipient_id, recipient_id)
            if token is not None:
                classification_result = do_classification(token, img_url)
            else:
                return None
        else:
            return classification_result


def do_classification(token, img_url):
    filename = str(time.time()) + 'pic.jpg'
    try:
        r = requests.get(img_url, allow_redirects=True)

        img_file = open(filename, 'wb').write(r.content)
        print("File download succeeded")

        files = {'carpic': img_file}
        headers = {'Authorization': token}

        print("Classification started")
        class_result = requests.post(CLASSIFICATION_FORWARD_ADDRESS, headers=headers, files=files)
        print("Classification ended")
        os.remove(filename)
        print(class_result.text)
        return class_result.text
    except Exception as e:
        print("Classification failed.. %s" % str(e))
        os.remove(filename)
        return None

def try_sign_in(userid, userps):
    try:
        body = {
            "first_name": "",
            "last_name": "",
            "email": userid + "@facebook.hu",
            "password": userps
        }
        print("Trying to sign in as %s" % str(userid))
        signin_result = requests.post(SIGN_IN_ADDRESS, body)
        if signin_result.status_code == 200 | signin_result.status_code == 201:
            print("User registration success, welcome %s" % str(userid))
            return True
        else:
            print("User registration failed")
            return False
    except Exception as e:
        print("Sign in failed")
        return None

def login(userid, userps):
    try:
        body = {
            "email": userid + "@facebook.hu",
            "password": userps
        }
        login_result = requests.post(LOGIN_ADDRESS, body)
        token = 'andy ' + json.loads(login_result.text)['token']
        print("Login succeeded, token updated in cache")
        cached_users[userid] = token
        return token
    except Exception as e:
        print("Login in failed")
        return None

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        print("Token verification ok!")
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

