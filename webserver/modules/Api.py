import requests
import json


class Api:
    def __init__(self):
        self.locIQ_location, self.weather_data_location = "./data/geocoding.json", "./data/weather_data.json"

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

    def write_to_json(self, weather_json, service_name):
        file_location = self.weather_data_location
        tagged_json = {}

        weather_json = json.JSONDecoder().decode(weather_json)
        # had formatting issues, this solved it https://stackoverflow.com/questions/15272421/python-json-dumps

        match service_name:
            case "locIq":
                file_location = self.locIQ_location
            case "vc":
                tagged_json["visual crossing"] = weather_json
            case "om":
                tagged_json["open metro"] = weather_json

        # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
        try:
            with open(file_location, "a", encoding="utf-8") as file:
                json.dump(tagged_json, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Err in {service_name}.write_to_json ", e)

    def read_from_json(self, service_name):
        file_location = self.weather_data_location

        data_store = []

        if service_name == "locIQ":
            file_location = self.locIQ_location

        try:
            with open(file_location) as file:  # exceeds load size
                data_store.append(json.loads(file))
            return data_store

        except Exception as e:
            print(f"Err in {service_name}.read_from_json", e)
