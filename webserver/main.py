from flask import Flask, jsonify, make_response, request


from modules.Speaker import Speaker


app = Flask(__name__)
speaker = Speaker()


@app.route("/communicate", methods=["POST", "GET"])
def communicate():
    message = request.args.get("message")
    print(message)

    name = request.args.get("name")

    speaker.fulfil_request(
        speaker.what_does_user_want(message)
    )  # don't forget about this
    return make_response(
        jsonify(
            {"response": "ok"},
            200,
        )
    )


def run_local():
    app.run(debug=True)


def run_on_network():
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    run_local()
