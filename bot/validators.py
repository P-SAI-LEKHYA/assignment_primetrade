# bot/validators.py

def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string identifier (e.g., 'BTCUSDT').")
        
    if not isinstance(side, str) or side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Execution Side must be strictly defined as a string: 'BUY' or 'SELL'.")
        
    if not isinstance(order_type, str) or order_type.upper() not in ["MARKET", "LIMIT", "STOP_LIMIT"]:
        raise ValueError("Order Type must be strictly a string: 'MARKET', 'LIMIT', or 'STOP_LIMIT'.")
        
    # 2. String/Alphabet Type Guard for Quantity
    # Checks if the user passed an alphabetical string instead of a number
    if isinstance(quantity, str):
        raise ValueError("Quantity cannot be an alphabetical string. It must be a numeric value.")
        
    if not isinstance(quantity, (int, float)):
        raise ValueError("Quantity must be a valid integer or float number.")
        
    if quantity <= 0:
        raise ValueError("Asset execution Quantity must be greater than zero.")
        
    if order_type.upper() in ["LIMIT", "STOP_LIMIT"]:
        if price is None:
            raise ValueError("Execution target Price is required for LIMIT/STOP_LIMIT orders.")
            
        if isinstance(price, str):
            raise ValueError("Price cannot be an alphabetical string. It must be a numeric value.")
            
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a valid integer or float number.")
            
        if price <= 0:
            raise ValueError("Execution target Price must be greater than zero.")