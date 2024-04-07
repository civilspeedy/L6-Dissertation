import datetime
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

    def basic_conversation(self, user_message, user_name):
        prompt = f"""You will not refer to yourself as gemma. Here is the user's message: {user_message}.
        There name is: {user_name}. Please respond to them in a polite manor."""
        return self.send_to_lm(prompt=prompt)

    def gainIntent(self, userRequest):
        # intent = self.send_to_lm(
        #   f"""This is the user's request: '{userRequest}'.
        # Please return in a json for the starting day and end day they want and the location they want.
        # In this format:
        # "start_date": start_date,
        # "end_date": end_date,
        # "just_today": boolean,
        # "location": location
        # """
        # )

        intent = self.test_string
        print(intent)
        intent_json = self.format_lm_json(intent)

        return intent_json

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
