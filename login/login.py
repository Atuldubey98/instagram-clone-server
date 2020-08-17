from flask import Blueprint, request, jsonify, flash
from db.db import useritems
from models.usermodel import Users
import bcrypt
from register.register import checkpassword


login = Blueprint("login", __name__, url_prefix= "/login")

def checkpasswordforCorrectuser(password, userpassword):
    passkey = checkpassword(password= password)
    
    if bcrypt.checkpw(password.encode('utf-8'),passkey):
        return True
    return False

@login.route("", methods = ["POST"])
def loginme():
    
    emailid = request.get_json()["emailid"]
    password = request.get_json()['password']
    existinguser = useritems.find_one({"emailid" : emailid})
    
    
    if existinguser is None:
        return jsonify(status = "notok" , data = False , error = 1 , message = "user doesnot exist")
    
    if checkpasswordforCorrectuser(password= password, userpassword=existinguser['password']):
        print("Authenticated")
        return jsonify(status = "ok" , data = str(existinguser['_id']) , error = 0 , message = "user Authenticated", emailid = existinguser['emailid'])
    return jsonify(status = "notok" , data = False , error = 1 , message = "Password Incorrect")
