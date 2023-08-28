from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
import urllib.parse

class Database:
    def __init__(self, connection_string, db_name):
        self.client = MongoClient(connection_string)
        self.db = self.client.get_database(db_name)

app = FastAPI()

mongoDbString = "mongodb+srv://<username>:<password>@gdg-app.clsqnrb.mongodb.net/"

# Escape the username and password using urllib.parse.quote_plus
escaped_username = urllib.parse.quote_plus("swoyamsiddharth")
escaped_password = urllib.parse.quote_plus("Somu@261765")
mongoDbString = mongoDbString.replace("<username>", escaped_username).replace("<password>", escaped_password)

database = Database(mongoDbString, "gdg-app")

@app.get("/")
def index():
    return {"backend_status" : "working"}

@app.get("/sites/list")
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
@app.post("/sites/create")
def create(name: str, title: str, link: str):
    collection = database.db["gdg-app"]
    collection.insert_one({"name": name, "title": title, "link": link})
    return {"status": "record added successfully"}

# creating delete request, take input of name, and delete the respective record
@app.delete("/sites/delete")
def delete(name: str):
    collection = database.db["gdg-app"]
    collection.delete_one({"name": name})
    return {"status": "deleted successfully"}

# creating a get request to get the lidt of all notifications in database
@app.get("/notification/list")
def get_notification():
    collection = database.db["notification"]
    data = collection.find()
    
    serialized_data = []
    for item in data:
        serialized_item = {
            "_id": str(item["_id"]),
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "link": item.get("link", ""),
            "number": item.get("number", 0)

        }
        serialized_data.append(serialized_item)
    
    serialized_data.sort(key=lambda x: x["number"], reverse=True)

    return {"data": serialized_data}

# creating post request, take input of title, description, link, all string
@app.post("/notification/create")
def create_notification(name: str, title: str, description: str, link: str, number: int):
    collection = database.db["notification"]
    collection.insert_one({"name":name, "title": title, "description": description, "link": link, "number": number})
    return {"status": "record added successfully"}

# creating delete request, take input of title, and delete the respective record
@app.delete("/notification/delete")
def delete_notification(title: str):
    collection = database.db["notification"]
    collection.delete_one({"title": title})
    return {"status": "deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)