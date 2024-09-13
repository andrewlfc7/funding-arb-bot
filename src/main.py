import asyncio
from api.endpoints import ExchangeEndpoints
from api.client_cexs import PublicClient


async def main():
    endpoints = ExchangeEndpoints()
    async with PublicClient(endpoints) as client:
        # paradex_funding_info = await client.get_funding_info("paradex", "BTC")
        apx_funding_info = await client.get_funding_info("apx", "BTC")
        # hyper_funding_info = await client.get_funding_info("hyper", "BTC")
        blofin_funding_info = await client.get_funding_info("blofin", "BTC")
        bfx_funding_info = await client.get_funding_info("bfx", "BTC")



        # print("Hyper Funding Info:", hyper_funding_info)
        # print("Paradex Funding Info:", paradex_funding_info)
        print("APX Funding Info:", apx_funding_info)
        print("BFX Funding Info:", bfx_funding_info)
        print("Blofin Funding Info:", blofin_funding_info)


        paradex_prices = await client.get_prices("paradex", "BTC")
        apx_prices = await client.get_prices("apx", "BTC")
        # hyper_prices = await client.get_prices("hyper", "BTC")
        blofin_prices = await client.get_prices("blofin", "BTC")
        bfx_prices = await client.get_prices("bfx", "BTC")


        # print("Paradex Prices:", paradex_prices)
        # print("Hyper Prices:", hyper_prices)
        # print("APX Prices:", apx_prices)
        # print("Blofin Prices:", blofin_prices)
        # print("BFX Prices:", bfx_prices)


if __name__ == "__main__":
    asyncio.run(main())

