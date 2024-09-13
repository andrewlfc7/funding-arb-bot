import aiohttp
from api.endpoints import ExchangeEndpoints
from typing import Dict, Tuple
import time
import json

class PublicClient:
    def __init__(self, endpoints: ExchangeEndpoints):
        self.endpoints = endpoints
        self.session = None

    async def __aenter__(self):

        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

    async def fetch(self, url: str, params: dict = None,payload: dict = None) -> dict:
        if url.startswith(self.endpoints.hyper.base_url):
            headers = {
                "Content-Type": "application/json"
            }
            async with self.session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()
        else:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()


    async def get_prices(self, exchange: str, base_symbol: str) -> dict:
        endpoints = getattr(self.endpoints, exchange)
        url = f"{endpoints.base_url}{endpoints.info}" if exchange == "hyper" else f"{endpoints.base_url}{endpoints.kline}"
        start_time, end_time = self.to_ms('1h')

        if exchange == "bitget":
            params = {
                "symbol": f"{base_symbol}USDT",
                "granularity": "1H",
                "productType": "usdt-futures"
            }
        elif exchange == "bybit":
            params = {
                "category": "linear",
                "symbol": f"{base_symbol}USDT",
                "interval": "1h"
            }
        elif exchange == "binance":
            params = {
                "symbol": f"{base_symbol}USDT",
                "interval": "1h"
            }
        elif exchange == "okx":
            params = {
                "instId": f"{base_symbol}-USDT-SWAP",
                "bar": "1h"
            }
        elif exchange == "gateio":
            params = {
                "contract": f"{base_symbol}_USDT",
                "interval": "1h"
            }
        elif exchange == "paradex":
            params = {
                "end_at":end_time,
                "resolution": "60",
                "start_at":start_time,
                "symbol": f"{base_symbol}-USD-PERP",

            }

        elif exchange == "apx":
            params = {
                "symbol": f"{base_symbol}USDT",
                "interval": "5m"
            }
        elif exchange == "hyper":
            payload = {
                "type": "candleSnapshot",
                "req": {
                    "coin":  f"{base_symbol}",
                    "interval": "5m",
                    "startTime": start_time,
                    "endTime": end_time
                }
            }
            return await self.fetch(url, payload=payload)

        elif exchange == "blofin":
            params = {
                "instId": f"{base_symbol}-USDT",
                "bar": "5m"
            }
        elif exchange == "bfx":
            params = {
                "market_id": f"{base_symbol}-USD",
                "timestamp_from":start_time,
                "timestamp_to":end_time,
                "period": 5
            }
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

        return await self.fetch(url, params)

    async def get_funding_info(self, exchange: str, base_symbol: str) -> dict:
        endpoints = getattr(self.endpoints, exchange)
        url = f"{endpoints.base_url}{endpoints.info}" if exchange == "hyper" else f"{endpoints.base_url}{endpoints.funding_info}"
        start_time, end_time = self.to_ms('1h')
        if exchange == "bitget":
            params = {
                "symbol": f"{base_symbol}USDT",
                "productType": "usdt-futures"
            }
        elif exchange == "bybit":
            params = {
                "category": "linear",
                "symbol": f"{base_symbol}USDT",
                "limit": 1
            }
        elif exchange == "binance":
            params = {"symbol": f"{base_symbol}USDT"}
        elif exchange == "okx":
            params = {
                "instId": f"{base_symbol}-USDT-SWAP"
            }
        elif exchange == "gateio":
            params = {
                "contract": f"{base_symbol}_USDT",
                "limit":4
            }
        elif exchange == "paradex":
            params = {"market": f"{base_symbol}-USD-PERP"}
        elif exchange == "apx":
            params = {"symbol": f"{base_symbol}USDT",
                      "limit":4}

        elif exchange == "hyper":
            payload = {
                "type": "fundingHistory",
                "req": {
                    "coin":  f"{base_symbol}",
                    # "startTime": start_time,
                    # "endTime": end_time
                }
            }
            return await self.fetch(url, payload=payload)

        elif exchange == "blofin":
            params = {
                "instId": f"{base_symbol}-USDT"}

        elif exchange == "bfx":
            params = {
                "market_id": f"{base_symbol}-USD",
                # "start_time":start_time,
                # "end_time":end_time,
                "p_limit": 1000
            }
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

        return await self.fetch(url, params)


    async def get_historical_funding(self, exchange: str, base_symbol: str, start_time: int = 0, end_time: int = 0, limit: int = 10) -> dict:
        endpoints = getattr(self.endpoints, exchange)
        url = f"{endpoints.base_url}{endpoints.historical_funding}"

        if exchange == "bitget":
            params = {
                "symbol": f"{base_symbol}USDT",
                "productType": "usdt-futures"
            }
        elif exchange == "bybit":
            params = {
                "category": "linear",
                "symbol": f"{base_symbol}USDT",
                "startTime": self.to_ms(start_time),
                "endTime": self.to_ms(end_time),
                "limit": limit
            }
        elif exchange == "binance":
            params = {
                "symbol": f"{base_symbol}USDT"
            }
        elif exchange == "okx":
            params = {
                "instId": f"{base_symbol}-USDT-SWAP"
            }
        elif exchange == "gateio":
            params = {
                "contract": f"{base_symbol}_USDT"
            }
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

        return await self.fetch(url, params)


    def to_ms(self, interval: str) -> Tuple[int, int]:
        """Convert a timestamp to milliseconds based on the specified interval."""
        interval_map = {
            "1m": 60000,
            "5m": 300000,
            "15m": 900000,
            "30m": 1800000,
            "1h": 3600000,
            "4h": 14400000,
            "1d": 86400000
        }
        ms_interval = interval_map[interval]
        current_time = int(time.time())
        start_time = current_time - (current_time % ms_interval)
        end_time = start_time + ms_interval
        return start_time, end_time




