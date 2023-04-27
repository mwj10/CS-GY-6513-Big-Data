import requests
import datetime
from pymongo import MongoClient


def main():
    # lets start with the extractionDB
    # or MongoClient("localhost:27")
    client = MongoClient('mongodb://localhost:27019')
    db = client.test_db
    # db.list_collection_names()  # this should be empty

    # drop collection if previous cell wasn't empty
    for collection in db.list_collection_names():
        db[collection].drop()

    # lets now repeat for sentimentDB
    # or MongoClient("localhost:27")
    client = MongoClient('mongodb://localhost:27018')
    db = client.test_db
    # db.list_collection_names()  # this should be empty

    # drop collection if previous cell wasn't empty
    for collection in db.list_collection_names():
        db[collection].drop()
    # db.list_collection_names()  # this should be empty

    endpoints = [
        '/',
        '/nyt',
        '/mediastack-gen',
        '/yfinance'
    ]

    for endpt in endpoints:
        url = f"http://localhost:8001"+endpt
        response = requests.get(url)
        print(f"{endpt} - {response.json()}")

    # make sure the sentiment-analysis flask app is listening on port 8002
    url = 'http://localhost:8002/transform'

    response = requests.get(url)

    print(response.json())

    # call endpoint to run sentiment
    # make sure the extraction flask app is listening on port 8001
    url = 'http://localhost:8002/sentiment'

    response = requests.get(url)

    print(response.json())

    # Test access data
    # connect to sentiment db
    client = MongoClient('mongodb://localhost:27018')
    db = client.test_db
    collection = db.test
    for doc in collection.find():
        print(doc)


if __name__ == "__main__":
    main()
