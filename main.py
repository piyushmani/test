from flask import Flask, render_template, request , jsonify
import cryptocompare
import datetime

cryptocompare.cryptocompare._set_api_key_parameter('********************')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html', the_title='Home')

def get_year_data(count):

    btc_price = cryptocompare.get_historical_price_day('BTC', currency='USD',limit=365)
    eth_price = cryptocompare.get_historical_price_day('ETH', currency='USD',limit=365)
    return btc_price , eth_price

def get_month_data(count):

    btc_price = cryptocompare.get_historical_price_day('BTC', currency='USD',limit=31)
    eth_price = cryptocompare.get_historical_price_day('ETH', currency='USD',limit=31)
    return btc_price , eth_price


def get_week_data(count):
    limit = count*7
    btc_price = cryptocompare.get_historical_price_day('BTC', currency='USD',limit=limit)
    eth_price = cryptocompare.get_historical_price_day('ETH', currency='USD',limit=limit)
    return btc_price , eth_price

def get_day_data(count):
    limit = count*24
    btc_price = cryptocompare.get_historical_price_hour('BTC', currency='USD',limit=24)
    eth_price = cryptocompare.get_historical_price_hour('ETH', currency='USD',limit=24)
    return btc_price , eth_price


def get_hour_data(count):
    btc_price =[]
    eth_price = []
    last_ts = datetime.datetime.now()
    for i in range(int(count)):
        btc_price.extend(cryptocompare.get_historical_price_minute('BTC', currency='USD',limit=60,toTs=last_ts)) 
        eth_price.extend(cryptocompare.get_historical_price_minute('ETH', currency='USD',limit=60,toTs=last_ts))
        last_ts = btc_price[1]['time']

    return btc_price , eth_price    


@app.route('/data')
def data():

    data_options={
        'Y':get_year_data,
        'M':get_month_data,
        'W':get_year_data,
        'D':get_day_data,
        'H':get_hour_data,
    }

    param = request.args.get('param')
    value = param[0]
    type = param[1]
    
    btc_price , eth_price = data_options[type](value)
    # import pdb;pdb.set_trace()
    jsonResponse = {}
    jsonResponse['btc_price'] =btc_price
    jsonResponse['eth_price'] =eth_price

    return jsonify(jsonResponse)

    
    return "HII"


if __name__ == '__main__':
    app.run(debug=True)
