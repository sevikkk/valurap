import asyncio
import pickle
import time
from collections import deque
from concurrent.futures._base import CancelledError

import aiomonitor
from aiohttp import web
import socketio
import os.path

from .printer import Valurap, ExecutionAborted, OLED

import logging

logging.basicConfig(level="INFO")

UI_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "../web/valurap-ui/dist/"))

current_state = {"X": 0, "Y": 0, "Z": 0}

current_speeds = {"X": 0, "Y": 0, "Z": 0}

prn_queue = asyncio.Queue()
prns = [None]
stopping = False

loop = asyncio.get_event_loop()
sio = socketio.AsyncServer(async_mode="aiohttp")
app = web.Application(client_max_size=100000000)
sio.attach(app)

oled = OLED()


def valurap_processing_loop():
    prn = Valurap(oled=oled)
    prns[0] = prn
    try:
        prn.setup()
        abs_safe = False
        while True:
            print("Waiting for command...")
            prn.idle = True
            fut = asyncio.run_coroutine_threadsafe(prn_queue.get(), loop)
            q = fut.result()
            prn.idle = False
            if prn.abort:
                while True:
                    try:
                        fut = asyncio.run_coroutine_threadsafe(prn_queue.get_nowait(), loop)
                        fut.result()
                    except asyncio.queues.QueueEmpty:
                        break
                break

            print("Got item:", q[0], )
            if q[0] == "exit":
                break
            elif q[0] == "home":
                prn.home()
                abs_safe = True
            elif q[0] in ("move", "moveto"):
                modes = q[1]
                deltas = q[2]
                speed = q[3]
                absolute = (q[0] == "moveto")
                print("  move", modes, deltas, speed, absolute)
                prn.move(modes=modes, speed=speed, targets=deltas, absolute=absolute)
            elif q[0] == "enable":
                modes = q[1]
                prn.enable_axes(modes)
            elif q[0] == "exec_code":
                code = q[1]
                prn.cb.reset()
                prn.cb.buffer.extend(code)
                prn.exec_code(prn.cb)
            else:
                print("Unknown command", q[0])
    except CancelledError:
        print("Cancelled")
    except ExecutionAborted:
        print("Aborted")
    finally:
        prn = Valurap(oled=oled)
        prn.setup()
        prns[0] = prn


def load_binary(layer):
    try:
        print("pickle load start")
        full_code = pickle.loads(layer)
        print("pickle load done")
    except:
        return 400, {"ok": 0, "err": "unpickle failed"}

    prn = prns[0]

    if len(prn.cb.buffer) > 0:
        print("longcode append")
        prn.cb.buffer.extend(full_code)
        print("longcode append done")
    else:
        print("queue put")
        fut = asyncio.run_coroutine_threadsafe(prn_queue.put(["exec_code", full_code]), loop)
        fut.result()
        print("queue put done")
        attempts = 10000
        while True:
            if len(prn.cb.buffer) > 0:
                break
            else:
                attempts -= 1
                if attempts < 0:
                    print("waiting for print start failed")
                    return 400, {"ok": 0, "err": "waiting for print start timed out"}

                print("waiting for print start")
                time.sleep(0.01)

    print("all done")
    return 200, {"ok": 1}


async def stop_valurap(app):
    global stopping

    stopping = True

app.on_cleanup.append(stop_valurap)

async def background_task():
    """Example of how to send server generated events to clients."""
    prn_loop = None
    while not stopping:
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

    print("exiting background task")
    prns[0].abort = True
    await prn_queue.put(["abort"])
    #await prn_loop

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

async def api(request):
    q = request.query
    print("api: {}".format(dict(request.query)))
    cmd = q["cmd"]
    result = {"ok": 1}
    status = 200
    if cmd == "home":
        await prn_queue.put(["home"])
    elif cmd == "abort":
        prns[0].abort = True
        await prn_queue.put(["abort"])
    elif cmd == "move" or cmd == "moveto":
        deltas = {}
        mode: Set[str] = set()
        if "mode" in q:
            mode = set(q["mode"].split(","))

        for axe in ["X1", "X2"]:
            if axe in q:
                deltas[axe] = float(q[axe])

        for axe in ["Y", "Z", "E1", "E2"]:
            if axe in q:
                deltas[axe] = float(q[axe])
                if not mode:
                    mode = {"print"}

                assert "print" in mode

        for axe in ["YL", "YR", "ZFR", "ZFL", "ZBR", "ZBL"]:
            if axe in q:
                deltas[axe] = float(q[axe])
                if not mode:
                    mode = {"home"}

                assert "home" in mode

        if not mode:
            mode = {"print"}

        if "E1" in deltas:
            mode.add("e1")

        if "E2" in deltas:
            mode.add("e2")

        speed = None
        if "speed" in q:
            speed = float(q["speed"])

        await prn_queue.put([cmd, list(mode), deltas, speed])

    elif cmd == "enable":
        mode = q.get("mode", "print")
        assert mode in ("print", "home")
        modes = [mode]
        axes = q.get("axes", "").lower().split(",")
        for axe in axes:
            if not axe:
                continue
            if axe not in ["e1", "e2"]:
                result = {"ok": 0, "err": "Only extruder axes can be modified"}
                break
            modes.append(axe)
        await prn_queue.put(["enable", modes])
    elif cmd == "exec_binary":
        data = await request.post()
        layer = data["code"].file.read()
        print("binary len: {} {}".format(len(layer), type(layer)))
        status, result = await loop.run_in_executor(None, load_binary, layer)
    elif cmd == "query":
        if prns[0].cb:
            buf_len = len(prns[0].cb.buffer)
        else:
            buf_len = None
        result = {
            "idle": prns[0].idle,
            "state": prns[0].hw_state,
            "buf_len": buf_len
        }
    else:
        result = {"ok": 0, "err": "unknown command"}
        status = 400

    return web.json_response(data=result, status=status)

app.router.add_get("/", index)
if 0:
    app.router.add_get("/favicon.ico", favicon)
    app.router.add_static("/js", UI_ROOT + "/js")
    app.router.add_static("/css", UI_ROOT + "/css")
app.router.add_get("/api", api)
app.router.add_post("/api", api)


with aiomonitor.start_monitor(
    loop=loop,
    host="0.0.0.0",
    port=5001,
    console_port=5002,
    locals={"app": app, "prns": prns, "prn_queue": prn_queue},
):
    web.run_app(app, port=5000, host="0.0.0.0")
