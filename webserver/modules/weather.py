from datetime import date
import datetime

from modules.Api import Api


class Weather(Api):
    def __init__(self):
        super().__init__()

    def doneAlready(self, requested_date):
        json = self.read_from_json(None)
        if json != None:
            for item in json:
                dates = []
                if isinstance(item, dict):
                    dates = item["open metro"]["hourly"]["time"]
                elif isinstance(item, list):
                    dates = (item[0]["visual crossing"]
                             ["hourly"]["time"])  # not sure why formatter is doing this
                for date in dates:
                    if date[:10] == requested_date:
                        return [True, item]


class Open_Metro(Weather):
    # https://pypi.org/project/requests/
    def __init__(self):
        super().__init__()

    def request_forecast(self, days):
        url = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,evapotranspiration,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_10m,wind_direction_10m,uv_index&forecast_days={days}"
        return self.send_request(url)


class Visual_Crossing(Weather):
    def __init__(self,):
        super().__init__()
        self.key = self.get_key('vc')

    def request_forecast(self, days):
        today = date.today()
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/bournemouth/{today}/{self.get_date(today, days)}?unitGroup=metric&key={self.key}&contentType=json"
        response = self.send_request(url)
        return str(response).replace('\\"', "\"")

    def get_date(self, today, days):
        return today + datetime.timedelta(days=days)
