import pymongo;
from pymongo import  MongoClient
cluster=MongoClient("mongodb+srv://satrajitghosh183:kalopsia@cluster0.7crnq8u.mongodb.net/?retryWrites=true&w=majority")
db=cluster["test"]
collection=db["Face"]
post={"face_id": "",
    "timestamp": "",
    "score": "",
    "bbox": {"x": "", "y": "", "w": "", "h": ""},
    "landmarks": [{"x": "", "y": ""} for i in range(6)],
    "image_path": "",
    "visit_count": 0}
collection.insert_one(post)