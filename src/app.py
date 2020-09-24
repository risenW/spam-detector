import os
import warnings
warnings.filterwarnings("ignore")

from flask import Flask, render_template, make_response, request
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
from dotenv import load_dotenv
from model import load_model,  process_sms

load_dotenv() ## load environment variables

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
twilio_api = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    spam_msg, not_spam_msg = get_sms_and_predict(0, 5)
    template = render_template('index.html', spam_msg=spam_msg, not_spam_msg=not_spam_msg)
    response = make_response(template)
    return response


def get_sms_and_predict(start, end):
    '''
    Return predictions for the sms between start and end.
    This is efficient for paginations
    '''
    model = load_model() ## load saved model
    sms = list(twilio_api.messages.stream())
    if (end > len(sms)):
        end = len(sms)

    sub_sms = sms[start:end]
    spam_msg = []
    not_spam_msg = []
    for msg in sub_sms:
        txt = msg.body
        txt = process_sms(txt)
        pred = (model.predict(txt) > 0.5).astype("int32").item()

        if pred == 1:
            spam_msg.append(msg)
        else:
            not_spam_msg.append(msg)
    return spam_msg, not_spam_msg



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)




