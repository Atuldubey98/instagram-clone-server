from db import db
from chat.chat import chat
from login.login import login
from register.register import register
from userdetails.usedetails import userdetails
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import logging
import socket
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)
socketio = SocketIO(app=app, async_mode = "gevent")

app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = "/userprofiles/users"

app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(userdetails)
app.register_blueprint(chat)

hostname = socket.gethostname()
serveradd = socket.gethostbyname(hostname)

logging.basicConfig(level= logging.DEBUG, format= "%(asctime)-15s - %(levelname)s- -%(name)s-%(relativeCreated)s- %(message)s")
logging.basicConfig(level=logging.CRITICAL)


logging.debug("Running on ****{}****".format(serveradd))

@app.errorhandler(404)
def handle_exception(e):
    return jsonify(status = "notok" , error = str(e), message = "notok")

@app.errorhandler(405)
def handle_exception(e):
    return jsonify(status = "notok" , error = str(e), message = "notok")


@app.route("/")
def checkstatusofserver():
    return jsonify(status = "ok" , error = {} , message = "Running on {}".format(serveradd), data = serveradd)

@socketio.on("chatmessage")
def sendMessageItem(message):
    print(message)
    socketio.emit("test3", message)

if __name__ == "__main__":
    
    socketio.run(app= app, debug = True, host= "0.0.0.0", port= 8000)
    