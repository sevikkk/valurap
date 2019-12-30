import asyncio

import aiomonitor
from aiohttp import web
import socketio
import os.path

from ..printer import Valurap, ExecutionAborted

UI_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "../web/valurap-ui/dist/"))

loop = asyncio.get_event_loop()

sio = socketio.AsyncServer(async_mode="aiohttp")
app = web.Application(loop=loop)
sio.attach(app)

current_state = {"X": 0, "Y": 0, "Z": 0}

current_speeds = {"X": 0, "Y": 0, "Z": 0}

prn_queue = asyncio.Queue()
prns = [None]

def valurap_processing_loop():
    prn = Valurap()
    prns[0] = prn
    prn.setup()
    try:
        while True:
            print("Waiting for command...")
            fut = asyncio.run_coroutine_threadsafe(prn_queue.get(), loop)
            q = fut.result()
            if prn.abort:
                while True:
                    fut = asyncio.run_coroutine_threadsafe(prn_queue.get_nowait(), loop)
                    try:
                        fut.result()
                    except asyncio.QueueEmpty:
                        break
                break

            print("Got item:", q)
            if q[0] == "exit":
                break
            elif q[0] == "home":
                prn.home()
    except ExecutionAborted:
        print("Aborted")
    finally:
        prn = Valurap()
        prns[0] = prn
        prn.setup()


async def background_task():
    """Example of how to send server generated events to clients."""
    prn_loop = None
    while True:
        if prn_loop is None:
            prn_loop = loop.run_in_executor(None, valurap_processing_loop)
        elif prn_loop.done():
            print("prn_loop done")
            try:
                print(prn_loop.result())
            except Exception as e:
                print("prn_loop exception", e)
                import traceback
                traceback.print_exc()

            prn_loop = None
            continue

        need_update = False
        for k, v in current_speeds.items():
            if v != 0:
                current_state[k] += v
                need_update = True

        if need_update:
            await sio.emit("cur_state", current_state)

        await sio.sleep(0.2)


sio.start_background_task(background_task)


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
    elif data == "abort" or  data == "start-abort":
        prns[0].abort = True
        await prn_queue.put(["abort"])
    elif data == "start-home":
        await prn_queue.put(["home"])

    await sio.emit("cur_state", current_state)


@sio.event
async def connect(sid, environ):
    await sio.emit("cur_state", current_state, room=sid)


@sio.event
def disconnect(sid):
    print("Client disconnected")


async def index(request):
    with open(UI_ROOT + "/index.html") as f:
        return web.Response(text=f.read(), content_type="text/html")


async def favicon(request):
    with open(UI_ROOT + "/favicon.ico", "rb") as f:
        return web.Response(body=f.read(), content_type="image/vnd.microsoft.icon")


app.router.add_get("/", index)
app.router.add_get("/favicon.ico", favicon)
app.router.add_static("/js", UI_ROOT + "/js")
app.router.add_static("/css", UI_ROOT + "/css")


with aiomonitor.start_monitor(
    loop=loop,
    host="0.0.0.0",
    port=5001,
    console_port=5002,
    locals={"app": app, "prns": prns, "prn_queue": prn_queue},
):
    web.run_app(app, port=5000, host="0.0.0.0")
