from email import message
from flask import Flask, jsonify, make_response, request

from modules.Geocoding import Geocoding
from modules.Speaker import Speaker
from modules.Weather import Open_Metro, Visual_Crossing

app = Flask(__name__)
speaker = Speaker()
vc = Visual_Crossing()
om = Open_Metro()
locIq = Geocoding()


@app.route("/")
def hello():
    # authorisation needs to be set up
    print("Someone has connected")
    return "Test Message"


# @app.route("/api/userMessage", methods=["GET", "POST"])
def user_message():
    # string = request.args.get("message")

    intent = speaker.gainIntent(message)
    location_longLat = locIq.default(intent["location"])

    vc_report = vc.request_forecast(
        intent["start_date"], intent["end_date"], intent["location"]
    )
    print(vc_report)

    # if string == "":
    # return make_response(jsonify({"result": "no input"}, 400))
    # return make_response(jsonify({"result": "ok"}, 200))


def run_local():
    app.run(debug=True)


def run_on_network():
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    user_message()
