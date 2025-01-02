import requests
import json


class FetchData:
    def fetch(self, bearer_token):
        FETCH_URL = "https://password-manager-api-2ax5.onrender.com/v1/pass/"
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(FETCH_URL, headers=headers)
        print(response.json())
        return response.json()
