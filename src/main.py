from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os

#variables
nuke_config_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/other_data/nuke_config.json"
nukes = []

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    #loading nukes
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
    latitude = data["lat"]
    longitude = data["lng"]
    choosed_nuke = data["choosed_nuke"]
    

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)