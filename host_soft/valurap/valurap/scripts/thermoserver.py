import asyncio
from concurrent.futures._base import CancelledError

from aiohttp import web
import os.path

from ..thermocontrol import ThermoC

app = web.Application()
tc = ThermoC()

async def index(request):
    return web.Response(text="hello", content_type="text/html")


async def api(request):
    print(request.query)
    cmd = request.query.get("cmd")
    print(f"cmd: {cmd}")
    if cmd == "q":
        q = tc.S3G_QUERY()
        print(f"q: {q}")
        reply = q._asdict()
    elif cmd == "spt":
        ch = int(request.query.get("ch"))
        val = int(request.query.get("val"))
        assert ch >= 1 and ch <= 3
        assert val >= 0
        tc.S3G_SET_PID_TARGET(ch, val)
        reply = {"ok": 1}
    elif cmd == "sfv":
        ch = int(request.query.get("ch"))
        val = int(request.query.get("val"))
        assert ch>=1 and ch <= 3
        assert val>=0 and val <= 1000

        tc.S3G_SET_FAN_VALUE(ch, val)
        reply = {"ok": 1}
    elif cmd == "spp":
        ch = int(request.query.get("ch"))
        k_p = int(request.query.get("p"))
        k_i = int(request.query.get("i"))
        assert ch >= 1 and ch <= 3

        tc.S3G_SET_PID_PARAMS(ch, k_p, k_i)
        reply = {"ok": 1}
    else:
        reply = {"error": "unqnown command"}

    return web.json_response(reply)


app.router.add_get("/", index)
app.router.add_get("/api", api)

if __name__ == "__main__":
    web.run_app(app, port=5000, host="0.0.0.0")
