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

    def get_key(self, service_name):
        try:
            file = open('keys.txt', "r")
            key = file.read()
            key_change = str(key).rfind("?")
            match service_name:
                case 'locIq':
                    return key[:key_change]
                case 'vc':
                    return key[key_change + 1:]

        except:
            print("failed to read key")
