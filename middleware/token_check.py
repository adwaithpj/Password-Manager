import json
import requests
import os
from flet_route import Basket


class TokenCheck:
    def __init__(self):
        self.token_file = "bearer_token.json"
        self.validation_url = "https://password-manager-api-2ax5.onrender.com/v1/auth/login"  # Update with the correct endpoint

    def check(self):
        try:
            # Check if the token file exists
            if os.path.exists(self.token_file):
                with open(self.token_file, "r") as file:
                    token_data = json.load(file)

                # Ensure the token key exists in the file
                if "bearer_token" not in token_data:
                    print("Bearer token not found in file.")
                    return False

                # Retrieve the bearer token
                # params = Params()
                bearer_token = token_data["bearer_token"]

                # print(bearer_token)
                # params.bearer_token = bearer_token

                # Validate the token by hitting the endpoint
                headers = {"Authorization": f"Bearer {bearer_token}"}
                response = requests.post(self.validation_url, headers=headers)

                if response.status_code == 200:
                    print("Token is valid.")
                    return True
                else:
                    print(
                        f"Token validation failed: {response.status_code} - {response.text}"
                    )
                    return False
            else:
                print("Token file does not exist.")
                return False
        except Exception as e:
            print(f"An error occurred while checking the token: {str(e)}")
            return False
