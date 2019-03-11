import random

from flask import Flask, request
from pymessenger import Bot

from commands import WELCOME_COMMAND, DETAILS, WEBSITE_LINK, HELP_COMMAND
from responses import WELCOME_MESSAGE, HELP_RESPONSE, NOT_IMPLEMENTED_YET, WEBSITE_RESPONSE, ERROR_MESSAGE, SUCCESSFUL_IMAGE_RECOGNITION_RESPONSE, ERROR_IMAGE_RECOGNITION_RESPONSE

app = Flask(__name__)
ACCESS_TOKEN = 'EAAECfzD3f4EBACw3TVuZClCSpZBHZC49qDcSJPIROZBUnI0kwHZCxT1UMXks46l0t7ZA3crmdOZBGX1g2eebD92TWB3joT5RKUyncfZBqR03gFdcrhBQ9pGVNqgRMJlhUin3jXggDUtEvtVZCJy4uU7ijIknu5SkfcQ4waQNAMhJh4AZDZD'
VERIFY_TOKEN = 'SUPER123SAFE_KAPPA'
bot = Bot(ACCESS_TOKEN)


@app.route("/check", methods=['GET'])
def availability_check():
    return "Ok, server is up, and listening!"


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub. ify_token")
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
                        print(message)
                        print(type(message['message'].get('attachments')))
                        print(message['sender'])
                        send_message(recipient_id, SUCCESSFUL_IMAGE_RECOGNITION_RESPONSE)
                    except Exception as e:
                        send_message(recipient_id, ERROR_IMAGE_RECOGNITION_RESPONSE)
    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        print(token_sent)
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run(host='0.0.0.0')