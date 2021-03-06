import asyncio
import pickle
import time
from collections import deque
from concurrent.futures._base import CancelledError

import aiomonitor
from aiohttp import web
import socketio
import os.path

from .. import asg
from ..printer import Valurap, ExecutionAborted, OLED

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
                prn.abs_safe = True
                prn.update_axes_positions()
            elif q[0] == "move":
                deltas = q[1]
                prn.move(**deltas)
                prn.update_axes_positions()
            elif q[0] == "moveto":
                pos = q[1]
                if prn.abs_safe:
                    prn.moveto(**pos)
                    prn.update_axes_positions()
                else:
                    print("Moveto in not abs_safe state, aborting")
                    prn.abort()
            elif q[0] == "enable":
                axes = q[1]
                for k,v in axes.items():
                    prn.axes[k].enabled = v
                prn.update_axes_config()
            elif q[0] == "exec_code":
                prn.abs_safe = False
                code = q[1]
                prn.exec_long_code(code, splits=1000, low_buf=2500, verbose=True)
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

def load_layer(layer):
    try:
        print("pickle load start")
        p = pickle.loads(layer)
        print("pickle load done")
    except:
        return 400, {"ok": 0, "err": "unpickle failed"}

    prn = prns[0]

    codes = []
    ok = 0
    for pp in p:
        if pp[0] != "segment":
            continue

        ok = 1

        cmd, meta, segments = pp
        if "map" in meta:
            if meta["map"]:
                codes.append(prn.asg.gen_map_code(meta["map"]))

        pr_opt = []

        apgs = {
            "X": prn.apg_x,
            "Y": prn.apg_y,
            "Z": prn.apg_z,
        }

        print("load segments")
        i = 0
        for dt, segs in segments:
            pr_opt.append([
                dt, [asg.ProfileSegment.from_tuple(s, apgs) for s in segs]
            ])
            i += 1
            if i > 100:
                time.sleep(0.001)
                i = 0

        print("gen code")
        path_code = prn.asg.gen_path_code(pr_opt,
                                          accel_step=50000000/meta["acc_step"],
                                          real_apgs=apgs)
        print(len(path_code))
        codes.append(path_code)
        time.sleep(0.001)

    print("load done")
    if not ok:
        return 400, {"ok": 0, "err": "no segment chunk found"}

    if prn.long_code and len(prn.long_code) > 100:
        print("longcode append")
        full_code = []
        for code in codes:
            full_code.extend(code[:-1])
        prn.long_code.extend(full_code)
        print("longcode append done")
    else:
        print("formaat command")
        full_code = deque()
        for code in codes:
            full_code.extend(code[:-1])
        print("queue put")
        fut = asyncio.run_coroutine_threadsafe(prn_queue.put(["exec_code", full_code]), loop)
        fut.result()
        print("queue put done")
        attempts = 10000
        while True:
            if prn.long_code and len(prn.long_code) > 0:
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

def load_binary(layer):
    try:
        print("pickle load start")
        full_code = pickle.loads(layer)
        print("pickle load done")
    except:
        return 400, {"ok": 0, "err": "unpickle failed"}

    prn = prns[0]

    if prn.long_code and len(prn.long_code) > 100:
        print("longcode append")
        prn.long_code.extend(full_code)
        print("longcode append done")
    else:
        print("format command")
        long_code = deque()
        long_code.extend(full_code)
        print("queue put")
        fut = asyncio.run_coroutine_threadsafe(prn_queue.put(["exec_code", long_code]), loop)
        fut.result()
        print("queue put done")
        attempts = 10000
        while True:
            if prn.long_code and len(prn.long_code) > 0:
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
        for axe in prns[0].axes.keys():
            if axe in q:
                deltas[axe] = float(q[axe])

        if cmd == "moveto":
            if prns[0].abs_safe:
                await prn_queue.put(["moveto", deltas])
            else:
                result = {"ok": 0, "err": "printer absolute position is uncertain"}
                status = 400
        else:
            await prn_queue.put(["move", deltas])
    elif cmd == "enable":
        states = {"E1": False, "E2": False}
        axes = q["axes"].split(",")
        for axe in axes:
            if axe not in states.keys():
                result = {"ok": 0, "err": "Only extruder axes can be modified"}
                states = {}
                break
            states[axe] = 1
        if states:
            await prn_queue.put(["enable", states])
    elif cmd == "exec_code":
        data = await request.post()
        layer = data["code"].file.read()
        print("code len: {} {}".format(len(layer), type(layer)))
        status, result = await loop.run_in_executor(None, load_layer, layer)
    elif cmd == "exec_binary":
        data = await request.post()
        layer = data["code"].file.read()
        print("binary len: {} {}".format(len(layer), type(layer)))
        status, result = await loop.run_in_executor(None, load_binary, layer)
    elif cmd == "query":
        result = {
            "idle": prns[0].idle,
            "state": prns[0].hw_state,
            "abs_safe": prns[0].abs_safe
        }
    else:
        result = {"ok": 0, "err": "unknown command"}
        status = 400

    return web.json_response(data=result, status=status)

app.router.add_get("/", index)
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
