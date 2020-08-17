from flask import Flask, Blueprint, send_file, make_response, jsonify, send_from_directory
from db.db import grid, useritems
from bson import ObjectId


userdetails = Blueprint("userdetails" , __name__,url_prefix="/userdetails")

@userdetails.errorhandler(404)
def notfound(e):
    return json.dumps(str(e))

@userdetails.errorhandler(500)
def notfound(e):
    return json.dumps(str(e))


@userdetails.route("/<string:userid>")
def userdetailofsingleperson(userid):
    print(userid)
    existinguser = useritems.find_one({"_id" : ObjectId(userid)})
    print(existinguser)
    return jsonify(error = 0 , data = {"_id" : userid , "username" : existinguser['username'], "posts" : existinguser['posts'], "followers" : existinguser['followers'] ,"following" : existinguser['following'] }, message = "exist")
    

@userdetails.route("getprofilephoto/<string:userid>")
def getprofilephoto(userid):
    if(userid):
        existinguser = useritems.find_one({"_id" : ObjectId(userid)})
        if(existinguser['profile_dp']):
            imageid = existinguser['profile_dp']
            grid_fs_file = grid.find_one({"_id" : ObjectId(imageid)})
            response = make_response(grid_fs_file.read())
            response.headers['Content-Type'] = "application/octet-stream"
            response.headers['Content-Disposition'] = "attachment;filename = {}.jpeg".format(imageid)
            return response
        return send_from_directory("", "download.png")
    return jsonify(error = 1)


@userdetails.route("getuserdetails/<string:searchquery>")
def getuserdetails(searchquery):
    if(searchquery):
        itemlist = []
        existingusers = useritems.find({"username" : {"$regex" : searchquery}})
        
        if(existingusers):
            for items in existingusers:
                itemtoadd = {"username" : items['username'], "emailid" : items['emailid'], "_id": str(items['_id'])}
                itemlist.append(itemtoadd)
        existingusers = useritems.find({"emailid" : {"$regex" : searchquery}})
        if(existingusers):
            for items in existingusers:
                itemtoadd = {"username" : items['username'], "emailid" : items['emailid'], "_id": str(items['_id'])}
                itemlist.append(itemtoadd)
            return jsonify(error = 1 , data = itemlist, message = "Not Found")

        return jsonify(error = 1 , data = [] , message = "Not found")
    return jsonify(error = 1 , data = [], message = "notfound")
        

