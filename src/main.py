from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('generate')
def handle_message(data):
    print('received message:', data)

if __name__ == '__main__':
    socketio.run(app)