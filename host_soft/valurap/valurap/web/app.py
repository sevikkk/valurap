import time

from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, send

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)

current_state = {
    "X": 0,
    "Y": 0,
    "Z": 0,
}

current_speeds = {
    "X": 0,
    "Y": 0,
    "Z": 0,
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
    elif data == "start-up":
        current_speeds["Y"] = 1
    elif data == "start-down":
        current_speeds["Y"] = 1
    elif data == "start-left":
        current_speeds["X"] = 1
    elif data == "start-right":
        current_speeds["X"] = 1
    elif data == "stop-up":
        current_speeds["Y"] = 0
    elif data == "stop-down":
        current_speeds["Y"] = 0
    elif data == "stop-left":
        current_speeds["X"] = 0
    elif data == "stop-right":
        current_speeds["X"] = 0

    emit('cur_state', current_state, broadcast=True)

import threading

class Incrementer(threading.Thread):
    def run(self):
        while True:
            need_update = False
            for k,v in current_speeds.items():
                if v != 0:
                    current_state[k] += v
                    need_update = True

            if need_update:
                socketio.emit('cur_state', current_state, broadcast=True)

            time.sleep(0.2)

t = Incrementer()
t.setDaemon(True)
t.start()

socketio.run(app, host="0.0.0.0")
