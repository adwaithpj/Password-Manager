import requests


class RefreshRequest:
    def run(self):
        try:
            result = requests.get(
                "https://password-manager-api-2ax5.onrender.com/reload"
            )
            if result.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False
