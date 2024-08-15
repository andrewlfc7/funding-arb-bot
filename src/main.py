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
        # # paradex_funding_info = await client.get_funding_info("paradex", "BTC")
        apx_funding_info = await client.get_funding_info("apx", "BTC")
        # # hyper_funding_info = await client.get_funding_info("hyper", "BTC")
        blofin_funding_info = await client.get_funding_info("blofin", "BTC")
        bfx_funding_info = await client.get_funding_info("bfx", "BTC")


        print("Bitget Funding Info:", bitget_funding_info)
        print("Bybit Funding Info:", bybit_funding_info)
        print("Binance Funding Info:", binance_funding_info)
        print("OKX Funding Info:", okx_funding_info)
        print("Gate.io Funding Info:", gateio_funding_info)
        # # print("Paradex Funding Info:", paradex_funding_info)
        print("APX Funding Info:", apx_funding_info)
        print("BFX Funding Info:", bfx_funding_info)
        print("Blofin Funding Info:", blofin_funding_info)


        bitget_prices = await client.get_prices("bitget", "BTC")
        bybit_prices = await client.get_prices("bybit", "BTC")
        binance_prices = await client.get_prices("binance", "BTC")
        okx_prices = await client.get_prices("okx", "BTC")
        gateio_prices = await client.get_prices("gateio", "BTC")
        # paradex_prices = await client.get_prices("paradex", "BTC")
        apx_prices = await client.get_prices("apx", "BTC")
        hyper_prices = await client.get_prices("hyper", "BTC")
        blofin_prices = await client.get_prices("blofin", "BTC")
        bfx_prices = await client.get_prices("bfx", "BTC")


        print("Bitget Prices:", bitget_prices)
        print("Bybit Prices:", bybit_prices)
        print("Binance Prices:", binance_prices)
        print("OKX Prices:", okx_prices)
        print("Gate.io Prices:", gateio_prices)
        # print("Paradex Prices:", paradex_prices)
        print("Hyper Prices:", hyper_prices)
        print("APX Prices:", apx_prices)
        print("Blofin Prices:", blofin_prices)
        print("BFX Prices:", bfx_prices)


if __name__ == "__main__":
    asyncio.run(main())
