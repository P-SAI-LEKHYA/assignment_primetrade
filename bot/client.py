import time
import hmac
import hashlib
import logging
import requests
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.headers = {"X-MBX-APIKEY": self.api_key}

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, method: str, endpoint: str, payload: dict = None) -> dict:
        if payload is None:
            payload = {}
            
        payload['timestamp'] = int(time.time() * 1000)
        query_string = urlencode(payload)
        signature = self._generate_signature(query_string)
        
        url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"
        
        logger.debug(f"Sending {method} request to {endpoint} with payload: {payload}")
        
        try:
            response = requests.request(method, url, headers=self.headers, timeout=10)
            response_json = response.json()
            
            if response.status_code != 200:
                logger.error(f"Binance API Error [{response.status_code}]: {response_json}")
                response.raise_for_status()
                
            logger.debug(f"API Response Successful: {response_json}")
            return response_json
            
        except requests.exceptions.HTTPError as http_err:
            raise RuntimeError(f"Binance API returned error status: {response.text}") from http_err
        except requests.exceptions.RequestException as req_err:
            raise RuntimeError(f"Network / Connectivity failure: {req_err}") from req_err