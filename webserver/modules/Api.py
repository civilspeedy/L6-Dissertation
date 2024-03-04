from fileinput import filelineno
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

    def write_to_json(self, weather_json, survice_name):
        file_location = "./data/weather_data.json"
        tagged_json = {}

        print(weather_json)
        weather_json = json.JSONDecoder().decode(weather_json)

        match survice_name:
            case "locIq":
                file_location = "./data/geocoding.json"
            case "vc":
                tagged_json["visual crossing"] = weather_json
            case "om":
                tagged_json["open metro"] = weather_json

        with open(file_location, "w") as json_file:
            json.dump(tagged_json, json_file)

        # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
        try:
            with open(file_location, "w", encoding="utf-8") as file:
                json.dump(tagged_json, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Err in {survice_name}.write_to_json ", e)
            # I believe this functional but would not be surprise if otherwise
