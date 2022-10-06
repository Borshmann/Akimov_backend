from flask import Flask, request
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
from os.path import join, dirname

import json
import os
import article_compiler as art

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
EAMIL_SRV = os.environ.get('EAMIL_SRV')
EMAIL_PORT = os.environ.get('EMAIL_PORT')

HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')

ALLOWED_ORIGINS = ['https://daryvolkhvov.ru', 'http://localhost:3000']

app = Flask(__name__)
CORS(app, origins=ALLOWED_ORIGINS)

app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SERVER'] = EAMIL_SRV
app.config['MAIL_PORT'] = EMAIL_PORT
app.config['MAIL_USERNAME'] = EMAIL
app.config['MAIL_DEFAULT_SENDER'] = EMAIL
app.config['MAIL_PASSWORD'] = PASSWORD

mail = Mail(app)
data = json.load(open('db.json', 'r', encoding='utf8'))


@app.route("/items", methods=["GET"])
def items():
    return data


@app.route("/cart", methods=["POST"])
def cart():
    bill = request.get_json()
    customer_email_adress = art.customer_email(bill)

    try:
        msg = Message("Заказ ДАРЫ ВОЛХВОВ", sender=EMAIL,
                      recipients=[EMAIL])
        msg.body = str(art.article_compiler(bill))
        mail.send(msg)

        msg2 = Message(str(art.customer_name(bill)) + ", благодарим за заказ!",
                       sender=EMAIL, recipients=[customer_email_adress])
        msg2.html = art.customer_compiler(bill)
        mail.send(msg2)

        return {"message": "email send!"}

    except:
        print('not send!')
        return {"message": "email ERROR"}


if __name__ == "__main__":
    from waitress import serve
    serve(app, host=HOST, port=PORT)
