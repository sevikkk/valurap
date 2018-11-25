from .crc8 import calculate_crc

def encode_payload(payload):
    """
    Encode passed payload into a packet.
    @param payload Command payload, 1 - n bytes describing the command to send
    @return bytearray containing the packet
    """
    if len(payload) > 255:
        raise ValueError("Packet too long: %d > 255" % (len(payload), ))

    packet = bytearray()
    packet.append(0xD5)
    packet.append(len(payload))
    packet.extend(payload)
    packet.append(calculate_crc(payload))

    return packet


def decode_packet(packet):
    """
    Decode a packet from a payload.Non-streaming packet decoder.
    Accepts a byte array containing a single packet, and attempts
    to parse the packet and return the payload.
    @param packet byte array containing the input packet
    @return payload of the packet
    """
    assert type(packet) is bytearray

    if len(packet) < 4:
        raise ValueError("Packet too short: %d < 4" % len(packet))

    if packet[0] != 0xD5:
        raise ValueError("Wrong Header: %x != 0xD5" % (packet[0], ))

    if packet[1] != len(packet) - 3:
        raise ValueError("Length mismatch: %d != %d" % (packet[1], len(packet) - 3))

    crc = calculate_crc(packet[2:(len(packet) - 1)])
    if packet[len(packet) - 1] != crc:
        raise ValueError("CRC mismatch: %x != %x" % (packet[len(packet) - 1], crc))

    return packet[2:(len(packet) - 1)]


class PacketStreamDecoder(object):

    """
    A state machine that accepts bytes from an s3g packet stream, checks the validity of
    each packet, then extracts and returns the payload.
    """
    def __init__(self):
        """
        Initialize the packet decoder
        """
        self.state = 'WAIT_FOR_HEADER'
        self.payload = bytearray()
        self.expected_length = 0

    def parse_byte(self, byte):
        """
        Entry point, call for each byte added to the stream.
        @param byte Byte to add to the stream
        """

        if self.state == 'WAIT_FOR_HEADER':
            if byte != 0xD5:
                raise ValueError("Header mismatch: %x != 0xD5" % (byte))

            self.state = 'WAIT_FOR_LENGTH'

        elif self.state == 'WAIT_FOR_LENGTH':
            self.expected_length = byte
            self.state = 'WAIT_FOR_DATA'

        elif self.state == 'WAIT_FOR_DATA':
            self.payload.append(byte)
            if len(self.payload) == self.expected_length:
                self.state = 'WAIT_FOR_CRC'

        elif self.state == 'WAIT_FOR_CRC':
            crc = calculate_crc(self.payload)
            if crc != byte:
                raise ValueError("CRC mismatch: %x != %x" % (crc, byte))

            self.state = 'PAYLOAD_READY'

        else:
            raise ValueError('Parser in bad state: too much data provided?')
