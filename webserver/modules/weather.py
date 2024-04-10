import datetime

from networkx import interval_graph
from numpy import info
from modules.Api import Api


class Open_Metro(Api):
    # https://pypi.org/project/requests/
    def __init__(self):
        super().__init__()

    def request_forecast(self, long, lat, what_user_wants, start_date, end_date):
        print("what user wants: ", what_user_wants)
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
        print("info_string: ", info_string)
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

    def request_forecast(self, start_date, end_date, location, what_user_wants):
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&key={self.key}&contentType=json"
        response = self.send_request(url)
        report = str(response).replace('\\"', '"')
        print("visual crossing: ", report)

        report_json = self.string_to_json(report)
        days = report_json["days"]

        for x in what_user_wants:
            match x:
                case "general_weather_request":
                    pass
                    break
                case "top_temperature":
                    pass
                case "lowest_temperature":
                    pass
                case "temperature_avg":
                    pass
                case "feels_like_temperature":
                    pass
                case "wind_speed":
                    pass
                case "uv_index":
                    pass
                case "rain":
                    pass
                case "cloud_coverage":
                    pass
                case "visibility":
                    pass

        return report  # needs system to get specific data

    def get_date(self, today, days):
        return today + datetime.timedelta(days=days)
