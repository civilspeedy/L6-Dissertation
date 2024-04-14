from modules.Api import Api


class Open_Metro(Api):
    # https://pypi.org/project/requests/
    def __init__(self):
        super().__init__()

    def request_forecast(self, long, lat, what_user_wants, start_date, end_date):
        print("Requesting forecast from open metro...\n")
        info_string = ""

        for x in what_user_wants:
            match x:
                case "general_weather_request":
                    info_string = "temperature_2m,weather_code"
                    break
                case "top_temperature":
                    info_string += "temperature_2m_max,"
                case "lowest_temperature":
                    info_string += "temperature_2m_min,"
                case "temperature_avg":
                    info_string += "temperature_2m,"
                case "feels_like_temperature":
                    info_string += "apparent_temperature,"
                case "wind_speed":
                    info_string += "wind_speed_10m,"
                case "uv_index":
                    info_string += "uv_index,"
                case "rain":
                    info_string += "rain,"
                case "cloud_coverage":
                    info_string += "cloud_cover,"
                case "visibility":
                    info_string += "visibility,"

        if info_string[-1] == ",":
            info_string = info_string[:-1]

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly={info_string}&start_date={start_date}&end_date={end_date}"

        return self.send_request(url)


class Visual_Crossing(Api):
    def __init__(
        self,
    ):
        super().__init__()
        self.key = self.get_key("vc")
        self.report = None

    def request_forecast(self, start_date, end_date, location):
        # not done COME BACK TO THIS
        print("Requesting forecast from visual crossing...\n")
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&key={self.key}&contentType=json"

        response = self.send_request(url)
        report = str(response).replace('\\"', '"')

        self.report = self.string_to_json(report)

        return self.report

    def search_report(self, search_item, date, time):
        print("Searching for specific item...")
        key = ""
        if self.report is not None:
            match search_item:
                case "temperature":
                    key = "temp"
                case "feels like temp":
                    key = "feelslike"
                case "wind speed":
                    key = "windspeed"
                case "uv index":
                    key = "uvindex"
                case "rain":
                    key = "precip"
                case "time":
                    key = "datetime"
                case "cloud cover":
                    key = "cloudcover"
                case "visibility":
                    key = "visibility"

            days = self.report["days"]
            for day in days:
                if day["datetime"] == str(date):
                    hours = day["hours"]
                    for hour in hours:
                        if hour["datetime"] == time:
                            if key in hour:
                                item = hour[key]
                                return item
                            else:
                                return False

                    return False

            return False
