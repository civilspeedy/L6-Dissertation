import os
import requests

from modules.Api import Api


class Weather(Api):
    def __init__(self):
        super().__init__()
        self.params = None

    def set_params(self, user_params):
        self.params = user_params


class Open_Metro(Weather):
    # https://pypi.org/project/requests/
    def __init__(self, params):
        super().__init__()
        self.set_params(params)

    def request_report(self, days):
        url = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,evapotranspiration,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_10m,wind_direction_10m,uv_index&forecast_days={days}"
        return self.send_request(url)
