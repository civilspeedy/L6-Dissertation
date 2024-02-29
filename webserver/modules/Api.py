import requests
import json


class Api:
    def __init__(self):
        pass

    def send_request(self, url):
        try:
            sent_request = requests.get(url)
            sent_request.raise_for_status()
            return sent_request.text
        except requests.exceptions.RequestException as e:
            print(f"Err in Api.send_request \nurl:{url}\n", e)

    def string_to_json(self, string):
        return json.loads(string)
