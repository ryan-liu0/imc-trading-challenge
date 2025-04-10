from datamodel import OrderDepth, UserId, TradingState, Order, Trade
from typing import List
import math
import string
import numpy as np
import pandas as pd
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
                    
                    z_position_cutoff = 0.5
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
                        print(f'SELL {-my_position} at {buy_price}')
                    elif z_sell < z_neutral_cutoff and my_position < 0:
                        orders.append(Order(product_name, int(sell_price), -my_position))
                        print(f'BUY {-my_position} at {sell_price}')

                self.historical_data[product_name].append(mid_price)
                
            elif product_name == "KELP":
                # Calculate mid-price
                best_bid = max(order_book.buy_orders.keys()) if order_book.buy_orders else None
                best_ask = min(order_book.sell_orders.keys()) if order_book.sell_orders else None
                max_buy = min(-sell_amount, abs(50 - my_position))
                max_sell = min(buy_amount, abs(my_position + 50))

                if best_bid is not None and best_ask is not None:
                    mid_price = (best_bid + best_ask) / 2
                    self.historical_data[product_name].append(mid_price)

                    if len(self.historical_data[product_name]) >= 22:
                        prices = pd.Series(self.historical_data[product_name])
                        ema9 = prices.ewm(span=9, adjust=False).mean()
                        ema22 = prices.ewm(span=22, adjust=False).mean()

                        if ema9.iloc[-1] < ema22.iloc[-1] and my_position < 0:
                            orders.append(Order(product_name, int(buy_price), my_position))
                        elif ema9.iloc[-1] > ema22.iloc[-1] and my_position > 0:
                            orders.append(Order(product_name, int(sell_price), -my_position))
                        elif ema9.iloc[-1] < ema22.iloc[-1] and my_position == 0:
                            orders.append(Order(product_name, int(buy_price), max_buy))
                        elif ema9.iloc[-1] > ema22.iloc[-1] and my_position == 0:
                            orders.append(Order(product_name, int(sell_price), -max_sell))

                        

                            
                    
            '''
            elif product_name == "SQUID_INK":
                # INVERTED Volatility Breakout: Fade the spike/drop
                lookback = 30
                std_multiplier = 2
                order_limit = 10

                self.historical_data[product_name].append(mid_price)

                if len(self.historical_data[product_name]) > lookback:
                    mean = np.mean(self.historical_data[product_name][-lookback:])
                    std = np.std(self.historical_data[product_name][-lookback:])
                    upper_band = mean + std_multiplier * std
                    lower_band = mean - std_multiplier * std

                    # Invert: if price spikes, short it; if it crashes, buy it
                    if mid_price > upper_band and my_position > -50:
                        sell_qty = min(order_limit, my_position + 50, buy_amount)
                        if sell_qty > 0:
                            orders.append(Order(product_name, buy_price, -sell_qty))

                    elif mid_price < lower_band and my_position < 50:
                        buy_qty = min(order_limit, 50 - my_position, -sell_amount)
                        if buy_qty > 0:
                            orders.append(Order(product_name, sell_price, buy_qty))
            
                '''
            result[product_name] = orders # put all the orders together
        
        traderData = state.traderData # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 0 # Converts one stock to another
        
        return result, conversions, traderData
