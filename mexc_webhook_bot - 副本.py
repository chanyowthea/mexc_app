from flask import Flask, request, jsonify
import os

app = Flask(__name__)
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = 'https://api.mexc.com'

import mexc_spot_v3
def place_order(symbol, side, price_,quantity=0.0007, order_type='MARKET'):
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "price": price_,
        "quantity": quantity,
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
        result = place_order(symbol.upper(), action.upper(),price)
        print(f"Order result: {result}", flush=True)
        return jsonify({'status': 'has run', 'response': result})
    except Exception as e:
        print(f"Error: {str(e)}", flush=True)
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    trade = mexc_spot_v3.mexc_trade()
    market = mexc_spot_v3.mexc_market()
    app.run(host='0.0.0.0', port=5000)