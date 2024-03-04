from flask import Flask, jsonify, make_response, request
from modules.Geocoding import Geocoding


from modules.weather import Open_Metro, Visual_Crossing

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


if __name__ == '__main__':
    vc = Visual_Crossing()
    om = Open_Metro()
    om.write_to_json(om.request_forecast(1), "om")
