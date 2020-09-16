from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, make_response
import json
from twilio.rest import Client
import os
from dotenv import load_dotenv
from model import load_model

load_dotenv()


app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
twilio_api = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def fetch_sms():
    return twilio_api.messages.stream()

@app.route("/")
def index():
    spam_or_not = [1, 0]
    sms = [{"body":"d ajadnlanldknaldklakdlakmdlakd"}, {"body": "loreaadkajdkakankdnakjdnkajndkd not spam"}]
    # sms = fetch_sms()
    # print(next(sms))
    # model =load_model()
    spam_msg = []
    not_spam_msg = []

    for i, message in enumerate(sms):
        if spam_or_not[i] == 1:
            spam_msg.append(message)
        else:
            not_spam_msg.append(message)

    # spam_or_not.append(model.predict(message))

    template = render_template('index.html', spam_msg=spam_msg, not_spam_msg=not_spam_msg)
    response = make_response(template)
    # response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response





# @app.route("/about")
# def about():
#     return render_template('about.html')


# @app.route("/scrap",  methods=['POST'])
# def scraptweets():
#     options = {}
#     if request.method == "POST":
#         req = request.form
#         print(req)
#         for val in req:
#             print(req[val])
#             if req[val] != "":
#                 options[val] = req[val]
#     # print(options)
#     download_path = scrap(options)
#     return render_template('success.html', path=download_path)


# app.secret_key = "nlhkjtgjhfhvhjfyfgcjgdtdgcngcghdt"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)