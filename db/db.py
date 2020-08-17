from pymongo import MongoClient
from gridfs import GridFS
connectionstring = "mongodb+srv://atuldubey:08091959@cluster0-isxbl.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = MongoClient(connectionstring)

db = client.finalinsta

useritems = db.users
profile = db.profilephoto
grid = GridFS(db)