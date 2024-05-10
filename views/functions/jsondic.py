import json


class JsonDict:
    def __init__(self, website_name: str, email_id: str, password: str):
        self.website_name = website_name
        self.email_id = email_id
        self.password = password
        self.encoded_pass = 0
        self.existing_data = {}
        self.saving_data = False
        self.load_json()

    def encode_password(self, to_encode_pass: str):
        # Simple encoding using base64
        self.encoded_pass = to_encode_pass.encode('utf-8').hex()
        return self.encoded_pass

    def decode_password(self, encoded_password):
        # Simple decoding using base64
        decoded_password = bytes.fromhex(encoded_password).decode('utf-8')
        return decoded_password


    def save_json(self):
        self.password = self.encode_password(self.password)
        self.existing_data[self.website_name] = {
            "email": self.email_id,
            "password": self.password
        }
        try:
            with open("pass.json", "w") as save_json_file:
                json.dump(self.existing_data, save_json_file)
                return True
        except FileNotFoundError:
            return False

    def load_json(self):
        try:
            with open("pass.json", "r") as json_file:
                try:
                    self.existing_data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    # Handle an empty file or invalid JSON
                    self.existing_data = {}

                if not self.existing_data:
                    self.existing_data = {self.website_name: {self.email_id: self.password}}
                    self.saving_data = self.save_json()
                    return self.saving_data
                else:
                    self.saving_data = self.save_json()
                    return self.saving_data
        except FileNotFoundError:

            # If the file doesn't exist, create a new file
            self.save_json()
            return None

    def show_json(self, website_name: str):
        try:
            with open("pass.json", "r") as json_file:
                self.existing_data = json.load(json_file)
                self.password = self.decode_password(self.existing_data[website_name]["password"])
                return self.existing_data[website_name][self.email_id], self.existing_data[website_name][self.password]

        except FileNotFoundError:
            pass



