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
    URL = "https://quotes.ino.com/exchanges/exchange.html?e=DOW"
    session = HTMLSession()
    request = session.get(URL)
    request = request.html.find("table > tr", first=False)

    requests = []
    for req in request:
        if req.find("a", first=True) != None:
            requests.append(req.find("a", first=False))

    symbol_dict = {}
    symbol_array = []
    for i, reqs in enumerate(requests, 1):
        symbol_dict = {'ref_id': i, 'short': '', 'name': ''}
        for c, req in enumerate(reqs, 1):
            if c%2 == 0:
                symbol_dict['name'] = req.text
            else:
                symbol_dict['short'] = req.text
        symbol_array.append(symbol_dict)

    for item in symbol_array:
        usa_stock = Usa_stock(ref_id=item['ref_id'],
                              short=item['short'],
                              name=item['name'])
        usa_stock.save()
    
    print("Database seed complete")