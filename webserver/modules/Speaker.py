import datetime
import json
import string
from openai import OpenAI

from modules.Api import Api


class Speaker(Api):
    # from https://build.nvidia.com/google/gemma-7b
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1", api_key=self.get_key("nv")
        )
        self.test_string = """
```json
{
    "start_date": "2023-10-27",
    "end_date": "2023-10-27",
    "just_today": true,
    "location": "London"
}
```
"""

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
        requested: boolean,
        start_date: string,
        end_date: string,
        specific_day: string,
        specific_time: string,
        temperature_avg: boolean,
        top_temperature: boolean,
        lowest_temperature: boolean,
        wind_speed: boolean,
        air_pollution: boolean,
        rain_probability: boolean,
        cloud_coverage: boolean,
        visibility: boolean,
        location: string
    },
    general_inquiry: {
        current_time: boolean,
        today_date: boolean,
        other: boolean,
    }
}
"""

        prompt = f"""This is the user's request: {user_message}.
        Please distill into this json format what they want: {json_template}
        """

        return self.format_lm_json(self.send_to_lm(prompt))

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
