from pymongo import MongoClient
client = MongoClient("mongodb+srv://thelapssql:581ysg2315@cluster0.efos6wv.mongodb.net/Cluster0?retryWrites=true&w=majority")
db = client.musical

user = db.users.find_one({ "name": "bob" }, { "_id": False })
print((user))