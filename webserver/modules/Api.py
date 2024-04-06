import os
import requests
import json


class Api:
    """Parent class relating to all api data requesting and storage."""

    def __init__(self):
        """Constructor where file locations are defined."""
        self.locIQ_location, self.weather_data_location = (
            "./data/geocoding.json",
            "./data/weather_data.json",
        )

    def send_request(self, url):
        """Method for sending http requests using passed url and returns data in wrapped in string.

        Parameters:
        - url (String): url for http requests

        Returns:
        String: the response from the request wrapped in a string."""
        try:
            sent_request = requests.get(url)
            sent_request.raise_for_status()
            return sent_request.text
        except requests.exceptions.RequestException as e:
            print(f"Err in Api.send_request \nurl:{url}\n", e)

    def string_to_json(self, string):
        """Simple method for parsing a string into a dict.

        Parameters:
        - string (String): string to be parsed into a dict.

        Returns:
        - Dict: the string now as a dict."""
        return json.loads(string)

    def get_key(self, service_name):
        """Reads and returns the required api depending on which service is needed.

        Parameters:
        - service_name (String): the name of the service requiring the key.

        Returns:
        String: the required api key as a string."""
        try:
            with open("keys.json", "r") as file:
                jsonFile = json.load(file)[0]

                match service_name:
                    case "nv":
                        return jsonFile["nvidia"]
                    case "locIq":
                        return jsonFile["locationIq"]
                    case "vc":
                        return jsonFile["visualCrossing"]

        except Exception as e:
            print("err in get_key ", e)

    def write_to_json(self, json_data, service_name):
        """Writes a passed dict into the corresponding json file.

        Parameters:
        - json_data (String): data in the format of a json but wrapped in a string.
        - service_name (String): name of the service where the data came from.
        """
        file_location, tagged_json, json_array = self.weather_data_location, {}, []

        json_data = json.JSONDecoder().decode(json_data)
        # had formatting issues, this solved it https://stackoverflow.com/questions/15272421/python-json-dumps

        match service_name:
            case "locIq":
                file_location = self.locIQ_location
                tagged_json = json_data
            case "vc":
                tagged_json["visual crossing"] = json_data
            case "om":
                tagged_json["open metro"] = json_data

        try:
            if os.path.exists(file_location):
                with open(file_location, "r", encoding="utf-8") as file:
                    data_before = json.load(file)
                json_array.append(data_before)

            json_array.append(tagged_json)
            # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
            with open(file_location, "w", encoding="utf-8") as file:
                json.dump(json_array, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Err in {service_name}.write_to_json ", e)

    def read_from_json(self, service_name):
        """Reads json based on provided service name.

        Parameters:
        - service_name (String): specifying which data to read.

        Returns:
        Dict: dict containing the data from the json.

        """
        file_location = self.weather_data_location
        if service_name == "locIQ":
            file_location = self.locIQ_location
        try:
            with open(file_location, "r") as file:  # exceeds load size
                return json.load(file)
        except Exception as e:
            print(f"Err in {service_name}.read_from_json", e)

    def check_report_exists(self, requested_date):
        json, return_array = self.read_from_json(None), []

        # needs to check if locations are the same
        if json is not None:
            for item in json:
                dates = []
                if item is not None:
                    if isinstance(item, dict):
                        dates = item["open metro"]["hourly"]["time"]
                    elif isinstance(item, list):
                        dates = item[0]["visual crossing"]["hourly"][
                            "time"
                        ]  # not sure why formatter is doing this
                    for date in dates:
                        if date[:10] == requested_date:
                            return_array.append(item)
        return return_array  # sort of works, data looked a bit odd, needs another look

    def format_report(self):
        json = self.read_from_json(None)
        # not sure if nessisary

        if json is not None:
            for item in json:
                if isinstance(item, dict):
                    print(item["open metro"]["hourly"]["apparent_temperature"])
