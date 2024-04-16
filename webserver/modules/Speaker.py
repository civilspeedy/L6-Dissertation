from datetime import datetime, date
from os import name
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
        print("Giving message to LM...\n")
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
        print("Figuring out what the user wants...\n")
        json_template = """
{
    weather_report: {
        general_conversation: boolean. 
        weather_report_requested: boolean,
        general_weather_request: boolean,
        specific_days: List<String>,
        temperature_avg: boolean,
        top_temperature: boolean,
        lowest_temperature: boolean,
        feels_like_temperature,
        wind_speed: boolean,
        uv_index: boolean,
        rain: boolean,
        cloud_coverage: boolean,
        visibility: boolean,
        location: string,
        user_has_made_mistake: boolean,
    }
}
"""

        prompt = f"""This is the user's request: {user_message}.
        Please distill into this json format what they want: {json_template}. 
        There name is {name}.
        weather_report_requested can only be true if the user has specifically asked for the weather, 
        if this is not the case, then general_conversation is true (this includes asking the date or time).
        If they have asked just for the weather then general_weather_request must be true.
        Values like Today', 'Weekend', 'Thursday' go in specific_days, and have capitalised first letters.
        Specific_days cannot be an empty array it must have a value.
        If they have asked for a weather report all values in general_inquiry must be false.
        Specific_time refers to time of day, not the day itself. 
        If not specified specific_day defaults to today.
        user_has_made_mistake is for only when you cannot figure out a specific part of the user's request.
        Do not give an explanation. Avoid starting sentences with certainly or similar vocabulary. 
        """
        lm_response = self.send_to_lm(prompt)
        print(lm_response)
        return self.format_lm_json(lm_response)

    def fulfil_request(self, want_json, user_message, name):
        print("Fulfilling User's Request...\n")
        # https://www.w3schools.com/python/ref_dictionary_items.asp
        wants = []
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = date.today()

        if want_json is not None:
            weather_wants = want_json["weather_report"]

            if weather_wants["general_conversation"]:
                return self.send_to_lm(
                    f"""
    Here is the user's message: {user_message}.
    Please respond to them in a polite and brief manor.
    Here is some general information that may help your response:
    current time is {current_time}, the current date is {current_date}, 
    only use this information if it relates to the user's message.

"""
                )

            if weather_wants["weather_report_requested"]:
                for key, item in weather_wants.items():
                    if item:
                        wants.append(key)

                days = self.get_specific_days(weather_wants["specific_days"])
                start_date = days[0]
                end_date = days[1]

                location = self.geocode.default(weather_wants["location"])
                print("location: ", location)
                long = location[0]
                lat = location[1]

                open_metro_report = self.open_metro.request_forecast(
                    long=long,
                    lat=lat,
                    what_user_wants=wants,
                    start_date=start_date,
                    end_date=end_date,
                )

                self.visual_crossing.request_forecast(
                    start_date=start_date,
                    end_date=end_date,
                    location=weather_wants["location"],
                )

                return self.send_to_lm(f"""
    Here is the user's request: {user_message}.
    Here is the information needed for that request: {open_metro_report}.
    The current time is" {current_time}, only relay this if it is relevant to the user's request.
    Here is is a list that shows where if another source shows a different report: {self.compare_reports}. 
    There is no room for Notes or extra comments, focus on providing the information the user has requested.
    Please relay this information to the user in a short, polite and understandable manor.
    """)
            if weather_wants["user_has_made_mistake"]:
                return self.confuse_message()
        else:
            return self.error_message()

    def format_lm_json(self, string):
        print("Formatting the lm's json...\n")
        string_without_grave = string.replace("`", "")

        anti_hallucination = self.check_for_json_hallucination(string_without_grave)

        string_as_json = self.string_to_json(anti_hallucination)

        return string_as_json

    def check_for_json_hallucination(self, string):
        print("Checking for hallucinations...\n")
        print(string, type(string))
        if string[:6] == "python":
            string = string.replace("python", "")
        else:
            string = string.replace("json", "")

        return string

    def compare_reports(self):
        om_report = self.open_metro.report
        vc_report = self.visual_crossing.report
        difference = []

        if om_report is not None and vc_report is not None:
            for key, value in om_report["hourly"].items():
                if key == "time":
                    pass
                else:
                    for i in range(len(om_report["hourly"]["time"])):
                        date_time = self.date_time_conversion(
                            om_report["hourly"]["time"][i]
                        )
                        vc_value = self.visual_crossing.search_report(
                            search_item=key,
                            date=date_time["date"],
                            time=date_time["time"],
                        )
                        if value[i] != vc_value:
                            if vc_value is False:
                                pass
                            else:
                                difference.append(
                                    {
                                        "time": {date_time["time"]},
                                        f"{key}_in_om": value[i],
                                        f"{key}_in_vc": vc_value,
                                    }
                                )
        return difference

    def error_message(self):
        return self.send_to_lm(
            "Please explain to that something has gone wrong and suggest that they try again."
        )

    def confuse_message(self):
        return self.send_to_lm(
            "Please explain to the user that you didn't quite understand what they meant, and ask they they try again."
        )
