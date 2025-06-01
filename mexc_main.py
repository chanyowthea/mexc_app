
import json
import os
from time import sleep
import time

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = 'https://api.mexc.com'


# import os
# proxy = 'http://127.0.0.1:7890' # 代理设置，此处修改
# os.environ['HTTP_PROXY'] = proxy 
# os.environ['HTTPS_PROXY'] = proxy 



import mexc_spot_v3



if __name__ == '__main__':
    trade = mexc_spot_v3.mexc_trade()
    market = mexc_spot_v3.mexc_market()

    symbol = 'SUIUSDC'
    params_kline = {
    "symbol": symbol.upper(),
    "interval": "1m",
    "limit": "5",
    }
    quantity_ = 0.4

    # file_name = f'{symbol}_1m_1748764380000.json'
    # json_obj = None
    # with open(file_name, 'r') as f:
    #     json_data = f.read()
    #     json_obj = json.loads(json_data)


    
    # Kline = market.get_kline(params_kline)
    # js = {'data':Kline}
    # with open(file_name, 'w',encoding="utf=8") as f:
    #     content = json.dumps(js)
    #     f.write(content)



    # count = 0
    # while True:
    #     Kline = market.get_kline(params_kline)
    #     print(f"Kline data: {Kline}", flush=True)
    #     if count % 2 == 0:
    #         params = {
    #             "symbol": symbol,
    #             "side": "BUY",
    #             "type": "MARKET",  # Default order type
    #             "price": float(Kline[-1][4]),  # Use the closing price of the last candle
    #             "quantity": quantity,
    #             # 'quoteOrderQty': quoteOrderQty_,
    #         }
    #     else:
    #         params = {
    #             "symbol": symbol,
    #             "side": "SELL",
    #             "type": "MARKET",  # Default order type
    #             "price": float(Kline[-1][4]),  # Use the closing price of the last candle
    #             "quantity": quantity,
    #             # 'quoteOrderQty': quoteOrderQty_,
    #         }
    
    #     print(f"place_order params: {params}", flush=True)
    #     PlaceOrder = trade.post_order(params)
    #     print(f"Order result: {PlaceOrder}", flush=True)
    #     sleep(1)
    #     count += 1

    print("mexc_app start!!!", flush=True)
    # Kline = market.get_kline(params_kline)
    # params = {
    # "symbol": symbol,
    # "side": "SELL",
    # "type": "MARKET",  # Default order type
    # "price": float(Kline[-1][4]),  # Use the closing price of the last candle
    # "quantity": quantity_,
    #     # 'quoteOrderQty': quoteOrderQty_,
    # }
    # print(f"place_order params: {params}", flush=True)
    # PlaceOrder = trade.post_order(params)
    # print(f"Order result: {PlaceOrder}", flush=True)
    # if PlaceOrder is None or 'code' in PlaceOrder:
    #     print(f"====Error placing order: {PlaceOrder}", flush=True)

    has_buy = False
    action_time_stamp = '0'
    action_time_stamp_int = 0
    data_index = 100
    sleep_gap = 5
    while True:
        seconds_local = int(time.time())
        print(action_time_stamp, flush=True)
        # print(f"Current local time in seconds: {seconds_local},{int(int(action_time_stamp)/1000)}", flush=True)
        if seconds_local < action_time_stamp_int+60:
            sleep(sleep_gap)
            print(f"====Action time stamp is the same {seconds_local-action_time_stamp_int}", flush=True)
            continue

        # real_data_index = int(data_index /60)
        # Kline = json_obj['data'][:real_data_index]  # Use the preloaded Kline data
        Kline = market.get_kline(params_kline)
        # print(f"Kline data: {Kline}", flush=True)
        if not Kline or len(Kline) <= 2:
            print("====Kline data is not sufficient or empty.", flush=True)
            sleep(sleep_gap)
            data_index += 1
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
            has_buy_temp = True if side == 'BUY' else False
            ts = Kline[-1][0]  # Use the timestamp of the last candle
            if ts == action_time_stamp:
                # print(f"====Action time stamp is the same, skipping order. Current time: {ts}, Previous time: {action_time_stamp}", flush=True)
                sleep(sleep_gap)
                
                data_index += 1
                continue
            if has_buy_temp == has_buy:
                # print(f"====No change in position, skipping order. Current side: {side}, Previous side: {has_buy}", flush=True)
                sleep(sleep_gap)
                data_index += 1
                continue

            quantity = quantity_
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "price": Price,
                "quantity": quantity,
                # 'quoteOrderQty': quoteOrderQty_,
            }
            
            seconds = Kline[-1][0] / 1000  # Convert milliseconds to seconds
            # dest= time.strftime("%M:%S", time.localtime(seconds))
            dest_long = time.strftime("%H:%M:%S", time.localtime(seconds))


            print(f"{dest_long} {Kline[-1][0]} place_order params: {params}", flush=True)
            PlaceOrder = trade.post_order(params)
            if PlaceOrder is None or 'code' in PlaceOrder:
                print(f"====Error placing order: {PlaceOrder}", flush=True)
                sleep(sleep_gap)
                data_index += 1
                continue
            
            has_buy = has_buy_temp
            action_time_stamp = ts
            action_time_stamp_int = int(int(action_time_stamp)/1000)
            print(f"Order result: {PlaceOrder}", flush=True)
        sleep(sleep_gap)
        data_index += 1
