from flask import Blueprint, jsonify, request, json
from db.db import useritems, grid
from models.usermodel import Users
import bcrypt
import os

from bson import ObjectId
register = Blueprint("register" , __name__, url_prefix= "/register")

def checkpassword(password):
    res = password.encode('utf-8')
    print(res)
    hashed = bcrypt.hashpw(res,bcrypt.gensalt())
    print(hashed)
    return hashed
    

@register.route("", methods = ["POST"])
def registerme():
    request_data = request.get_json()
    username = request_data["username"]
    emailid = request_data["emailid"]
    password = request_data['password']
    existinguser = useritems.find_one({"emailid" : emailid})
    if existinguser is None:
        user1 = {
        "username" : username,
        "emailid" : emailid,
        "password" : checkpassword(password= password),
        "posts" : 0,
        "followers" : 0,
        "following" : 0,
        "isOnline" : False
        }
        uniqueid = useritems.insert_one(user1).inserted_id
        print(uniqueid)
        return jsonify(status = "ok", data = True,error = 0 , message= "user created")
    
    return jsonify(status = "notok", data = False,error = 1, message= "user Exist")
    

    
@register.route("registerDP/<string:userid>",methods = ['POST'])
def registerDP(userid):
    if request.method == 'POST':
        f = request.files[userid]
        existinguser = useritems.find_one({"_id" : ObjectId(userid)})
        if existinguser['profile_dp'] is None:
            
            with grid.new_file(filename = f.filename) as fp:
                    fp.write(f)
                    file_id = fp._id
            if grid.find_one(file_id) is not None:
                    user = useritems.find_one({"_id" : ObjectId(userid)})
                    user['profile_dp'] = str(file_id)
                    iditem = useritems.find_and_modify({"_id" : ObjectId(userid)}, {"$set" : user} )
                    return jsonify({'status': 'File saved successfully',"data" : 1}), 200
                    
                
            return json.dumps({'status': 'Error occurred while saving file.'}), 500
        file_id = ObjectId(existinguser['profile_dp'])
        grid.delete(file_id=file_id)
        with grid.new_file(filename = f.filename) as fp:
                    fp.write(f)
                    file_id = fp._id
        if grid.find_one(file_id) is not None:
                    user = useritems.find_one({"_id" : ObjectId(userid)})
                    user['profile_dp'] = str(file_id)
                    iditem = useritems.find_and_modify({"_id" : ObjectId(userid)}, {"$set" : user} )
                    return jsonify({'status': 'File saved successfully', "data" : 1}), 200


        
        