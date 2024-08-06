from flask import Flask, jsonify, render_template, request
import yfinance as yf
import requests_html
from yahoo_fin import stock_info

app = Flask(__name__)

def get_data(ticker, start_date=None, end_date=None, index_as_date=True, interval="1d"):
    ticker_obj = yf.Ticker(ticker)
    data = ticker_obj.history(start=start_date, end=end_date, interval=interval)
    
    if not index_as_date:
        data.reset_index(inplace=True)
    
    return data

@app.route('/get_data/<ticker>', methods=['GET'])
def get_ticker_data(ticker):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    index_as_date = request.args.get('index_as_date', 'true').lower() in ['true', '1', 't', 'y', 'yes']
    interval = request.args.get('interval', '1d')

    data = get_data(ticker, start_date, end_date, index_as_date, interval)
    return jsonify(data.to_dict(orient='records'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/day_gainers')
def day_gainers():
    gainers = stock_info.get_day_gainers().head(10)
    gainers = gainers[['Symbol', 'Name', 'Price (Intraday)', 'Change', 'Volume']]
    return jsonify(gainers.to_dict(orient='records'))

@app.route('/day_losers')
def day_losers():
    losers = stock_info.get_day_losers().head(10)
    losers = losers[['Symbol', 'Name', 'Price (Intraday)', 'Change', 'Volume']]
    return jsonify(losers.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)