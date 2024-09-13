import asyncio
from api.client_cexs import PublicClient
from api.endpoints import ExchangeEndpoints
from algo.funding_arb import FundingArbitrageBot


async def main():
    # Initialize the required components
    endpoints = ExchangeEndpoints()
    client = PublicClient(endpoints)
    
    # Instantiate the bot with a list of assets (coins)
    bot = FundingArbitrageBot(
        endpoints=endpoints,
        
        client=client,
        assets=["BTC", "ETH", "SOL"]  # Example list of coins
    )

    # Run the bot
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
