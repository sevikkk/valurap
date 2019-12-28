from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, send

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)

current_state = {
    "X": 0,
    "Y": 0,
    "Z": 0
}

@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')

@socketio.on('send_command')
def on_send_command(data):
    print("got_command:", data)
    if data == "up":
        current_state["Y"] += 1
    elif data == "down":
        current_state["Y"] -= 1
    elif data == "left":
        current_state["X"] -= 1
    elif data == "right":
        current_state["X"] += 1

    emit('cur_state', current_state)

socketio.run(app, host="0.0.0.0")
