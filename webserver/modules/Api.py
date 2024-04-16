import calendar
import requests
import json
import datetime


class Api:
    """Parent class relating to all api data requesting and storage."""

    def __init__(self):
        """Constructor where file locations are defined."""
        pass

    def send_request(self, url):
        print("Sending Request... ", url)
        """Method for sending http requests using passed url and returns data in wrapped in string.

        Parameters:
        - url (String): url for http requests

        Returns:
        String: the response from the request wrapped in a string."""
        try:
            sent_request = requests.get(url)
            sent_request.raise_for_status()
            return sent_request.text
        except requests.exceptions.RequestException as e:
            print(f"Err in Api.send_request \nurl:{url}\n", e)

    def string_to_json(self, string):
        """Simple method for parsing a string into a dict.

        Parameters:
        - string (String): string to be parsed into a dict.

        Returns:
        - Dict: the string now as a dict."""
        print("Converting string to json/dict...\n")
        return json.loads(string)

    def get_key(self, service_name):
        """Reads and returns the required api depending on which service is needed.

        Parameters:
        - service_name (String): the name of the service requiring the key.

        Returns:
        String: the required api key as a string."""
        try:
            with open("keys.json", "r") as file:
                jsonFile = json.load(file)[0]

                match service_name:
                    case "nv":
                        return jsonFile["nvidia"]
                    case "locIq":
                        return jsonFile["locationIq"]
                    case "vc":
                        return jsonFile["visualCrossing"]

        except Exception as e:
            print("err in get_key ", e)

    def today_plus(self, today, days):
        return today + datetime.timedelta(days=days)

    def get_next_day_from_name(self, day_name):
        today = datetime.date.today()
        for i in range(7):
            date = self.today_plus(today=today, days=i)
            if calendar.day_name[date.weekday()] == day_name:
                return date

    def check_if_named_day(self, day):
        for name_of_day in calendar.day_name:
            print(name_of_day)
            if name_of_day == day:
                return True

    def get_specific_days(self, specific_days):
        print("Getting day for report...\n")
        named_days = []
        start_date = None
        end_date = None
        today = datetime.date.today()
        # need something for like, this weekend and the next
        for specific_day in specific_days:  # e.g. monday
            if self.check_if_named_day(specific_day):
                named_days.append(self.get_next_day_from_name(specific_day))

        if named_days != []:
            start_date, end_date = named_days[0], named_days[-1]

        if len(specific_days) == 1:
            specific_day = specific_days[0]
            if self.check_if_named_day(specific_day):
                start_date = self.get_next_day_from_name(specific_day)

            if specific_day in ("today", "Today"):
                start_date = today

            if specific_day in ("tomorrow", "Tomorrow"):
                start_date = self.today_plus(today, 1)

            end_date = start_date

            if specific_day in ("weekend", "Weekend"):
                start_date = self.get_next_day_from_name("Saturday")
                end_date = self.get_next_day_from_name("Sunday")

        return [start_date, end_date, named_days]

    def date_time_conversion(self, date_time):
        date_and_time = date_time.split("T")
        return {"date": date_and_time[0], "time": date_and_time[1] + ":00"}
