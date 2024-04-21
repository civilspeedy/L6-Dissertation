from modules.Api import Api


class Open_Metro(Api):
    """A class that inherits from Api, for the specific methods around the Open Metro weather api."""

    def __init__(self):
        super().__init__()
        self.report = None

    def request_forecast(self, long, lat, what_user_wants, start_date, end_date):
        """Requests weather information from Open Metro based on the user's input.

        Parameters:
        - long (float): longitude value relating to the user's request.
        - lat (float): latitude value relating to the user's request.
        - what_user_wants (dict): a dict contain bool values for the type of information the
        user would like.
        - start_date (str): the date in which the user would like information to start from.
        - end_date (str): the date the user would like the information to end on.

        Returns:
        - self.report (dict): a json containing all relevant weather information.
        """

        print("Requesting forecast from open metro...\n")

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly={self.create_info_string(what_user_wants)}&start_date={start_date}&end_date={end_date}"

        self.report = self.string_to_json(self.send_request(url))
        return self.report

    def create_info_string(self, what_user_wants):
        """creates a string that outlines what information is wanted to be fetched in api call to open metro.

        Parameters:
        - what_user_wants (dict): a dict contain bool values for the type of information the user would like.

        Returns:
        - info_string (str): a string formatting what info is need for url.
        """

        info_string = ""

        for x in what_user_wants:
            match x:
                case "general_weather_request":
                    info_string = "temperature_2m,weather_code"
                    break
                case "top_temperature":
                    info_string += "temperature_2m_max,"
                case "lowest_temperature":
                    info_string += "temperature_2m_min,"
                case "temperature_avg":
                    info_string += "temperature_2m,"
                case "feels_like_temperature":
                    info_string += "apparent_temperature,"
                case "wind_speed":
                    info_string += "wind_speed_10m,"
                case "uv_index":
                    info_string += "uv_index,"
                case "rain":
                    info_string += "rain,"
                case "cloud_coverage":
                    info_string += "cloud_cover,"
                case "visibility":
                    info_string += "visibility,"

        if info_string[-1] == ",":
            info_string = info_string[:-1]

        return info_string

    def get_date_time(self):
        """Gets all datetimes relating to weather information and returns in list.

        Returns:
        - date_times (list): a list of dates and times that that a weather report contains.
        """

        print("Getting datetimes...\n")
        date_times = []
        if self.report is not None:
            for date_time in self.report["hourly"]["time"]:
                date_times.append(date_time)
        return date_times

    def get_value(self, datetime, key):
        """Returns a specific weather information value from report.

        Parameters:
        - datetime (str): the date and time of the information being requested
        - key (str): the key relating to the specific type of information being requested.

        Returns:
        - Any: a specific value fetched from report dict
        """
        print("Getting specific value...\n")

        if self.report is not None:
            if self.report["hourly"] is not None:
                time = self.report["hourly"]["time"]
                print(time)
                for i in range(len(time)):
                    print(time[i], datetime)
                    if time[i] == datetime:
                        return self.report["hourly"][key][i]


class Visual_Crossing(Api):
    """A class inheriting from Api, for weather request specific to Visual Crossing's api.
    Visual crossing is not the primary source for weather information but as a alternative source for more reliable reports.
    """

    def __init__(
        self,
    ):
        super().__init__()
        self.key = self.get_key("vc")
        self.report = None

    def request_forecast(self, start_date, end_date, location):
        """Sends http request to Visual Crossing's api service for weather information based on user's
        provided start date, end date and location. Updates self.report.

        Parameters:
        - start_date (str): the date in which the user would like information to start from.
        - end_date (str): the date the user would like the information to end on.
        - location (str): the name of the user's provided location.
        """
        print("Requesting forecast from visual crossing...\n")
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&key={self.key}&contentType=json"

        response = self.send_request(url)
        report = str(response).replace('\\"', '"')

        self.report = self.string_to_json(report)

    def search_report(self, search_item, date, time):
        """For searching a specific item in the report.

        Parameters:
        - search_item (str): the type of information to be fetched.
        - date (str): the date the specific information needs to relate to.
        - time (str): the time the specific information needs to relate to.

        Returns:
        - Any: If the specific information is found it is returned .
        - False: If the specific information is not found False is returned.
        """
        print("Searching for specific item...")
        if self.report is not None:
            key = self.define_key(search_item)

            if key != "":
                days = self.report["days"]
                for day in days:
                    if day["datetime"] == date:
                        for time_slot in day["hours"]:
                            if time_slot["datetime"] == time:
                                return time_slot[key]
        return False

    def define_key(self, search_item):
        """Translates the keys from Open Metro reports to match that of the keys found in Visual Crossing's reports.

        Parameters:
        - search_item (str): the specific information being searched for referenced as a key from Open Metro.

        Returns:
        - key (str): the key that will find the corresponding value in a Visual Crossing report.
        """
        key = ""

        match search_item:
            case "temperature_2m":
                key = "temp"
            case "apparent_temperature":
                key = "feelslike"
            case "wind_speed_10m":
                key = "windspeed"
            case "uv_index":
                key = "uvindex"
            case "rain":
                key = "precip"
            case "cloud_cover":
                key = "cloudcover"
            case "visibility":
                key = "visibility"

        return key
