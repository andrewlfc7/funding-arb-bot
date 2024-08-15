import asyncio
from api.endpoints import ExchangeEndpoints
from api.client import PublicClient


async def main():

    endpoints = ExchangeEndpoints()
    async with PublicClient(endpoints) as client:
        bitget_funding_info = await client.get_funding_info("bitget", "BTC")
        bybit_funding_info = await client.get_funding_info("bybit", "BTC")
        binance_funding_info = await client.get_funding_info("binance", "BTC")
        okx_funding_info = await client.get_funding_info("okx", "BTC")
        gateio_funding_info = await client.get_funding_info("gateio", "BTC")
        paradex_funding_info = await client.get_funding_info("paradex", "BTC")
        aevo_funding_info = await client.get_funding_info("aevo", "ETH")
        apx_funding_info = await client.get_funding_info("apx", "BTC")

        print("Bitget Funding Info:", bitget_funding_info)
        print("Bybit Funding Info:", bybit_funding_info)
        print("Binance Funding Info:", binance_funding_info)
        print("OKX Funding Info:", okx_funding_info)
        print("Gate.io Funding Info:", gateio_funding_info)
        print("Paradex Funding Info:", paradex_funding_info)
        print("Aevo Funding Info:", aevo_funding_info)
        print("APX Funding Info:", apx_funding_info)

if __name__ == "__main__":
    asyncio.run(main())
