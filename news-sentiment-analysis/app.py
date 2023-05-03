from flask import Flask, request, json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pymongo import MongoClient
import datetime
from collections import defaultdict


app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

today = datetime.datetime.today()
# Retreive 9-days old data
dates = [(today-datetime.timedelta(days=i)).strftime('%m-%d-%Y') for i in range(10)]


@app.route("/")
@app.route("/index")
def index():
    return {"message":"Sentiment Analysis service is running."}

@app.route("/transform")
def transform_data():
    client = MongoClient('news-extract-mongo', 27019)
    # client = MongoClient('mongodb://localhost:27017') #connect to extraction db
    db = client.test_db
    collection = db.test
    #load data from yesterday
    # end = (datetime.datetime.today()) - datetime.timedelta(days=2)
    # between = end - datetime.timedelta(days=1)
    # start = between - datetime.timedelta(days=1)
    
    # dates = [start.strftime('%m-%d-%Y'), between.strftime('%m-%d-%Y'), end.strftime('%m-%d-%Y')]

    results = []
    for dd in dates:
        query = {
            'date': dd
        }
        # print(f"transform {dd}")
        collection = db.test
        data = collection.find(query, {'_id':0})
        data_to_transform = []
        #initialize new collection in extraction db for transformed data
        collection = db.transformedData
        for t in data:
            # print(t)
            """
            There are two kinds of data: 1. Stock Market, 2. Company Specifics
            For stock market data, we take as is. 
            For company specific:
            1. For ones coming in from yfinance, we take as is
            2. For both nyt and mediastack, we will only pick the docs where theres a match between search_term and entities.
                That is because, a lot of what is queried from these two sources may not contain what we are looking for.
            """
            if t['source'] == 'yfinance':
                data_to_transform.append(t)
            else:
                if t['search_term'] in t['entities'] and t['search_term'] != "Stock Market":
                    data_to_transform.append(t)
                elif t['search_term'] == "Stock Market":
                    data_to_transform.append(t)
        try:
            collection.insert_many( list(data_to_transform) )
            # return {
            #     'message': 'Successfully pushed transformed data to mongo'
            # }
            results.append(f"{dd} Successfully pushed transformed data to mongo.'")
        except:
            # return {
            #     'message': 'Error pushing transformed data.'
            # }
            results.append(f"{dd} Error pushing transformed data.'")

    return results

@app.route("/sentiment")
def hello_world():
    client = MongoClient('news-extract-mongo', 27019)
    # client = MongoClient('mongodb://localhost:27017') #connect to extraction db
    db = client.test_db
    collection = db.transformedData
    # end = (datetime.datetime.today()) - datetime.timedelta(days=2)
    # between = end - datetime.timedelta(days=1)
    # start = between - datetime.timedelta(days=1)
    
    # dates = [start.strftime('%m-%d-%Y'), between.strftime('%m-%d-%Y'), end.strftime('%m-%d-%Y')]

    # yesterday = ((datetime.datetime.today()) - datetime.timedelta(days=1)).strftime('%m-%d-%Y')
    results = []
    for dd in dates:
        # print(f"sentiment {dd}")
        query = {
            'date': dd
        }
        test = collection.find(query)
        transformed_data = []
        for t in test:
            transformed_data.append(t)
        
        data  = defaultdict(dict)
        # print(transformed_data)
        for i in range(len(transformed_data)):
            if transformed_data[i]['date'] not in data:
                data[ transformed_data[i]['date'] ] = {}

            if transformed_data[i]['search_term'] not in data[ transformed_data[i]['date'] ]:
                data[ transformed_data[i]['date'] ][ transformed_data[i]['search_term'] ] = {
                    'avg_sentiment': [],
                    'news': []
                }

            inputs = tokenizer(transformed_data[i]['news'], padding = True, truncation = True, return_tensors='pt')
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            positive = predictions[:, 0].tolist()
            negative = predictions[:, 1].tolist()
            neutral = predictions[:, 2].tolist()
            
            sentiment_data = {
                'symbol':transformed_data[i]['symbol'],
                'headline':transformed_data[i]['news'],
                'sentiment': {
                    'positive': positive[0],
                    'negative': negative[0],
                    'neutral': neutral[0] 
                },
                'source': transformed_data[i]['source']
            }
            data[ transformed_data[i]['date'] ][ transformed_data[i]['search_term'] ]['news'].append(sentiment_data)

        #connect and send data to sentiment store db
        client2 = MongoClient('news-sentiment-analysis-mongo', 27018)
        # client2 = MongoClient('mongodb://localhost:27018') 
        db2 = client2.test_db
        collection2 = db2.test
        try:
            collection2.update_one(
                {'date': dd},
                {'$set': {'data': data}},
                upsert=True
            )
            # return {"message":"Data push to sentiment DB- Succeded"}
            results.append(f"{dd} Data push to sentiment DB Succeded'")
        except:
            # return {"message":"Data push to sentiment DB failed"}
            results.append(f"{dd} Data push to sentiment DB failed'")
    return results


if __name__ == '__main__':
    app.run()


"""
inputs = tokenizer(data_to_test, padding = True, truncation = True, return_tensors='pt')
outputs = model(**inputs)
predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

positive = predictions[:, 0].tolist()
negative = predictions[:, 1].tolist()
neutral = predictions[:, 2].tolist()
#df = pd.DataFrame(table, columns = ["Headline", "Positive", "Negative", "Neutral"])
#response = df.to_json(orient='records')[1:-1].replace('},{', '} {')
"""