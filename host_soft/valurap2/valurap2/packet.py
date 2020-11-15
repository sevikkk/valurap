def calculate_crc(data):
    """
    Calculate the iButton/Maxim crc for a give bytearray
    @param data bytearray of data to calculate a CRC for
    @return Single byte CRC calculated from the data.
    """
    # CRC table from http://forum.sparkfun.com/viewtopic.php?p=51145
    crctab = [
        0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
        157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
        35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
        190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
        70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
        219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
        101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
        248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
        140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
        17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
        175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
        50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
        202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
        87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
        233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
        116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53
    ]

    data_bytes = bytearray(data)

    val = 0
    for x in data_bytes:
        val = crctab[val ^ x]
    return val


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
        packet_crc = packet[junk_bytes + payload_len + 2]
        if packet_crc != crc:
            raise ValueError("CRC mismatch: %x != %x" % (packet_crc, crc))
        else:
            return payload, packet[junk_bytes + payload_len + 3:]
    raise ValueError("Start byte not found")
