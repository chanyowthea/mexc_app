from flask import Flask, request, jsonify
import time
import hmac
import hashlib
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = 'https://api.mexc.com'

import mexc_spot_v3


# 'MARKET'
def place_order(symbol, side, price_,quantity=0.00001, order_type='MARKET'):
    # quantity = quoteOrderQty_ / price_
    quoteOrderQty_ = quantity * float(price_)
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "price": price_,
        "quantity": quantity,
        # 'quoteOrderQty': quoteOrderQty_,
    }
    print(f"place_order params: {params}", flush=True)
    PlaceOrder = trade.post_order(params)
    return PlaceOrder

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"receive {data}",flush=True)
    try:
        action = data['action']
        symbol = data['instrument']
        price = data['price']
        quantity = data['quantity']
        result = place_order(symbol.upper(), action.upper(),price,quantity=quantity)
        print(f"Order result: {result}", flush=True)
        return jsonify({'status': 'has run', 'response': result})
    except Exception as e:
        print(f"Error: {str(e)}", flush=True)
        return jsonify({'status': 'error', 'message': str(e)}), 400



# import os
# proxy = 'http://127.0.0.1:7890' # 代理设置，此处修改
# os.environ['HTTP_PROXY'] = proxy 
# os.environ['HTTPS_PROXY'] = proxy 


if __name__ == '__main__':
    trade = mexc_spot_v3.mexc_trade()
    market = mexc_spot_v3.mexc_market()
    app.run(host='0.0.0.0', port=5000)

    # params = {
    # "symbol": "BTCUSDC",
    # "interval": "1m",
    # "limit": "5",
    # # "startTime": "1705029500000",
    # # "endTime": "1705029599909"
    # }
    # Kline = market.get_kline(params)
    # prev_k = Kline[-2]
    # prev_k_h = prev_k[2]
    # prev_k_l = prev_k[3]
    # cur_k_c = Kline[-1][4]

    # side = 'BUY'
    # # print(Kline)
    # print(prev_k_h, cur_k_c)
    # if side == "BUY":
    #     if cur_k_c > prev_k_h:
    #         order_type = 'MARKET'
    #         Price = cur_k_c
    #     elif cur_k_c < prev_k_l:
    #         order_type = 'MARKET'
    #         Price = cur_k_c

    # market.get_kline({"symbol": "BTCUSDC", "interval": "1m"})
    # print(f"Start web hook for mexc!!!",flush=True)

    # params = {"symbol": "BTCUSDC"}
    # market = mexc_spot_v3.mexc_market()
    # Price = float(market.get_price(params)['price'])
    # print(f"Current Price: {Price}", flush=True)
    # # ret = place_order('BTCUSDC', 'BUY', Price, quantity=0.00001, order_type='LIMIT')
    # ret = place_order('BTCUSDC', 'SELL', Price, quantity=0.00001, order_type='LIMIT')
    # print(f"Initial Order Result: {ret}", flush=True)






    # data = {'action': 'sell', 'instrument': 'BTCUSDC', 'price': '104424.47'}
    # try:
    #     # action, symbol = data['message'].split(',')
    #     action = data['action']
    #     symbol = data['instrument']
    #     price = data['price']
    #     result = place_order(symbol.upper(), action.upper(),price)
    #     print(f"Order result: {result}", flush=True)
    #     # return jsonify({'status': 'has run', 'response': result})
    # except Exception as e:
    #     print(f"Error: {str(e)}", flush=True)
    #     # return jsonify({'status': 'error', 'message': str(e)}), 400