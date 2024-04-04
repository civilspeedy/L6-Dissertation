from flask import Flask, jsonify, make_response, request
from modules.Speaker import Speaker

app = Flask(__name__)


@app.route("/")
def hello():
    # authorisation needs to be set up
    print("Someone has connected")
    return "Test Message"


@app.route("/api/userMessage", methods=["GET", "POST"])
def user_message():
    string = request.args.get("message")
    print(string)
    if string == "":
        return make_response(jsonify({"result": "no input"}, 400))
    return make_response(jsonify({"result": "ok"}, 200))


def run_local():
    app.run(debug=True)


def run_on_network():
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    pass
