from typing import Dict, Any, List


class FundingRateHandler:
    @staticmethod
    def handle_apx(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "symbol": item['symbol'],
                "timestamp": item['fundingTime'],
                "funding_rate": float(item['fundingRate']),
            }
            for item in data
        ]

    @staticmethod
    def handle_blofin(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "symbol": item['instId'],
                "timestamp": int(item['fundingTime']),
                "funding_rate": float(item['fundingRate']),
            }
            for item in data.get("data", [])
        ]

    @staticmethod
    def handle_bfx(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "symbol": item['market_id'],
                "timestamp": int(item['timestamp']),
                "funding_rate": float(item['funding_rate']),
            }
            for item in data.get("result", [])
        ]


