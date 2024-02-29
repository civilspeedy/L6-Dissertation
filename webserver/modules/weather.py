from datetime import date
import datetime
import os
import requests

from modules.Api import Api


class Weather(Api):
    def __init__(self):
        super().__init__()


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
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/bournemouth/2024-02-01/2024-03-22?unitGroup=metric&key={self.key}&contentType=json"

    def get_date(self, days):
        current_date = date.today()
        return current_date + datetime.timedelta(days=days)
