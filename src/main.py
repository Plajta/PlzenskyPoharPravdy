from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os
import requests

#variables
nuke_config_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/other_data/nuke_config.json"


app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    #loading nukes
    nukes = []
    nuke_config = open(nuke_config_path)
    nuke_config_data = json.load(nuke_config)
    for nuke in nuke_config_data["nukes"]:
        nukes.append({
            "name": nuke["name"],
            "energy": str(nuke["energy"]) + "kt",
            "value": nuke["name"].replace(" ", "")
        })

    print(nukes)
    return render_template('index.html', nuke_data=nukes)

@socketio.on('generate')
def handle_generate(data):
    print('received message:', data)


@socketio.on('nukede')
def handle_nukede(data):
    print('received nukede message:', data)
    latitude = data["lat"]
    longitude = data["lng"]
    choosed_nuke = data["choosed_nuke"]
    x = requests.get("https://api.mapy.cz/v1/rgeocodeurl",
                     params={"lon": longitude, "lat": latitude},
                     headers={"accept": "application/json",
                              "X-Mapy-Api-Key": "YmWIzXtT9Xx5rhFEc2rLnY8ymxWHpAW5D2pGf3P1QlA"})

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)