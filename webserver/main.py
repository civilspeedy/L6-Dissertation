import os
from flask import Flask, jsonify, make_response, request
from modules.Geocoding import Geocoding
import csv

from modules.weather import Visual_Crossing

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Test Message'


@app.route('/api/userMessage', methods=["GET", "POST"])
def user_message():
    string = request.args.get("string")
    print(string)
    if string == '':
        return make_response(jsonify({"result": "no input"}, 400))
    return make_response(jsonify({"result": "ok"}, 200))


class Csv_manipulator:
    def __init__(self):
        pass

    def get_location(self, type):
        match type:
            case "weather":
                return "./data/weather.csv"
        return ''

    def store_to_csv(self, type, to_be_written):
        location = self.get_location(type)
        try:
            # https://docs.python.org/3/library/csv.html
            with open(location, "a", newline="") as file:
                write_now = csv.writer(
                    file, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL)
                write_now.writerow([to_be_written])
            print(f"Success, file {location} has been written to.")
        except Exception as e:
            print(f"Err in store_to_csv: {e}, failed to write to file.")

    def remove_csv(self, type):
        os.remove(self.get_location(type))


if __name__ == '__main__':
    vc = Visual_Crossing()
    vc.write_to_json(vc.request_forecast(1), "vc")
