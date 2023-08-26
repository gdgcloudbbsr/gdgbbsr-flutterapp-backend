from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
import urllib.parse

class Database:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.get_database("gdg-app")

app = FastAPI()

mongoDbString = "mongodb+srv://<username>:<password>@gdg-app.clsqnrb.mongodb.net/"

# Escape the username and password using urllib.parse.quote_plus
escaped_username = urllib.parse.quote_plus("enter username")
escaped_password = urllib.parse.quote_plus("enter password")
mongoDbString = mongoDbString.replace("<username>", escaped_username).replace("<password>", escaped_password)

database = Database(mongoDbString)

@app.get("/")
def index():
    return {"backend_status" : "working"}

@app.get("/list")
def get_list():
    collection = database.db["gdg-app"]
    data = collection.find()
    
    serialized_data = []
    for item in data:
        serialized_item = {
            "_id": str(item["_id"]),
            "name": item.get("name", ""),
            "title": item.get("title", ""),
            "link": item.get("link", "")
        }
        serialized_data.append(serialized_item)
    
    return {"data": serialized_data}

# creating post request, take input of name, title, link, all string
@app.post("/create")
def create(name: str, title: str, link: str):
    collection = database.db["gdg-app"]
    collection.insert_one({"name": name, "title": title, "link": link})
    return {"status": "record added successfully"}

# creating delete request, take input of name, and delete the respective record
@app.delete("/delete")
def delete(name: str):
    collection = database.db["gdg-app"]
    collection.delete_one({"name": name})
    return {"status": "deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)