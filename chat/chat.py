from flask import Blueprint


chat = Blueprint("chat", __name__)



    

@chat.route("/getmessge")
def getmessge():
    return "this your messaage"