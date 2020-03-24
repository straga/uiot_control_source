import logging
log = logging.getLogger("MQTT-MSG")
log.setLevel(logging.INFO)

try:
    import ustruct as struct
except Exception:
    import struct
    pass


def pack_variable_byte_integer(value):
    remaining_bytes = bytearray()
    while True:
        value, b = divmod(value, 128)
        if value > 0:
            b |= 0x80
        remaining_bytes.extend(struct.pack('!B', b))
        if value <= 0:
            break
    return remaining_bytes


# def pack_utf8(packet=bytearray(), data=''):
#
#     if isinstance(data, str):
#         data = data.encode('utf-8')
#     packet.extend(struct.pack("!H", len(data)))
#     packet.extend(data)
#     return packet

def _pack_str16(packet, data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    packet.extend(struct.pack("!H", len(data)))
    packet.extend(data)
