from flask import Flask, jsonify, make_response, request


from modules.Speaker import Speaker


app = Flask(__name__)
speaker = Speaker()


@app.route("/communicate", methods=["POST", "GET"])
def communicate():
    message = request.args.get("message")
    print(f"Received message... {message}")

    name = request.args.get("name")
    print(name)

    location = request.args.get("location")
    print(location)

    response = speaker.fulfil_request(
        want_json=speaker.what_does_user_want(message, check_device_location(location)),
        user_message=message,
        name=name,
        user_location=location,
    )  # don't forget about this
    print(speaker.format_user_location(location))
    return make_response(
        jsonify(
            {"response": response},
            200,
        )
    )


def check_device_location(location):
    if location == "None":
        return False
    else:
        return True


def run_local():
    app.run(debug=True)


def run_on_network():
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    run_local()
