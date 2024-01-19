from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html')

@socketio.event
def send_data_request(message):
    print(message)
    emit('data', {'data': 'got it!'})

if __name__ == '__main__':
    socketio.run(app)