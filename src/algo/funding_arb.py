import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Any

import pandas as pd
import numpy as np
import statsmodels.api as sm

from api.client_cexs import PublicClient
from api.endpoints import ExchangeEndpoints
from api.handlers.funding import FundingRateHandler
from api.handlers.kline import KlineHandler

@dataclass
class RiskManagement:
    positions: List[Dict[str, Any]] = field(default_factory=list)

    def open_position(self, asset, long_exchange, short_exchange, entry_time, expected_duration):
        position = {
            'asset': asset,
            'long_exchange': long_exchange,
            'short_exchange': short_exchange,
            'entry_time': entry_time,
            'expected_duration': expected_duration,
            'status': 'open'
        }
        self.positions.append(position)
        print(f"Opened position: {position}")

    def update_positions(self, current_time):
        for position in self.positions:
            if position['status'] == 'open':
                elapsed_time = current_time - position['entry_time']
                if elapsed_time >= position['expected_duration']:
                    position['status'] = 'closed'
                    position['exit_time'] = current_time
                    print(f"Closed position: {position}")

    def get_open_positions(self):
        return [p for p in self.positions if p['status'] == 'open']

    def get_closed_positions(self):
        return [p for p in self.positions if p['status'] == 'closed']

@dataclass
class FundingArbitrageBot:
    endpoints: ExchangeEndpoints
    client: PublicClient
    assets: List[str] = field(default_factory=list) 
    funding_rates: Dict[str, Dict[str, float]] = field(default_factory=dict)
    prices: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def __post_init__(self):
        self.handlers = {
            "apx": {
                "funding": FundingRateHandler.handle_apx,
                "price": KlineHandler.handle_apx
            },
            "blofin": {
                "funding": FundingRateHandler.handle_blofin,
                "price": KlineHandler.handle_blofin
            },
            "bfx": {
                "funding": FundingRateHandler.handle_bfx,
                "price": KlineHandler.handle_bfx
            }
        }
        self.risk_manager = RiskManagement()
        self.funding_data = {
            exchange: {asset: pd.DataFrame() for asset in self.assets} for exchange in self.handlers.keys()
        }

    async def run(self):
        async with self.client:
            while True:
                await self.update_funding_rates()
                await self.update_prices()
                await self.forecast_funding_rates()
                await self.check_arbitrage_opportunities()
                current_time = pd.Timestamp.now()
                self.risk_manager.update_positions(current_time)
                await asyncio.sleep(36000)  

    async def update_funding_rates(self):
        for asset in self.assets:
            for exchange, handler in self.handlers.items():
                raw_funding_data = await self.client.get_funding_info(exchange, asset)
                parsed_funding_data = handler["funding"](raw_funding_data)
                df = pd.DataFrame(parsed_funding_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.set_index('timestamp', inplace=True)
                if not self.funding_data[exchange][asset].empty:
                    self.funding_data[exchange][asset] = pd.concat([self.funding_data[exchange][asset], df])
                else:
                    self.funding_data[exchange][asset] = df
                latest_funding_rate = df['funding_rate'].iloc[-1]
                self.funding_rates.setdefault(asset, {})[exchange] = {'current': latest_funding_rate}

    async def update_prices(self):
        for asset in self.assets:
            for exchange, handler in self.handlers.items():
                raw_price_data = await self.client.get_prices(exchange, asset)
                parsed_price_data = handler["price"](raw_price_data)
                latest_price = parsed_price_data[-1]['close'] 
                self.prices.setdefault(asset, {})[exchange] = latest_price

    async def forecast_funding_rates(self):
        for exchange, assets_data in self.funding_data.items():
            for asset, df in assets_data.items():
                if df.empty or len(df) < 10:  
                    continue

                df_resampled = df['funding_rate'].resample('8H').mean()
                window_size = 8  
                df_resampled = df_resampled.dropna()
                df_resampled = df_resampled.to_frame()
                df_resampled['rolling_avg'] = df_resampled['funding_rate'].rolling(window=window_size).mean()
                df_resampled = df_resampled.dropna()
                if df_resampled.empty:
                    continue

                X = df_resampled['rolling_avg']
                y = df_resampled['funding_rate']
                X = sm.add_constant(X)
                model = sm.OLS(y, X).fit()
                latest_avg = df_resampled['rolling_avg'].iloc[-1]
                X_pred = sm.add_constant(pd.DataFrame({'rolling_avg': [latest_avg]}))
                forecast = model.predict(X_pred)[0]
                self.funding_rates[asset][exchange]['forecast'] = forecast
                half_life = self.calculate_half_life(model)
                self.funding_rates[asset][exchange]['half_life'] = half_life

    def calculate_half_life(self, model):
        params = model.params
        if 'rolling_avg' in params:
            beta = params['rolling_avg']
            if beta != 0:
                half_life = -np.log(2) / np.log(beta)
                return max(0, half_life)  
        return np.inf  

    async def check_arbitrage_opportunities(self):
        timestamp = pd.Timestamp.now()
        for asset in self.assets:
            positive_funding_exchanges = [
                ex for ex, rate_info in self.funding_rates[asset].items()
                if rate_info.get('forecast', 0) > 0
            ]
            negative_funding_exchanges = [
                ex for ex, rate_info in self.funding_rates[asset].items()
                if rate_info.get('forecast', 0) < 0
            ]

            if positive_funding_exchanges and negative_funding_exchanges:
                for pos_ex in positive_funding_exchanges:
                    for neg_ex in negative_funding_exchanges:
                        pos_price = self.prices[asset].get(pos_ex)
                        neg_price = self.prices[asset].get(neg_ex)

                        if pos_price is None or neg_price is None:
                            continue

                        half_life_neg = self.funding_rates[asset][neg_ex].get('half_life', np.inf)
                        half_life_pos = self.funding_rates[asset][pos_ex].get('half_life', np.inf)
                        expected_duration = min(half_life_neg, half_life_pos)

                        if expected_duration == np.inf:
                            continue  
                        print(
                            f"Potential arbitrage opportunity for {asset}: "
                            f"Long {asset} on {neg_ex} (forecasted funding rate: {self.funding_rates[asset][neg_ex]['forecast']}, half-life: {half_life_neg} periods) "
                            f"Short {asset} on {pos_ex} (forecasted funding rate: {self.funding_rates[asset][pos_ex]['forecast']}, half-life: {half_life_pos} periods) "
                            f"Expected profitable duration: {expected_duration} periods"
                        )

                        self.risk_manager.open_position(
                            asset=asset,
                            long_exchange=neg_ex,
                            short_exchange=pos_ex,
                            entry_time=timestamp,
                            expected_duration=pd.Timedelta(hours=expected_duration * 8)  
                        )

    def analyze_positions(self):
        closed_positions = self.risk_manager.get_closed_positions()
        positions_df = pd.DataFrame(closed_positions)
        if not positions_df.empty:
            positions_df['Duration'] = positions_df['exit_time'] - positions_df['entry_time']
            print("Closed Positions Analysis:")
            print(positions_df[['asset', 'long_exchange', 'short_exchange', 'entry_time', 'exit_time', 'Duration']])
        else:
            print("No closed positions to analyze.")

