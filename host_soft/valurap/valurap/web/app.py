import asyncio

from aiohttp import web

import socketio

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

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

async def background_task():
    """Example of how to send server generated events to clients."""
    while True:
        need_update = False
        for k,v in current_speeds.items():
            if v != 0:
                current_state[k] += v
                need_update = True

        if need_update:
            await sio.emit('cur_state', current_state)

        await sio.sleep(0.2)

async def index(request):
    with open('valurap-ui/dist/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def favicon(request):
    with open('valurap-ui/dist/favicon.ico', 'rb') as f:
        return web.Response(body=f.read(), content_type='image/vnd.microsoft.icon')

@sio.event
async def leave(sid, message):
    sio.leave_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Left room: ' + message['room']},
                   room=sid)


@sio.event
async def send_command(sid, data):
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
        current_speeds["Y"] = -1
    elif data == "start-left":
        current_speeds["X"] = -1
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

    await sio.emit('cur_state', current_state)

@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.event
async def connect(sid, environ):
    await sio.emit('cur_state', current_state, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')


app.router.add_get('/', index)
app.router.add_get('/favicon.ico', favicon)
app.router.add_static('/js', 'valurap-ui/dist/js')
app.router.add_static('/css', 'valurap-ui/dist/css')
app.router.add_static('/static', 'static')


if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app, host='0.0.0.0', port=5000)

