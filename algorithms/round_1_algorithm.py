from datamodel import OrderDepth, UserId, TradingState, Order, Trade
from typing import List
import string
import numpy as np
from collections import defaultdict

class Trader:
    def __init__(self):
        self.historical_data = defaultdict(list)
        self.pnl_data = defaultdict(list)
    
    def run(self, state: TradingState):
        result = {}
        
        # KELP, RAINFOREST_RESIN, SQUID_INK
        for product_name in state.order_depths:
            print(product_name)
            order_book: OrderDepth = state.order_depths[product_name]
            orders: List[Order] = []
            
            # If empty position
            try:
                my_position = state.position[product_name]
            except:
                my_position = 0
            
            # BUG: 'KELP' returns keyerror for some reason
            # my_orders = state.own_trades[product_name]
            # other_orders = state.market_trades[product_name]
            
            sell_price, sell_amount = list(order_book.sell_orders.items())[0]
            buy_price, buy_amount = list(order_book.buy_orders.items())[0]
            mid_price = sell_price - buy_price
            print(f'Mid Price: {mid_price}')
            
            if len(self.historical_data[product_name]) > 1:
                daily_pnl = my_position * (mid_price - self.historical_data[product_name][-1])
                print(f'{product_name} daily pnl: {round(daily_pnl, 2)}')
                self.pnl_data[product_name].append(daily_pnl)
                cumm_pnl = sum(self.pnl_data[product_name])
                print(f'{product_name} cumm pnl: {round(cumm_pnl, 2)}')
            
            if product_name == "RAINFOREST_RESIN":
                '''
                Logic for RAINFOREST_RESIN
                '''
                lookback = 20 # How far back to calculate mean/std
                order_limit = 10 # Max number of shares to buy/sell per trade
                max_buy = min(order_limit, abs(50 - my_position))
                max_sell = min(order_limit, abs(my_position + 50))
                
                if len(self.historical_data[product_name]) > lookback:
                    std = np.std(self.historical_data[product_name][-lookback:])
                    mean = np.mean(self.historical_data[product_name][-lookback:])
                    z_score = (mid_price - mean) / std
                    
                    # Place order with max amount at mid_price
                    if z_score > 1:
                        orders.append(Order(product_name, mid_price, -max_sell))
                        print(f'SELL {max_sell} at {mid_price}')
                    elif z_score < -1:
                        orders.append(Order(product_name, mid_price, max_buy))
                        print(f'BUY {max_buy} at {mid_price}')
        
                self.historical_data[product_name].append(mid_price)
                
            elif product_name == '':
                '''
                LOGIC FOR
                '''
                
            elif product_name == '':
                '''
                LOGIC FOR 
                '''
            
                
            result[product_name] = orders # put all the orders together
        
        traderData = state.traderData # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 0 # Converts one stock to another
        
        return result, conversions, traderData
