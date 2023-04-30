from flask import Flask
import requests
from collections import defaultdict
from util import *
from pymongo import MongoClient
import json
import datetime
import http.client
import urllib.parse
import yfinance as yf
import os
from dotenv import load_dotenv

# Load your API key from an environment variable or secret management service
load_dotenv()

secretNYT = os.getenv('NYT_KEY')
secretMediaStack = os.getenv('MEDIA_STACK_KEY')

KEY = secretNYT
client = MongoClient('news-extract-mongo', 27019)
db = client.test_db
collection = db.test

app = Flask(__name__)
search_terms = [
    "Apple", "Amgen", "American Express", "Boeing", "Caterpillar",
    "Salesforce",	"Cisco Systems", "Chevron",	"Walt Disney",
    "Dow",	"Goldman Sachs Group", "Home Depot",
    "Honeywell International",	"IBM",
    "Intel", "Johnson & Johnson", "JP Morgan", "Coca-Cola",
    "McDonalds", "3M Company", "Merck & Company",
    "Microsoft", "Nike", "Procter & Gamble", "The Travelers",	"United Health Group", "Visa",
    "Verizon Communications",	"Walgreens", "Walmart"
]
ticker_search = [
    "AAPL",	"AMGN",	"AXP",	"BA",	"CAT",	"CRM",	"CSCO",	"CVX",	"DIS",	"DOW",	"GS",	"HD",	"HON",	"IBM",	"INTC",	"JNJ",	"JPM",	"KO",	"MCD",	"MMM",	"MRK",	"MSFT",	"NKE",	"PG",	"TRV",	"UNH",	"V",	"VZ",	"WBA",	"WMT"
]
ticker_to_company = {}
company_to_ticker = {}
for i in range(len(search_terms)):
    ticker_to_company[ticker_search[i]] = search_terms[i]
    company_to_ticker[search_terms[i]] = ticker_search[i]

@app.route("/")
def index():
    return { 'result': "News extracting service is running."} 


@app.route("/extract")
def extract_nyt():
    """
    This endpoint is particularly to query the over Stock market news from NYT
    For this, what we'll do is for every news, if there is an entity within our Dow30, we'll also send that
    news to the Companies collection. Otherwise we only send data to Stock Market collections
    """
    
    end = (datetime.datetime.today()) - datetime.timedelta(days=2)
    start = end - datetime.timedelta(days=2)
    start, end = start.strftime('%Y%m%d'), end.strftime('%Y%m%d')
    # print(start, end)
    search_term = "Stock Market"
    query = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={search_term}&begin_date={start}&end_date={end}&page=0&api-key={KEY}"
    res = requests.get(query)
    response = res.json()
    msg = defaultdict(dict)
    stock_market_data = []

    for doc in response['response']['docs']:
        date = formatDate(doc['pub_date'])
        newsNER = extractFromNews(doc['lead_paragraph'])
        news_data = {
            # 'ticker': company_to_ticker[newsNER[1]],
            'date': date, 'news': newsNER[0], 'entities': newsNER[1], 'search_term': search_term, 'source': 'nyt', 'symbol':''}
        stock_market_data.append(news_data)
    try:
        collection.insert_many(list(stock_market_data))
        return {
            'message': 'Successfully pushed data to mongo'
        }
    except:
        return {
            'message': 'Error pushing data.'
        }


@app.route("/nyt")
def extract_nyt_main():
    """
    This endpoint is particularly to query the over Stock market news from NYT
    For this, what we'll do is for every news, if there is an entity within our Dow30, we'll also send that
    news to the Companies collection. Otherwise we only send data to Stock Market collections
    """
    end = (datetime.datetime.today()) - datetime.timedelta(days=2)
    start = end - datetime.timedelta(days=2)
    start, end = start.strftime('%Y%m%d'), end.strftime('%Y%m%d')

    collection = db.test

    for search_term in search_terms:

        query = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={search_term}&begin_date={start}&end_date={end}&page=0&api-key={KEY}"
        res = requests.get(query)
        response = res.json()

        stock_market_data = []
        if 'response' in response.keys():
            print(search_term)
            for doc in response['response']['docs']:
                date = formatDate(doc['pub_date'])
                newsNER = extractFromNews(doc['lead_paragraph'])
                news_data = {
                    'date': date, 'news': newsNER[0], 'entities': newsNER[1], 'search_term': search_term, 'source': 'nyt', 'symbol':company_to_ticker[search_term]}
                
                stock_market_data.append(news_data)
                # print(stock_market_data)

            try:
                collection.insert_many(list(stock_market_data))
                print("success")
            except:
                pass
                print("error (nothing to insert)")

    return {
        "message": "success"
    }


@app.route("/mediastack-gen")
def mediastackGeneral():
    end = (datetime.datetime.today()) - datetime.timedelta(days=2)
    start = end - datetime.timedelta(days=2)
    start_end = f"{start.strftime('%Y-%m-%d')},{end.strftime('%Y-%m-%d')}"
    params = urllib.parse.urlencode({
        'access_key': secretMediaStack,
        'keyword': 'Stock Market',
        'sort': 'published_desc',
        'countries': 'us',
        'categories': 'business',
        'date': start_end,
        'limit': 100,
    })
    query = f"http://api.mediastack.com/v1/news?{params}"
    res = requests.get(query)
    response = res.json()
    stock_market_data = []
    for news in response['data']:
        #news_data['date'] = news['published_at'].strftime('%m-%d-%Y')
        newsNER = extractFromNews(news['title'])

        news_data = {
            # 'ticker': company_to_ticker[newsNER[1]],
            'date': formatDate(news['published_at']),
            'news': newsNER[0], 'entities': newsNER[1],
            'search_term': 'Stock Market', 'source': 'mediastack', 'symbol':'',
        }
        # print(news_data)
        stock_market_data.append(news_data)
        
    try:
        collection.insert_many(list(stock_market_data))
        return {
            'message': 'Successfully pushed data to mongo'
        }
    except:
        return {
            'message': 'Error pushing data.'
        }


@app.route("/yfinance")
def extract_yfinance():
    stock_market_data = []
    for ticker in ticker_search:
        t = yf.Ticker(ticker)
        for news in t.news:
            newsNER = extractFromNews(news['title'])
            news_data = {
                'date': datetime.datetime.fromtimestamp(news['providerPublishTime']).strftime("%m-%d-%Y"),
                'news': newsNER[0], 'entities': newsNER[1],
                'search_term': ticker_to_company[ticker], 'source': 'yfinance', 'symbol': ticker
            }
        stock_market_data.append(news_data)
    try:
        collection.insert_many(list(stock_market_data))
        return {
            'message': 'Successfully pushed data to mongo'
        }
    except:
        return {
            'message': 'Error pushing data.'
        }

@app.route("/getnews")
@app.route("/getnews/")
@app.route("/getnews/<string:q_ticker>")
def getnews(q_ticker=None):

    today = datetime.datetime.today()
    # Retreive 9-days old data
    dates = [(today-datetime.timedelta(days=i)).strftime('%m-%d-%Y') for i in range(10)]

    client = MongoClient('news-sentiment-analysis-mongo', 27018) #connect to sentiment db
    db = client.test_db
    collection = db.test
    cursor = collection.find({'date': { '$in': dates }}).sort("date", -1)
    json_collection_arr = []
    json_collection_dict = {}
    for row in cursor:
        print(row)
        for key, val in row['data'].items():
            # json_result[key] = val
            # print(key)
            for k, v in val.items():
                
                # for k, v in item.items():
                #     print(v)
                for item in v['news']:
                    json_collection_dict["date"] = key
                    json_collection_dict["stock"] = k
                    for kk, vv in item.items():
                        
                        json_collection_dict[kk] = vv
                    # print(item)
                
                    json_collection_arr.append(json_collection_dict)
                    json_collection_dict = {}
            # print(val)
        # 
    # print(json_collection_arr)

    json_result_arr = []
    if q_ticker is not None:
        if str(q_ticker).lower() == 'all':
            json_result_arr = json_collection_arr
        else:
            for col in json_collection_arr:
                if str(q_ticker).lower() == str(col['symbol']).lower():
                    json_result_arr.append(col)
    else:
        for col in json_collection_arr:
            if col['symbol'] == "":
                json_result_arr.append(col)
    # for item in json_collection_arr:
    #     print(item)
    
    return json_result_arr


@app.route("/test")
def test():
    return {
        'test': 'test'
    }

@app.cli.command('db_seed')
@app.route("/seed")
def seed():

    # lets start with the extractionDB
    client = MongoClient('news-extract-mongo', 27019)
    db = client.test_db
    
    end = (datetime.datetime.today()) - datetime.timedelta(days=2)
    between = end - datetime.timedelta(days=1)
    start = between - datetime.timedelta(days=1)
    
    dates = [start.strftime('%m-%d-%Y'), between.strftime('%m-%d-%Y'), end.strftime('%m-%d-%Y')]
    collection = db.test
    for dd in dates:
        collection.delete_many({'date': dd})
    collection = db.transformedData
    for dd in dates:
        collection.delete_many({'date': dd})

    endpoints = [
        '/extract',
        '/nyt',
        '/mediastack-gen',
        '/yfinance'
    ]

    for endpt in endpoints:
        url = f"http://news-extract-flask:8001"+endpt
        response = requests.get(url)
        print(f"{endpt} - {response.json()}")


    client2 = MongoClient('news-sentiment-analysis-mongo', 27018)
    db2 = client2.test_db
    collection2 = db2.test
    for dd in dates:
        collection2.delete_many({'date': dd})

    # make sure the sentiment-analysis flask app is listening on port 8002
    url = 'http://news-sentiment-analysis-flask:8002/transform'

    response = requests.get(url)

    print(response)

    # call endpoint to run sentiment
    # make sure the extraction flask app is listening on port 8001
    url = 'http://news-sentiment-analysis-flask:8002/sentiment'

    response = requests.get(url)

    print(response)

    # Test access data
    # connect to sentiment db
    
    client2 = MongoClient('news-sentiment-analysis-mongo', 27018)
    db = client2.test_db
    collection = db.test
    for doc in collection.find():
        print(doc)

    return {
        'message': 'News database has been seeded'
    }

if __name__ == "__main__":
    app.run()
