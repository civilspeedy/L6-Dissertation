import calendar
import requests
import json
import datetime


class Api:
    """Parent class relating to all api data requesting and formatting"""

    def __init__(self):
        pass

    def send_request(self, url):
        print("Sending Request... ", url)
        """Method for sending http requests using passed url and returns data in wrapped in string.

        Parameters:
        - url (str): url for http requests

        Returns:
        - str: the response from the request wrapped in a string."""
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
        - dict: the string now as a dict."""
        print("Converting string to json/dict...\n")
        try:
            if string is not None:
                return json.loads(string)
            else:
                pass
        except Exception:
            return None

    def get_key(self, service_name):
        """Reads and returns the required api depending on which service is needed.

        Parameters:
        - service_name (str): the name of the service requiring the key.

        Returns:
        - str: the required api key as a string.
        - None: error has occurred."""
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
            return None

    def today_plus(self, today, days):
        """Adds given amount of days to current date.

        Parameters:
        - today (str): the current date.
        - days (int): the number of days to be added.

        Returns:
        - str: the new date
        """
        return today + datetime.timedelta(days)

    def get_next_day_from_name(self, day_name):
        """Finds date of given day name.

        Parameters:
        - day_name (str): the name of day being looked for.

        Returns:
        - str: the date relating to given day name"""
        today = datetime.date.today()
        for i in range(7):
            date = self.today_plus(today=today, days=i)
            if calendar.day_name[date.weekday()] == day_name:
                return date

    def check_if_named_day(self, day):
        """checks if a string is a day name.

        Parameters:
        - day (str): a day of the week.

        Returns:
        - bool: whether the passed string is a day name or not.
        """
        for name_of_day in calendar.day_name:
            if name_of_day == day:
                return True

    def get_specific_days(self, specific_days):
        """fetches the dates for specific day arrangements to be then used in api requests.

        Parameters:
        - specific_days (list): the days the user has requested.

        Returns:
        - list: the start date, end date and named days (e.g. monday, tuesday) based of user's request.
        """
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

            if specific_day in ("this week", "This Week", "Week", "week"):
                start_date = datetime.datetime.today()
                end_date = self.today_plus(start_date, 7)

            if specific_day in ("next week", "Next Week", "Next week"):
                start_date = self.get_next_day_from_name("monday")
                end_date = self.today_plus(start_date, 7)

        day_array = [str(start_date), str(end_date), named_days]
        return day_array

    def date_time_conversion(self, date_time):
        """Converts time format used by open metro into a format that matches visual crossing.

        Parameters:
        - date_time (str): a specific date and time in one string.

        Returns:
        - dict: a dict where the date and time are separate values."""
        date_and_time = date_time.split("T")
        return {"date": date_and_time[0], "time": date_and_time[1] + ":00"}
