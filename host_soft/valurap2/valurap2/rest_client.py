import pickle
import time
from urllib.parse import urlencode

import requests

class Client:
    thermo_base = 'http://orange:5000/api'
    motion_base = 'http://orange2:5000/api'

    def __init__(self, emu=False):
        self.emu = emu


    def _do_api_request(self, cmd, args=None, thermo=False):
        if thermo:
            base = self.thermo_base
        else:
            base = self.motion_base

        qs = {"cmd": cmd}
        qs.update(args or {})
        url = base + "?" + urlencode(qs)

        if self.emu:
            print("url:", url)
            if cmd == "query":
                return {'idle': True, 'state': {'motors_x': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'lb': 0}, 'buf_len': 0}
            return {}

        r = requests.get(url)
        r.raise_for_status()
        return r.json()


    def home(self):
        self._do_api_request('home')

    def move(self, **args):
        self._do_api_request('move', args)

    def moveto(self, **args):
        self._do_api_request('moveto', args)

    def enable(self, **args):
        self._do_api_request('enable', args)

    def exec_binary(self, codes):
        if self.emu:
            print("send code", len(codes))
            return

        data = pickle.dumps(codes)
        r = requests.post(self.motion_base + "?cmd=exec_binary", files={"code": data})
        r.raise_for_status()
        return r


    def abort(self):
        self._do_api_request('abort')

    def state(self):
        return self._do_api_request('query')

    def wait_idle(self, timeout=None):
        if self.emu:
            return {'idle': True, 'state': {'motors_x': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'lb': 0}, 'buf_len': 0}

        t0 = time.time()
        while True:
            r = self._do_api_request('query')
            if r["idle"]:
                break
            if timeout and time.time() - t0 > timeout:
                raise TimeoutError()
            time.sleep(0.1)

        return r

    def thermo_state(self):
        return self._do_api_request('q', thermo=True)

    def sfv(self, ch, val):
        return self._do_api_request('sfv', {"ch":  ch, "val": val}, thermo=True)

    def spt(self, ch, val):
        return self._do_api_request('spt', {"ch":  ch, "val": val}, thermo=True)

    def spp(self, ch, p, i):
        return self._do_api_request('spp', {"ch":  ch, "p": p, "i": i}, thermo=True)



