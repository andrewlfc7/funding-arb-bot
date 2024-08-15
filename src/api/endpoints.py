
from dataclasses import dataclass, field

@dataclass
class BitgetEndpoints:
    base_url: str = "https://api.bitget.com"
    funding_info: str = "/api/v2/mix/market/current-fund-rate"
    prices: str = "/api/v2/mix/market/symbol-price"
    historical_funding: str = "/api/v2/mix/market/history-fund-rate"


@dataclass
class BybitEndpoints:
    base_url: str = "https://api.bybit.com"
    funding_info: str = "/v5/market/funding/history"
    prices: str = "/v5/market/tickers"


@dataclass
class BinanceEndpoints:
    base_url: str = "https://fapi.binance.com"
    funding_info: str = "/fapi/v1/fundingInfo"
    historical_funding: str = "/fapi/v1/fundingRate"
    basis: str = "/futures/data/basis"


@dataclass
class OKXEndpoints:
    base_url: str = "https://www.okx.com"
    funding_info: str = "/api/v5/public/funding-rate"
    historical_funding: str = "/api/v5/public/funding-rate-history"
    prices: str = "/api/v5/market/index-tickers"
    mark_price: str = "/api/v5/public/mark-price"


@dataclass
class GateioEndpoints:
    base_url: str = "https://api.gateio.ws/api/v4"
    funding_info: str = "/futures/usdt/funding_rate"
    prices: str = "/futures/usdt/contracts"


@dataclass
class ParadexEndpoints:
    base_url: str = "https://api.prod.paradex.trade/v1"
    funding_info: str = "/funding/data"
    markets_summary: str = "/markets/summary"


@dataclass
class AevoEndpoints:
    base_url: str = "https://api.aevo.xyz"
    funding_info: str = "/funding"
    historical_funding: str = "/funding-history"
    markets: str = "/markets"


@dataclass
class APXEndpoints:
    base_url: str = "https://fapi.apollox.finance"
    funding_info: str = "/fapi/v1/fundingRate"
    premium_index: str = "/fapi/v1/premiumIndex"




@dataclass
class ExchangeEndpoints:
    bitget: BitgetEndpoints = field(default_factory=BitgetEndpoints)
    bybit: BybitEndpoints = field(default_factory=BybitEndpoints)
    binance: BinanceEndpoints = field(default_factory=BinanceEndpoints)
    okx: OKXEndpoints = field(default_factory=OKXEndpoints)
    gateio: GateioEndpoints = field(default_factory=GateioEndpoints)
    paradex: ParadexEndpoints = field(default_factory=ParadexEndpoints)
    aevo: AevoEndpoints = field(default_factory=AevoEndpoints)
    apx: APXEndpoints = field(default_factory=APXEndpoints)


