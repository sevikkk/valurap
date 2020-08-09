from collections import namedtuple

import struct

from .s3g import S3GPortBase

class ThermoC(S3GPortBase):
    default_port = '/dev/ttyS2'
    default_baudrate = 115200

    def S3G_PING(self, value=0, cmd_id=None):
        """
        Send strobe
        """
        payload = struct.pack('<BI', 0, value)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        value = struct.unpack("<I", reply[1:5])[0]
        return value

    t_query_reply = namedtuple(
        "t_query_reply",
        "k_type adc1 adc2 adc3 ext1 ext2 ext3 target1 target2 target3 temp1 temp2 temp3 fan1 fan2 fan3")

    def S3G_QUERY(self, cmd_id=None):
        """
        Send strobe
        """
        payload = struct.pack('<B', 1)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        value = self.t_query_reply(*struct.unpack("<HHHHHHHHHHHHHHHH", reply[1:]))
        return value

    def S3G_SET_PID_TARGET(self, channel, target, cmd_id=None):
        """
        Send strobe
        """
        payload = struct.pack('<BBH', 2, channel, target)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_SET_PID_PARAMS(self, channel, k_p, k_i, cmd_id=None):
        """
        Send strobe
        """
        payload = struct.pack('<BBHH', 3, channel, k_p, k_i)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

    def S3G_SET_FAN_VALUE(self, channel, target, cmd_id=None):
        """
        Send strobe
        """
        payload = struct.pack('<BBH', 4, channel, target)

        reply = self.send_and_wait_reply(payload, cmd_id)
        if reply[0] != 0x81:
            raise RuntimeError("Unexpected reply code")
        return

