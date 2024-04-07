import datetime

from modules.Api import Api


class Open_Metro(Api):
    # https://pypi.org/project/requests/
    def __init__(self):
        super().__init__()

    def request_forecast(self, start_date, end_date, long, lat):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,wind_speed_10m,wind_gusts_10m&start_date={start_date}&end_date={end_date}"
        return self.send_request(url)


class Visual_Crossing(Api):
    def __init__(
        self,
    ):
        super().__init__()
        self.key = self.get_key("vc")

    def request_forecast(self, start_date, end_date, location):
        date = datetime.date.today()
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&key={self.key}&contentType=json"
        response = self.send_request(url)
        return str(response).replace('\\"', '"')

    def get_date(self, today, days):
        return today + datetime.timedelta(days=days)
