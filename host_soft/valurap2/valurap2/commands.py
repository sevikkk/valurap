import struct
from collections import deque

from valurap2.buf_commands import CommandBuffer

from valurap.s3g import S3GPortBase

class S3GPort(S3GPortBase):
    default_baudrate = 1500000

    def S3G_OUTPUT(self, reg, value, cmd_id=None):
        """
        Set output to value
        """
        if value > 2 ** 31:
            value = value - 2 ** 32

        payload = struct.pack("<BBi", 60, reg, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_INPUT(self, reg, cmd_id=None):
        """
        Get value of input
        @return value
        """
        payload = struct.pack("<BB", 61, reg)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81 or len(reply) != 5:
            raise RuntimeError("Unexpected reply")
        value = struct.unpack("<i", reply[1:5])[0]
        return value

    def S3G_STB(self, value, cmd_id=None):
        """
        Send strobe
        """
        payload = struct.pack("<BI", 62, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_CLEAR(self, value, cmd_id=None):
        """
        Clear pending interrupt
        """
        payload = struct.pack("<BI", 63, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_MASK(self, value, cmd_id=None):
        """
        Mask interrupts
        """
        payload = struct.pack("<BI", 64, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    # noinspection PyUnreachableCode
    def S3G_WRITE_FIFO(self, *values, timeout=5, max_cmds=None, cmd_id=None, until_free=None):
        """
        Write data to buf_executor memory
        """

        if len(values) == 1 and isinstance(values[0], CommandBuffer):
            data = values[0].buffer
        else:
            data = deque(values)

        free_space, status = None, None
        while data:
            l = min(40, len(data))

            if max_cmds is not None:
                l = min(l, max_cmds)
                max_cmds -= l

            if l == 0:
                break

            packet_data = bytearray().join([data.popleft() for _ in range(l)])
            assert len(packet_data) == l * 5

            payload = struct.pack("<BB", 66, l) + packet_data

            reply = self.send_and_wait_reply(payload, cmd_id=cmd_id, timeout=timeout)
            if reply[0] != 0x81:
                raise RuntimeError("Unexpected reply code: {}".format(reply[0]))
            free_space, status = struct.unpack("<ii", reply[1:9])
            if until_free is not None:
                if free_space < until_free:
                    break

        return free_space, status

