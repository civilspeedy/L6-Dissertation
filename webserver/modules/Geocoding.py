from modules.Api import Api


class Geocoding(Api):
    """A class that inherits from Api to carry out geocoding related functionality and api calls."""
    def __init__(self):
        self.key = self.get_key("locIq")

    def reverse(self, lat, long):
        """Returns the name or address of a location based of a provided latitude and longitude.
        
        Parameters:
        - lat (float): provided latitude.
        - long (float): provided longitude.
        
        Returns:
        - dict: a dict containing the address of the provided long and lat.
        """
        print("Getting name from lat and long...")
        url = f"https://us1.locationiq.com/v1/reverse?key={self.key}&lat={lat}&lon={long}&format=json&"
        return self.string_to_json(self.send_request(url))

    def default(self, location_name):
        """Returns the longitude and latitude of a provided location name.

        Parameters:
        - location_name (str): a string of the location name trying to be found.

        Returns:
        - list: a list containing the longitude and latitude relating to location name
        """
        print("Getting lat and long from name...")
        url = f"https://us1.locationiq.com/v1/search?key={self.key}&q={self.format_for_request(location_name)}&format=json&"
        response = self.string_to_json(self.send_request(url))
        return self.get_long_lat(response)

    def format_for_request(self, location_name):
        """Formats a location name so that it can be used in a request for geocoding.
        
        Parameters:
        - location_name (str): the name of a location to be found.
        
        Returns:
        - formatted_location (str): the location name formatted correctly for the api request."""
        print("Formatting name for api request...")
        if " " in location_name:
            formatted_location = location_name.replace(" ", "%20")
        else:
            formatted_location = location_name
        formatted_location += "%20United%20Kingdom"
        return formatted_location

    def get_long_lat(self, json):
        """Isolates the long and lat values from return json from geocoding api.
        
        Parameters:
        -json (dict): the json return from LocationIq's api service
        
        Returns:
        - value (list): a list containing the long and lat values."""
        print("Putting lat and long into array...")
        long = float(json[0]["lon"])
        lat = float(json[0]["lat"])
        value = [long, lat]
        return value
