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
        print("Giving message to LM...")
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
        print("Figuring out what the user wants...")
        json_template = """

    weather_report: {
        weather_report_requested: boolean,
        general_weather_request: boolean,
        specific_days: List<String>,
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
    }

"""

        prompt = f"""This is the user's request: {user_message}.
        Please distill into this json format what they want: {json_template}. 
        If they have asked just for the weather then general_weather_request must be true.
        Values like 'today', 'weekend', 'thursday' go in specific_days.
        If they have asked for a weather report all values in general_inquiry must be false.
        Do not give an explanation.
        """
        lm_response = self.send_to_lm(prompt)
        print(lm_response)
        self.fulfil_request(self.format_lm_json(lm_response))

    def fulfil_request(self, want_json):
        print("Fulfilling User's Request...")
        # https://www.w3schools.com/python/ref_dictionary_items.asp
        wants = []
        other_wants_list = []
        # avoid heavy nesting at all costs

        weather_wants = want_json["weather_report"]

        if weather_wants["weather_report_requested"]:
            for key, item in weather_wants.items():
                if item:
                    wants.append(key)

            days = self.get_specific_days(weather_wants["specific_days"])
            start_date = days[0]
            end_date = days[1]

            location = self.geocode.default(weather_wants["location"])
            long = location[0]
            lat = location[0]

            open_metro_report = self.open_metro.request_forecast(
                long=long,
                lat=lat,
                what_user_wants=wants,
                start_date=start_date,
                end_date=end_date,
            )
            print("open_metro_report: ", open_metro_report)

            visual_crossing_report = self.visual_crossing.request_forecast(
                start_date=start_date,
                end_date=end_date,
                location=weather_wants["location"],
                what_user_wants=wants,
            )
            print("visual_crossing_report: ", visual_crossing_report)

    def format_lm_json(self, string):
        print("Formatting the lm's json...")
        string_without_grave = string.replace("`", "")

        anti_hallucination = self.check_for_json_hallucination(string_without_grave)

        string_as_json = self.string_to_json(anti_hallucination)

        return string_as_json

    def check_for_json_hallucination(self, string):
        print("Checking for hallucinations...")
        if string[:6] == "python":
            string = string.replace("python", "")
        else:
            string = string.replace("json", "")

        return string
