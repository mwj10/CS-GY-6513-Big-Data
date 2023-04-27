from flask import Flask
import requests
from collections import defaultdict
from util import *
from pymongo import MongoClient
import datetime
import http.client
import urllib.parse
import yfinance as yf
import os
from dotenv import load_dotenv

# Load your API key from an environment variable or secret management service
load_dotenv()

secretNYT = os.environ.get('NYT_KEY')
secretMediaStack = os.environ.get('MEDIA_STACK_KEY')

KEY = secretNYT
client = MongoClient('mongodb://localhost:27019')
db = client.test_db
collection = db.test

app = Flask(__name__)
search_terms = [
    "Apple", "Amgen", "American Express", "Boeing", "Caterpillar",
    "Salesforce",	"Cisco Systems", "Chevron",	"Walt Disney",
    "Dow ",	"Goldman Sachs Group", "Home Depot",
    "Honeywell International",	"IBM",
    "Intel", "Johnson & Johnson", "JP Morgan", "Coca-Cola",
    "McDonalds", "3M Company", "Merck & Company",
    "Microsoft", "Nike", "Procter & Gamble", "The Travelers",	"United Health Group", "Visa ",
    "Verizon Communications",	"Walgreens", "Walmart "
]
ticker_search = [
    "AAPL",	"AMGN",	"AXP",	"BA",	"CAT",	"CRM",	"CSCO",	"CVX",	"DIS",	"DOW",	"GS",	"HD",	"HON",	"IBM",	"INTC",	"JNJ",	"JPM",	"KO",	"MCD",	"MMM",	"MRK",	"MSFT",	"NKE",	"PG",	"TRV",	"UNH",	"V",	"VZ",	"WBA",	"WMT"
]
ticker_company_dict = {}
for i in range(len(search_terms)):
    ticker_company_dict[ticker_search[i]] = search_terms[i]


@app.route("/")
def extract_nyt():
    """
    This endpoint is particularly to query the over Stock market news from NYT
    For this, what we'll do is for every news, if there is an entity within our Dow30, we'll also send that
    news to the Companies collection. Otherwise we only send data to Stock Market collections
    """
    end = (datetime.datetime.today()) - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=2)
    start, end = start.strftime('%Y%m%d'), end.strftime('%Y%m%d')
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
            'date': date, 'news': newsNER[0], 'entities': newsNER[1], 'search_term': search_term, 'source': 'nyt'}
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
    end = (datetime.datetime.today()) - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=2)
    start, end = start.strftime('%Y%m%d'), end.strftime('%Y%m%d')

    collection = db.test

    for search_term in search_terms:

        query = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={search_term}&begin_date={start}&end_date={end}&page=0&api-key={KEY}"
        res = requests.get(query)
        response = res.json()

        stock_market_data = []
        print(search_term)
        if 'response' in response.keys():
            for doc in response['response']['docs']:
                date = formatDate(doc['pub_date'])
                newsNER = extractFromNews(doc['lead_paragraph'])
                news_data = {
                    'date': date, 'news': newsNER[0], 'entities': newsNER[1], 'search_term': search_term, 'source': 'nyt'}
                stock_market_data.append(news_data)
            try:
                collection.insert_many(list(stock_market_data))
                print("success")
            except:
                print("error")

    return {
        "message": "success"
    }


@app.route("/mediastack-gen")
def mediastackGeneral():
    end = (datetime.datetime.today()) - datetime.timedelta(days=0)
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
            'date': formatDate(news['published_at']),
            'news': newsNER[0], 'entities': newsNER[1],
            'search_term': 'Stock Market', 'source': 'mediastack'
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
                'search_term': ticker_company_dict[ticker], 'source': 'yfinance'
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


@app.route("/test")
def test():
    return {
        'test': 'test'
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
