from typing import List, Dict, Any
import asyncio
from typing import List, Dict, Any

class KlineHandler:

    @staticmethod
    async def handle_apx(symbol: str, data: List[List[Any]]) -> List[Dict[str, Any]]:
        """
        Parses the raw data from APX exchange.
        APX data format: [timestamp, open, high, low, close, volume, close_time, ...]
        """
        return [
            {
                "symbol": symbol,
                "timestamp": item[0],  
                "open": float(item[1]),  
                "high": float(item[2]),  
                "low": float(item[3]),  
                "close": float(item[4]),  
                "volume": float(item[5]),  
            }
            for item in data
        ]

    @staticmethod
    async def handle_blofin(symbol: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parses the raw data from Blofin exchange.
        Blofin data format: {"code": "0", "msg": "success", "data": [[timestamp, open, high, low, close, volume, ...], ...]}
        """
        return [
            {
                "symbol": symbol,
                "timestamp": int(item[0]),  
                "open": float(item[1]),  
                "high": float(item[2]),  
                "low": float(item[3]),  
                "close": float(item[4]),  
                "volume": float(item[5]),  
            }
            for item in data.get("data", []) if data.get("code") == "0"
        ]

    @staticmethod
    async def handle_bfx(symbol: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parses the raw data from BFX exchange.
        BFX data format: {"success": True, "request_id": "...", "result": [{"time": timestamp, "low": "...", "high": "...", "open": "...", "close": "...", "volume": "..."}, ...]}
        """
        return [
            {
                "symbol": symbol,
                "timestamp": item['time'],  
                "open": float(item['open']),  
                "high": float(item['high']),  
                "low": float(item['low']),  
                "close": float(item['close']),  
                "volume": float(item['volume']),  
                **{k: v for k, v in item.items() if k not in {'time', 'open', 'high', 'low', 'close', 'volume'}}
            }
            for item in data.get("result", []) if data.get("success")
        ]

    @staticmethod
    async def handle_all(symbol: str, apx_data: List[List[Any]], blofin_data: Dict[str, Any], bfx_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Handles data for all exchanges concurrently.
        """
        apx_task = asyncio.create_task(KlineHandler.handle_apx(symbol, apx_data))
        blofin_task = asyncio.create_task(KlineHandler.handle_blofin(symbol, blofin_data))
        bfx_task = asyncio.create_task(KlineHandler.handle_bfx(symbol, bfx_data))

        apx_result, blofin_result, bfx_result = await asyncio.gather(apx_task, blofin_task, bfx_task)

        return {
            "APX": apx_result,
            "Blofin": blofin_result,
            "BFX": bfx_result
        }
