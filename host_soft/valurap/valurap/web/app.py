from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, send

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')

@socketio.on('hello')
def on_hello(data):
    """Create a game lobby"""
    print("hello:", data)

@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    print("connected:", data)
    emit('hello', {'bubu': 'bebe'})

socketio.run(app, host="0.0.0.0")
