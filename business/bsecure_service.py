# payments/bsecure_service.py

import requests
from django.conf import settings

class BsecureService:
    def __init__(self):
        self.client_id = settings.BSECURE['CLIENT_ID']
        self.client_secret = settings.BSECURE['CLIENT_SECRET']
        self.base_url = settings.BSECURE['BASE_URL']
        self.sandbox = settings.BSECURE['SANDBOX']

    def _get_token(self):
        url = f"{self.base_url}/oauth/token"
        try:
            response = requests.post(url, data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            
            if response.status_code != 200:
                print(f"bSecure Token Error: {response.status_code} - {response.text}")
            response.raise_for_status()
            return response.json().get('access_token')
        except Exception as e:
            print(f"Token Request Exception: {e}")
            raise e


    def create_order(self, order_id, amount, currency, customer, redirect_url):
        token = self._get_token()
        url = f"{self.base_url}/v1/{'sandbox/' if self.sandbox else ''}order"
        headers = {'Authorization': f'Bearer {token}'}
        payload = {
            'merchantOrderId': order_id,
            'amount': amount,
            'currency': currency,
            'customer': customer,
            'redirectUrl': redirect_url
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def verify_payment(self, transaction_ref):
        token = self._get_token()
        url = f"{self.base_url}/v1/{'sandbox/' if self.sandbox else ''}transaction/{transaction_ref}"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
