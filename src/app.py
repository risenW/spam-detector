from flask import Flask, render_template, make_response
from twilio.rest import Client
from dotenv import load_dotenv
from model import load_model,  process_sms

import warnings
warnings.filterwarnings("ignore")

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
twilio_api = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

load_dotenv()
model =load_model() ## load saved model


app = Flask(__name__)


def fetch_sms():
    return twilio_api.messages.stream()

sms = fetch_sms() ## get all sms from twilio


@app.route("/")
def index():
    spam_msg = []
    not_spam_msg = []

    for msg in sms:
        txt = msg.body
        txt = process_sms(txt)
        pred = model.predict_classes(txt).item()

        if pred == 1:
            spam_msg.append(msg)
        else:
            not_spam_msg.append(msg)


    template = render_template('index.html', spam_msg=spam_msg, not_spam_msg=not_spam_msg)
    response = make_response(template)
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)