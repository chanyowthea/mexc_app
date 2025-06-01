
import os
from time import sleep

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = 'https://api.mexc.com'



import mexc_spot_v3


# import os
# proxy = 'http://127.0.0.1:7890' # 代理设置，此处修改
# os.environ['HTTP_PROXY'] = proxy 
# os.environ['HTTPS_PROXY'] = proxy 
if __name__ == '__main__':
    trade = mexc_spot_v3.mexc_trade()
    market = mexc_spot_v3.mexc_market()

    symbol = 'BTCUSDC'
    params_kline = {
    "symbol": symbol.upper(),
    "interval": "1m",
    "limit": "5",
    }
    quantity = 0.00001

    count = 0
    while True:
        Kline = market.get_kline(params_kline)
        print(f"Kline data: {Kline}", flush=True)
        if count % 2 == 0:
            params = {
                "symbol": symbol,
                "side": "BUY",
                "type": "MARKET",  # Default order type
                "price": float(Kline[-1][4]),  # Use the closing price of the last candle
                "quantity": quantity,
                # 'quoteOrderQty': quoteOrderQty_,
            }
        else:
            params = {
                "symbol": symbol,
                "side": "SELL",
                "type": "MARKET",  # Default order type
                "price": float(Kline[-1][4]),  # Use the closing price of the last candle
                "quantity": quantity,
                # 'quoteOrderQty': quoteOrderQty_,
            }
    
        print(f"place_order params: {params}", flush=True)
        PlaceOrder = trade.post_order(params)
        print(f"Order result: {PlaceOrder}", flush=True)
        sleep(1)
        count += 1


    while False:
        Kline = market.get_kline(params)
        print(f"Kline data: {Kline}", flush=True)
        if not Kline or len(Kline) <= 2:
            print("====Kline data is not sufficient or empty.", flush=True)
            sleep(1)
            continue

        prev_k = Kline[-2]
        prev_k_h = prev_k[2]
        prev_k_l = prev_k[3]
        cur_k_c = Kline[-1][4]

        print('prev_k=',prev_k,prev_k_h, prev_k_l, cur_k_c,flush=True)
        Price = cur_k_c
        order_type = 'MARKET'  # Default order type
        side = None
        if cur_k_c > prev_k_h:
            Price = cur_k_c
            side = 'BUY'
        if cur_k_c < prev_k_l:
            Price = cur_k_c
            side = 'SELL'

        if side is not None:
            quantity = 0.0005
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "price": Price,
                "quantity": quantity,
                # 'quoteOrderQty': quoteOrderQty_,
            }
            print(f"place_order params: {params}", flush=True)
            PlaceOrder = trade.post_order(params)
            print(f"Order result: {PlaceOrder}", flush=True)
        sleep(1)