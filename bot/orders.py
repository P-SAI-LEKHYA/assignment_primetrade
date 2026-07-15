import logging
from bot.client import BinanceFuturesClient
from bot.validators import validate_order_inputs

logger = logging.getLogger(__name__)

class OrderManager:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def create_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        # Validate baseline formatting strings ahead of compilation
        validate_order_inputs(symbol, side, order_type, quantity, price)
        
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()
        
        payload = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        
        if order_type == "LIMIT":
            payload["price"] = price
            payload["timeInForce"] = "GTC"  # Good 'Till Cancelled standard inclusion

        logger.info(f"Dispatching [{order_type}] order payload targeting {side} {quantity} {symbol}...")
        return self.client.send_signed_request("POST", "/fapi/v1/order", payload)