from modules.Api import Api


class Geocoding(Api):
    def __init__(self):
        self.key = self.get_key("locIq")

    def reverse(self, lat, long):
        print("Getting name from lat and long...")
        url = f"https://us1.locationiq.com/v1/reverse?key={self.key}&lat={lat}&lon={long}&format=json&"
        return self.string_to_json(self.send_request(url))

    def default(self, location_name):
        print("location_name: ", location_name)
        print("Getting lat and long from name...")
        url = f"https://us1.locationiq.com/v1/search?key={self.key}&q={self.format_for_request(location_name)}&format=json&"
        response = self.string_to_json(self.send_request(url))
        print("geocoding url: ", url)
        return self.get_long_lat(response)

    def format_for_request(self, location_name):
        print("Formatting name for api request...")
        if " " in location_name:
            formatted_location = location_name.replace(" ", "%20")
        else:
            formatted_location = location_name
        formatted_location += "%20United%20Kingdom"
        return formatted_location

    def get_long_lat(self, json):
        print("Putting lat and long into array...")
        long = float(json[0]["lon"])
        lat = float(json[0]["lat"])
        value = [long, lat]
        print("latlong: ", value)
        return value
