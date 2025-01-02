import requests


class UpdateData:
    def __init__(self):
        self.root_url = "https://password-manager-api-2ax5.onrender.com/v1/pass"

    def patch_pass(self, id, bearer_token, data):
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        pass_delete_url = f"{self.root_url}/{id}/update/"
        response = requests.patch(url=pass_delete_url, headers=headers, data=data)
        if response.status_code == 200:
            return True
        else:
            return False
