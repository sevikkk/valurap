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
    Decode a packet from a payload.
    Accepts a byte array containing a stream subset, and attempts
    to parse the packet and return the payload and rest of stream.
    @param packet byte array containing stream data
    @return payload of the packet and rest of stream
    """
    assert type(packet) is bytearray

    if len(packet) < 4:
        raise ValueError("Packet too short: %d < 4" % len(packet))

    for junk_bytes in range(0, len(packet) - 3):
        if packet[junk_bytes] != 0xD5:
            continue

        payload_len = packet[junk_bytes + 1]
        if payload_len > len(packet) - 3 - junk_bytes:
            raise ValueError("Packet too short")

        payload = packet[junk_bytes + 2:junk_bytes + 2 + payload_len]
        crc = calculate_crc(payload)
        packet_crc = packet[junk_bytes + payload_len + 2 ]
        if packet_crc != crc:
            raise ValueError("CRC mismatch: %x != %x" % (packet_crc, crc))
        else:
            return payload, packet[junk_bytes + payload_len + 3:]
    raise ValueError("Start byte not found")

