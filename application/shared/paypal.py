import requests
import json
from .exceptions import PayPalTransactionError


class Paypal:
    def __init__(self, base_url: str,
                 client_id: str,
                 client_secret: str) -> None:
        self.base_url: str = base_url
        self.client_id: str = client_id
        self.client_secret: str = client_secret

    def get_access_token(self) -> str:
        headers = {
            'accept': "application/json",
            'accept-language': "de",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.post(f"{self.base_url}/v1/oauth2/token",
                                 data={"grant_type": "client_credentials"},
                                 auth=(self.client_id,
                                       self.client_secret),
                                 headers=headers)
        return response.json()["access_token"]

    def create_payment(self, id_: int, item) -> requests.Response:
        access_token = self.get_access_token()
        payload = {
          "intent": "CAPTURE",
          "purchase_units": [
            {
              "reference_id": str(id_),
              "amount": {
                "currency_code": "EUR",
                "value": item.get("current_price")
              }
            }
          ],
          "application_context": {
            "return_url": "",
            "cancel_url": ""
          }
        }
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'accept-language': "de",
            'authorization': f"Bearer {access_token}"
        }
        response = requests.post(f"{self.base_url}/v2/checkout/orders",
                                 data=json.dumps(payload),
                                 headers=headers)
        return response

    def get_order(self, order_id: int) -> requests.Response:
        access_token = self.get_access_token()
        headers = {
            'content-type': "application/json",
            'authorization': f"Bearer {access_token}"
        }
        response = requests.get(f"{self.base_url}/v2/checkout/orders/{order_id}",
                                headers=headers)
        if response.status_code != 200:
            raise PayPalTransactionError
        return response
