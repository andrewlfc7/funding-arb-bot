from dataclasses import dataclass, field
@dataclass
class BitgetEndpoints:
    base_url: str = "https://api.bitget.com"
    funding_info: str = "/api/v2/mix/market/current-fund-rate"
    prices: str = "/api/v2/mix/market/symbol-price"
    historical_funding: str = "/api/v2/mix/market/history-fund-rate"
    kline: str = "/api/v2/mix/market/candles"

@dataclass
class BybitEndpoints:
    base_url: str = "https://api.bybit.com"
    funding_info: str = "/v5/market/funding/history"
    prices: str = "/v5/market/tickers"
    kline: str = "/v5/market/kline"

@dataclass
class BinanceEndpoints:
    base_url: str = "https://fapi.binance.com"
    # funding_info: str = "/fapi/v1/fundingInfo"
    historical_funding: str = "/fapi/v1/fundingRate"
    basis: str = "/futures/data/basis"
    funding_info: str = "/fapi/v1/premiumIndex"
    kline: str = "/fapi/v1/klines"

@dataclass
class OKXEndpoints:
    base_url: str = "https://www.okx.com"
    funding_info: str = "/api/v5/public/funding-rate"
    historical_funding: str = "/api/v5/public/funding-rate-history"
    prices: str = "/api/v5/market/index-tickers"
    mark_price: str = "/api/v5/public/mark-price"
    kline: str = "/api/v5/market/mark-price-candles"

@dataclass
class GateioEndpoints:
    base_url: str = "https://api.gateio.ws/api/v4"
    funding_info: str = "/futures/usdt/funding_rate"
    prices: str = "/futures/usdt/contracts"
    kline: str= "/futures/usdt/candlesticks"


@dataclass
class ParadexEndpoints:
    base_url: str = "https://api.prod.paradex.trade/v1"
    funding_info: str = "/funding/data"
    markets_summary: str = "/markets/summary"
    kline: str = "/markets/klines"

@dataclass
class APXEndpoints:
    base_url: str = "https://fapi.apollox.finance"
    funding_info: str = "/fapi/v1/fundingRate"
    premium_index: str = "/fapi/v1/premiumIndex"
    kline: str = "/fapi/v1/klines"
@dataclass
class HyperEndpoints:
    base_url: str = "https://api.hyperliquid.xyz"
    info: str = "/info"
@dataclass
class BlofinEndpoints:
    base_url: str = "https://openapi.blofin.com/"
    funding_info: str = "api/v1/market/funding-rate"
    kline: str = "api/v1/market/candles"

@dataclass
class BFXEndpoints:
    base_url: str = "https://api.bfx.trade"
    funding_info: str = "/markets/fundingrate"
    kline: str = "/candles"

@dataclass
class LyraEndpoints:
    base_url: str = "https://api.lyra.finance/"
    funding_info: str = "/public/get_funding_rate_history"
    tickers: str = "public/get_all_instruments"
    ticker_info: str = "public/get_ticker"



@dataclass
class ExchangeEndpoints:
    bitget: BitgetEndpoints = field(default_factory=BitgetEndpoints)
    bybit: BybitEndpoints = field(default_factory=BybitEndpoints)
    binance: BinanceEndpoints = field(default_factory=BinanceEndpoints)
    okx: OKXEndpoints = field(default_factory=OKXEndpoints)
    gateio: GateioEndpoints = field(default_factory=GateioEndpoints)
    paradex: ParadexEndpoints = field(default_factory=ParadexEndpoints)
    apx: APXEndpoints = field(default_factory=APXEndpoints)
    hyper: HyperEndpoints = field(default_factory=HyperEndpoints)
    blofin: BlofinEndpoints = field(default_factory=BlofinEndpoints)
    bfx: BFXEndpoints = field(default_factory=BFXEndpoints)
    lyra: LyraEndpoints = field(default_factory=LyraEndpoints)





