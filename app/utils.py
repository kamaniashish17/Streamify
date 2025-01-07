from pymongo import MongoClient
import requests
from bson.binary import Binary

MONGO_URI = "mongodb://ec2-3-89-250-161.compute-1.amazonaws.com:28081"
DB_NAME = "streamify"
COLLECTION_NAME = "music"

def connect_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection


def upload_audio_file(request):

    document = {
        "audioData" : request.FILES["audioData"].read(),
        "coverImage" : request.FILES["coverImage"].read(),
        "trackName" : request.POST["trackName"],
        "artistName" : request.POST["artistName"],
        "genreName" : request.POST["genreName"],
        "albumName" : request.POST["albumName"],
        "country" : request.POST["country"],
        "releaseDate" : request.POST["releaseDate"],
    }
    
    collection = connect_mongodb()
    result = collection.insert_one(document)
    print(f"Track uploaded successfully. Document ID: {result.inserted_id}")


def get_search_results(search_text):
    collection = connect_mongodb()

    query = {
    "$or": [
        {"artistName": search_text},
        {"genreName": search_text}
    ]
}
    results = list(collection.find(query).limit(18))

    return results
