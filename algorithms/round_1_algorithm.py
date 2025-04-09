from datamodel import OrderDepth, UserId, TradingState, Order, Trade
from typing import List
import math
import string
import numpy as np
from collections import defaultdict

class Trader:
    def __init__(self):
        self.historical_data = defaultdict(list)
    
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
            
            # Note: Sell amount is negative
            sell_price, sell_amount = list(order_book.sell_orders.items())[0]
            buy_price, buy_amount = list(order_book.buy_orders.items())[0]
            mid_price = (sell_price + buy_price) / 2
            print(f'Mid Price: {mid_price}')
            
            if product_name == "RAINFOREST_RESIN":
                '''
                Logic for RAINFOREST_RESIN
                '''
                lookback = 20 # How far back to calculate mean/std
                order_limit = 10 # Max number of shares to buy/sell per trade
                max_buy = min(-sell_amount, abs(50 - my_position))
                max_sell = min(buy_amount, abs(my_position + 50))
                
                if len(self.historical_data[product_name]) > lookback:
                    std = np.std(self.historical_data[product_name][-lookback:])
                    mean = np.mean(self.historical_data[product_name][-lookback:])
                    z_buy = (buy_price - mean) / std
                    z_sell = (sell_price - mean) / std
                    z_score = (mid_price - mean ) / std
                    
                    z_position_cutoff = 1
                    z_neutral_cutoff = 0
                    
                    # Place order, if buyers above then sell, if sellers above then buy
                    if z_buy > z_position_cutoff and my_position == 0:
                        orders.append(Order(product_name, int(buy_price), -max_sell))
                        print(f'SELL {max_sell} at {z_buy}')
                    elif z_sell < -z_position_cutoff and my_position == 0:
                        orders.append(Order(product_name, int(sell_price), max_buy))
                        print(f'BUY {max_buy} at {z_sell}')
        
                    if z_buy > -z_neutral_cutoff and my_position > 0:
                        orders.append(Order(product_name, int(buy_price), -my_position))
                        print(f'TRADE {-my_position} at {buy_price}')
                    elif z_sell < z_neutral_cutoff and my_position < 0:
                        orders.append(Order(product_name, int(sell_price), -my_position))
                    

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
