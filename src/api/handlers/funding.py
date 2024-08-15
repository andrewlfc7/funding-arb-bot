from typing import Dict

class FundingHandler:
    def __init__(self) -> None:
        self.funding_rates: Dict[str, Dict[str, float]] = {}

    def initialize(self, data: Dict) -> None:
        if "data" in data:
            for funding in data["data"]:
                symbol = funding["symbol"]
                funding_rate = float(funding["fundingRate"])
                self.funding_rates[symbol] = {"bitget": funding_rate}
        elif "result" in data:
            for funding in data["result"]["list"]:
                symbol = funding["symbol"]
                funding_rate = float(funding["fundingRate"])
                self.funding_rates[symbol] = {"bybit": funding_rate}
        elif "symbol" in data:
            symbol = data["symbol"]
            funding_rate = float(data["lastFundingRate"])
            self.funding_rates[symbol] = {"binance": funding_rate}
        elif "data" in data:
            for funding in data["data"]:
                symbol = funding["instId"].split("-")[0]
                funding_rate = float(funding["fundingRate"])
                self.funding_rates[symbol] = {"okx": funding_rate}
        elif isinstance(data, list):
            for funding in data:
                symbol = "BTC-USDT"
                funding_rate = float(funding["r"])
                self.funding_rates[symbol] = {"gateio": funding_rate}
        elif isinstance(data, list):
            for funding in data:
                symbol = funding["symbol"]
                funding_rate = float(funding["fundingRate"])
                self.funding_rates[symbol] = {"apx": funding_rate}
        elif "result" in data:
            for funding in data["result"]:
                symbol = "BTC-USD"
                funding_rate = float(funding["funding_rate"])
                self.funding_rates[symbol] = {"bfx": funding_rate}
        elif "data" in data:
            for funding in data["data"]:
                symbol = funding["instId"]
                funding_rate = float(funding["fundingRate"])
                self.funding_rates[symbol] = {"blofin": funding_rate}

    def process(self, recv: Dict) -> None:
        self.initialize(recv)
