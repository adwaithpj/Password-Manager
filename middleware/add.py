import requests
import json


class AddPassword:
    def __init__(self):
        self.root_url = "https://password-manager-api-2ax5.onrender.com/v1/pass/create"

    def add(self, data, bearer_token):
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        add_url = f"{self.root_url}/"
        response = requests.post(url=add_url, data=json.dumps(data), headers=headers)
        return response
