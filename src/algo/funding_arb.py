from itertools import combinations, permutations



class FundingArbitrageBot:
    def __init__(self, endpoints: ExchangeEndpoints, client: PublicClient, assets: List[str]):
        self.endpoints = endpoints
        self.client = client
        self.assets = assets

    async def check_arbitrage_opportunities(self):
        for asset in self.assets:
            # funding_rates = self.exchange_handler.get_latest_funding_rates(asset)
            # prices = self.exchange_handler.get_latest_prices(asset)


            positive_funding_exchanges = [ex for ex, rate in funding_rates.items() if rate > 0]
            negative_funding_exchanges = [ex for ex, rate in funding_rates.items() if rate < 0]

            if positive_funding_exchanges and negative_funding_exchanges:
                for pos_ex, neg_ex in permutations(positive_funding_exchanges, negative_funding_exchanges):
                    pos_price = prices[pos_ex]
                    neg_price = prices[neg_ex]

                    if pos_price > neg_price:
                        print(
                            f"Potential arbitrage opportunity for {asset}:"
                            f"Long {asset} on {neg_ex} (funding rate: {funding_rates[neg_ex]})"
                            f"Short {asset} on {pos_ex} (funding rate: {funding_rates[pos_ex]})"
                        )
