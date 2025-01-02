import requests


class DeleteData:
    def __init__(self):
        self.root_url = "https://password-manager-api-2ax5.onrender.com/v1/pass/delete"

    def delete_pass(self, id, bearer_token):
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        pass_delete_url = f"{self.root_url}/{id}"
        response = requests.delete(url=pass_delete_url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False


class DeleteAccount:
    def __init__(self):
        self.root_url = "https://password-manager-api-2ax5.onrender.com/v1/users"

    def delete_user(self, id, bearer_token):
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        pass_delete_url = f"{self.root_url}/{id}/"
        response = requests.delete(url=pass_delete_url, headers=headers)
        print(response)
        print(response.status_code)
        if response.status_code == 200:
            return True
        else:
            return False
