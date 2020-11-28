import struct

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

    def S3G_WRITE_FIFO(self, *values, **kw):
        """
        Write data to buf_executor memory
        """

        if len(values) == 1 and isinstance(values[0], CommandBuffer):
            data = bytearray().join(values[0].buffer)
        else:
            data = bytearray().join(values)

        l = len(data)
        if l % 5 != 0:
            raise ValueError("Buffer length is not multiple of 5")

        l = l / 5
        while data:
            if l < 40:
                packet_data = data
                data = None
            else:
                packet_data = data[: 40 * 5]
                data = data[40 * 5 :]

            packet_cmds = int(len(packet_data) / 5)
            payload = struct.pack("<BB", 66, packet_cmds) + packet_data
            #s = []
            #for ch in payload:
            #    s.append("%02X" % ch)
            #print("".join(s))

            # print(`payload`)
            reply = self.send_and_wait_reply(payload, kw.get("cmd_id", None), timeout=0.1)
            if reply[0] != 0x81:
                raise RuntimeError("Unexpected reply code")
        return

