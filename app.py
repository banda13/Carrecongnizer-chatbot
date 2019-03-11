import random
import urllib.request
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
                        send_message(recipient_id, CLASSIFICATION_STARTED)
                        attachments = message['message'].get('attachments')
                        if len(attachments) > 1:
                            send_message(recipient_id, TO_MANY_ATTACHMENTS)
                        elif len(attachments < 1):
                            send_message(recipient_id, TO_LITTLE_ATTACHMENTS)
                        else:
                            if attachments[0]['type'] != 'image':
                                send_message(recipient_id, BAD_ATTACHMENT_TYPE)
                            else:
                                img_url = attachments[0]['payload']['url']
                                response = forward_request(recipient_id, img_url)
                                if response is not None:
                                    send_message(recipient_id, SUCCESSFUL_IMAGE_RECOGNITION_RESPONSE)
                                else:
                                    send_message(recipient_id, ERROR_IMAGE_RECOGNITION_RESPONSE)
                    except Exception as e:
                        send_message(recipient_id, ERROR_IMAGE_RECOGNITION_RESPONSE)
    return "Message Processed"


def forward_request(recipient_id, img_url):
    try:
        user_token = cached_users[recipient_id]
    except KeyError:
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
    try:
        img_file = urllib.request.urlretrieve(img_url)
        print("File download succeeded")

        files = {'carpic': img_file}
        headers = {'Authorization': token}

        print("Classification started")
        class_result = requests.post(CLASSIFICATION_FORWARD_ADDRESS, headers=headers, files=files)
        print("Classification ended")
        return class_result.text
    except Exception as e:
        return None

def try_sign_in(userid, userps):
    try:
        body = {
            "first_name": "",
            "last_name": "",
            "email": userid,
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
            "email": userid,
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

# forward_request("asdasd", "data:image/jpeg;base64,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")