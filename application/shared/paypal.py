from flask import current_app
import requests
import json


class Paypal:
    base_url = current_app.config["PAYPAL_URL"]

    def make_payment(self, id_: int, item):
        headers = {
            'accept': "application/json",
            'accept-language': "de",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.post(f"{self.base_url}/v1/oauth2/token",
                                 data={"grant_type": "client_credentials"},
                                 auth=(current_app.config['CLIENT_ID'],
                                       current_app.config['CLIENT_SECRET']),
                                 headers=headers)
        access_token = response.json()["access_token"]
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
