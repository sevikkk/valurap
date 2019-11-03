import time

import random
import serial
import struct

from valurap.packet import encode_payload, decode_packet


class S3GPortBase(object):
    def __init__(self, port='/dev/ttyS1', baudrate=115200):
        self.port = self.open_port(port, baudrate)
        self.data = bytearray()
        self.unexpected_packets = []

    def open_port(self, port, baudrate):
        return serial.Serial(port, baudrate=baudrate, timeout=0.1)

    def unexpected_packet(self, packet):
        print("Unexpected packet: {}".format(repr(packet)))
        self.unexpected_packets.append(packet)

    def send_and_wait_reply(self, payload, cmd_id=None, timeout=1, retries=3):
        if cmd_id is None:
            cmd_id = random.randint(1000, 65000)
        buf = encode_payload(struct.pack("H", cmd_id) + payload)

        while retries:
            self.port.write(buf)
            self.port.flush()

            try:
                packet = self.wait_reply(cmd_id, timeout)
            except TimeoutError:
                retries -= 1
                if not retries:
                    raise
            else:
                break

        return packet[2:]

    def wait_reply(self, cmd_id=None, timeout=1):
        packet = bytearray()
        got_packet = False
        start_time = time.time()
        while not got_packet:
            if time.time() - start_time > timeout:
                raise TimeoutError

            reply = self.port.read()
            self.data += reply
            try:
                packet, rest = decode_packet(self.data)
            except ValueError:
                continue

            self.data = rest
            reply_cmd_id = struct.unpack("H", packet[:2])[0]
            if (cmd_id is None) or (cmd_id == reply_cmd_id):
                got_packet = True
            else:
                self.unexpected_packet(packet)
        return packet