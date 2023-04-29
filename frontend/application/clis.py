from application import app
from application.models import Usa_stock
from requests_html import HTMLSession
import datetime


@app.cli.command('db_reset')
def db_drop():
    Usa_stock.objects.delete()
    print('Reset database complete.')


@app.cli.command('db_seed')
def db_seed():
    # URL = "https://quotes.ino.com/exchanges/exchange.html?e=DOW"
    # session = HTMLSession()
    # request = session.get(URL)
    # print(request)
    # request = request.html.find("table > tr", first=False)
    # print(request)
    # requests = []
    # for req in request:
    #     if req.find("a", first=True) != None:
    #         requests.append(req.find("a", first=False))

    # symbol_dict = {}
    # symbol_array = []
    # for i, reqs in enumerate(requests, 1):
    #     symbol_dict = {'ref_id': i, 'short': '', 'name': ''}
    #     for c, req in enumerate(reqs, 1):
    #         if c % 2 == 0:
    #             symbol_dict['name'] = req.text
    #         else:
    #             symbol_dict['short'] = req.text
    #     symbol_array.append(symbol_dict)

    # print(symbol_array)
    symbol_array = [{'ref_id': 1, 'short': 'AAPL', 'name': 'Apple Inc.'},
                    {'ref_id': 2, 'short': 'AMGN', 'name': 'Amgen Inc.'},
                    {'ref_id': 3, 'short': 'AXP',
                        'name': 'American Express Company'},
                    {'ref_id': 4, 'short': 'BA',
                        'name': 'Boeing Company (The)'},
                    {'ref_id': 5, 'short': 'CAT', 'name': 'Caterpillar, Inc.'},
                    {'ref_id': 6, 'short': 'CRM', 'name': 'Salesforce, Inc.'},
                    {'ref_id': 7, 'short': 'CSCO', 'name': 'Cisco Systems, Inc.'},
                    {'ref_id': 8, 'short': 'CVX', 'name': 'Chevron Corporation'},
                    {'ref_id': 9, 'short': 'DIS',
                        'name': 'Walt Disney Company (The)'},
                    {'ref_id': 10, 'short': 'DOW', 'name': 'Dow Inc.'},
                    {'ref_id': 11, 'short': 'GS',
                     'name': 'Goldman Sachs Group, Inc. (The)'},
                    {'ref_id': 12, 'short': 'HD',
                        'name': 'Home Depot, Inc. (The)'},
                    {'ref_id': 13, 'short': 'HON',
                        'name': 'Honeywell International Inc.'},
                    {'ref_id': 14,
                     'short': 'IBM',
                     'name': 'International Business Machines Corporation'},
                    {'ref_id': 15, 'short': 'INTC', 'name': 'Intel Corporation'},
                    {'ref_id': 16, 'short': 'JNJ', 'name': 'Johnson & Johnson'},
                    {'ref_id': 17, 'short': 'JPM', 'name': 'JP Morgan Chase & Co.'},
                    {'ref_id': 18, 'short': 'KO',
                        'name': 'Coca-Cola Company (The)'},
                    {'ref_id': 19, 'short': 'MCD', 'name': "McDonald's Corp"},
                    {'ref_id': 20, 'short': 'MMM', 'name': '3M Company'},
                    {'ref_id': 21, 'short': 'MRK',
                        'name': 'Merck & Company, Inc. (new)'},
                    {'ref_id': 22, 'short': 'MSFT',
                        'name': 'Microsoft Corporation'},
                    {'ref_id': 23, 'short': 'NKE', 'name': 'Nike, Inc.'},
                    {'ref_id': 24, 'short': 'PG',
                     'name': 'Procter & Gamble Company (The)'},
                    {'ref_id': 25, 'short': 'TRV',
                        'name': 'The Travelers Companies, Inc.'},
                    {'ref_id': 26,
                     'short': 'UNH',
                     'name': 'UnitedHealth Group Incorporated (DE)'},
                    {'ref_id': 27, 'short': 'V', 'name': 'Visa Inc.'},
                    {'ref_id': 28, 'short': 'VZ',
                        'name': 'Verizon Communications Inc.'},
                    {'ref_id': 29, 'short': 'WBA',
                        'name': 'Walgreens Boots Alliance, Inc.'},
                    {'ref_id': 30, 'short': 'WMT', 'name': 'Walmart Inc.'}]

    for item in symbol_array:
        usa_stock = Usa_stock(ref_id=item['ref_id'],
                              short=item['short'],
                              name=item['name'])
        usa_stock.save()

    print("Database seed complete")
