#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request
from twilio.rest import Client
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


tasks = [
    {
        'id': 1,
        'status': u'oki',
        'done': False
    }
]

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

def send_message(messagebody,phone):
    # put your own credentials here
    account_sid = "AC9d90fe30d7e5179011a893f4b2fa5ea0"
    auth_token = "5e9bf15a81e56c2ae0c74f2c06345033"

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=phone,
        from_="+13073171105",
        body=messagebody
    )
    return client

@app.route('/vhack/api/v1.0/list', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/vhack/api/v1.0/sendMessage', methods=['POST'])
def create_task():
    if not request.json or not 'celphone' in request.json:
        abort(400)
    cliente=send_message(request.json['message'],request.json['celphone'])
    task = {
        'id': tasks[-1]['id'] + 1,
        'status': 'ok',
        'done': True
    }

    tasks.append(task)
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True)


