import aiohttp
from api.endpoints import ExchangeEndpoints

class PublicClient:
    def __init__(self, endpoints: ExchangeEndpoints):
        self.endpoints = endpoints
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

    async def fetch(self, url: str, params: dict = None) -> dict:
        async with self.session.get(url, params=params, ssl=False) as response:
            response.raise_for_status()
            return await response.json()

    def to_ms(self, timestamp: int) -> int:
        """Convert a timestamp to milliseconds."""
        return timestamp * 1000

    async def get_funding_info(self, exchange: str, base_symbol: str) -> dict:
        endpoints = getattr(self.endpoints, exchange)
        url = f"{endpoints.base_url}{endpoints.funding_info}"

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
                "contract": f"{base_symbol}_USDT"
            }
        elif exchange == "paradex":
            params = {"market": f"{base_symbol}-USD-PERP"}
        elif exchange == "aevo":
            params = {
                "instrument_name": f"{base_symbol}-PERP"
            }
        elif exchange == "apx":
            params = {"symbol": f"{base_symbol}USDT"}
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

        return await self.fetch(url, params)

    async def get_prices(self, exchange: str, base_symbol: str) -> dict:
        endpoints = getattr(self.endpoints, exchange)

        if exchange == "bitget":
            url = f"{endpoints.base_url}{endpoints.prices}"
            params = {
                "productType": "usdt-futures",
                "symbol": f"{base_symbol}USDT"
            }
            return await self.fetch(url, params)
        elif exchange == "bybit":
            url = f"{endpoints.base_url}{endpoints.prices}"
            params = {
                "category": "linear",
                "symbol": f"{base_symbol}USDT"
            }
            return await self.fetch(url, params)
        elif exchange == "binance":
            url = f"{endpoints.base_url}{endpoints.basis}"
            params = {
                "pair": f"{base_symbol}USDT",
                "contractType": "PERPETUAL"
            }
            return await self.fetch(url, params)
        elif exchange == "okx":
            url = f"{endpoints.base_url}{endpoints.prices}"
            params = {
                "instId": f"{base_symbol}-USDT"
            }
            return await self.fetch(url, params)
        elif exchange == "gateio":
            url = f"{endpoints.base_url}{endpoints.prices}"
            params = {
                "contract": f"{base_symbol}_USDT"
            }
            return await self.fetch(url, params)
        elif exchange == "paradex":
            url = f"{endpoints.base_url}{endpoints.markets_summary}"
            params = {
                "market": f"{base_symbol}-USD-PERP"
            }
            return await self.fetch(url, params)
        elif exchange == "aevo":
            url = f"{endpoints.base_url}{endpoints.markets}"
            params = {
                "asset": base_symbol,
                "instrument_type": "PERPETUAL"
            }
            return await self.fetch(url, params)
        elif exchange == "apx":
            url = f"{endpoints.base_url}{endpoints.premium_index}"
            params = {
                "symbol": f"{base_symbol}USDT"
            }
            return await self.fetch(url, params)
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

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
        elif exchange == "aevo":
            params = {
                "instrument_name": f"{base_symbol}-PERP",
                "start_time": self.to_ms(start_time),
                "end_time": self.to_ms(end_time),
                "limit": limit
            }
        else:
            raise ValueError(f"Unsupported exchange: {exchange}")

        return await self.fetch(url, params)
