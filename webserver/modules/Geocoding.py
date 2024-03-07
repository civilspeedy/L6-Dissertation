from modules.Api import Api


class Geocoding(Api):
    def __init__(self):
        self.key = self.get_key("locIq")

    def reverse(self, lat, long):
        url = f"https://us1.locationiq.com/v1/reverse?key={self.key}&lat={lat}&lon={long}&format=json&"
        return self.string_to_json(self.send_request(url))

    def defualt(self, location_name):
        url = f"https://us1.locationiq.com/v1/search?key={self.key}&q={self.format_for_request(location_name)}&format=json&"
        return self.get_long_lat(self.string_to_json(self.send_request(url)))

    def format_for_request(self, location_name):
        return location_name.replace(" ", "%20")

    def get_long_lat(self, json):
        long = float(json[0]["lon"])
        lat = float(json[0]["lat"])
        return [long, lat]
