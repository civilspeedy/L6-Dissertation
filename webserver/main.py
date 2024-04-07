from email import message
import json
from flask import Flask, jsonify, make_response, request

from modules.Geocoding import Geocoding
from modules.Speaker import Speaker
from modules.Weather import Open_Metro, Visual_Crossing

app = Flask(__name__)
speaker = Speaker()
vc = Visual_Crossing()
om = Open_Metro()
locIq = Geocoding()

name = " "


@app.route("/communicate", methods=["POST", "GET"])
def communicate():
    message = request.args.get("message")
    print(message)

    name = request.args.get("name")
    print(name)

    return make_response(
        jsonify(
            {
                "response": speaker.basic_conversation(
                    user_name=name, user_message=message
                )
            },
            200,
        )
    )


def run_local():
    app.run(debug=True)


def run_on_network():
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    run_local()
