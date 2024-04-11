import datetime
from openai import OpenAI

from modules.Api import Api
from modules.Geocoding import Geocoding
from modules.Weather import Open_Metro, Visual_Crossing


class Speaker(Api):
    # from https://build.nvidia.com/google/gemma-7b
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1", api_key=self.get_key("nv")
        )
        self.open_metro = Open_Metro()
        self.visual_crossing = Visual_Crossing()
        self.geocode = Geocoding()

    def send_to_lm(self, prompt):
        response = ""
        request = self.client.chat.completions.create(
            model="google/gemma-7b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True,
        )

        for chunk in request:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return response

    def what_does_user_want(self, user_message):
        json_template = """
{
    weather_report: {
        weather_report_requested: boolean,
        general_weather_request: boolean,
        forecast_for_todays_date: boolean,
        start_date: string,
        end_date: string,
        specific_day: string,
        specific_time: string,
        temperature_avg: boolean,
        top_temperature: boolean,
        lowest_temperature: boolean,
        feels_like_temperature,
        wind_speed: boolean,
        uv_index: boolean,
        rain: boolean,
        cloud_coverage: boolean,
        visibility: boolean,
        location: string
    },
    general_inquiry: {
        current_time: boolean,
        tell_todays_date: boolean,
        other: boolean,
    }
}
"""

        prompt = f"""This is the user's request: {user_message}.
        Please distill into this json format what they want: {json_template}. 
        If they have stated another day forecast_for_todays_date must be false.
        """

        self.fulfil_request(self.format_lm_json(self.send_to_lm(prompt)))

    def fulfil_request(self, want_json):
        # needs return
        # https://www.w3schools.com/python/ref_dictionary_items.asp
        wants = []
        if want_json is not None:
            for topic, sub_topic in want_json.items():
                for item_key, item in sub_topic.items():
                    if item:
                        wants.append(item_key)

            if want_json["weather_report"]["weather_report_requested"]:
                weather_wants = want_json["weather_report"]

                if weather_wants["location"] is not None:
                    long_and_lat = self.geocode.default(weather_wants["location"])
                    long = long_and_lat[0]
                    lat = long_and_lat[1]

                    if weather_wants["forecast_for_todays_date"]:
                        start_date = datetime.date.today()
                        end_date = start_date

                    if weather_wants["forecast_for_todays_date"] is not True:
                        match weather_wants["specific_day"]:
                            case "tomorrow":
                                start_date = self.get_date(datetime.date.today(), 1)
                                end_date = start_date

                            case _:
                                start_date = weather_wants["start_date"]
                                end_date = weather_wants["end_date"]

                    open_metro_report = self.open_metro.request_forecast(
                        long=long,
                        lat=lat,
                        what_user_wants=wants,
                        start_date=start_date,
                        end_date=end_date,
                    )

                    # need visual crossing report here
                    visual_crossing_report = self.visual_crossing.request_forecast(
                        start_date=start_date,
                        end_date=end_date,
                        location=weather_wants["location"],
                        what_user_wants="temp",
                    )

    def format_lm_json(self, string):
        string_without_grave = string.replace("`", "")
        print(string_without_grave)

        anti_hallucination = self.check_for_json_hallucination(string_without_grave)

        string_as_json = self.string_to_json(anti_hallucination)

        return string_as_json

    def check_for_json_hallucination(self, string):
        print(string[:5])
        if string[:6] == "python":
            string = string.replace("python", "")
        else:
            string = string.replace("json", "")

        print(string)
        return string
