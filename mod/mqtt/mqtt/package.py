
try:
    import uasyncio as asyncio
    import ustruct as struct
    from core.platform import upy_awrite as _awrite
    from core.platform import upy_aclose as _aclose
except Exception:
    import asyncio
    import struct
    from core.platform import pc_awrite as _awrite
    from core.platform import pc_aclose as _aclose
    pass



import logging
log = logging.getLogger("MQTT")

from .handler import MQTTHandler
from .utils import pack_variable_byte_integer, pack_utf8

class MQTTPacket:

    def __init__(self, client):
        self.client = client

    @staticmethod
    def ping():
        # command = 0xC0 #11000000 PINGREQ
        return struct.pack('!BB', 0xC0, 0)


    def subscribe(self, topic, qos=0):

        self.client.newpid()
        command = 0x80 #10000000
        command = command | 0 << 3 | 0 << 2 | 1 << 1 | 0 << 0 # + 0010

        remaining_length = 2
        remaining_length += 2 + len(topic) + 1

        packet = bytearray()
        packet.append(command)
        packet.extend(pack_variable_byte_integer(remaining_length))
        packet.extend(struct.pack("!H", self.client.pid))
        packet = pack_utf8(packet, topic)

        subscribe_options = 0 << 3 | 0 << 2 | 0 << 1 | qos << 0
        #subscribe_options = retain_handling_options << 4 | retain_as_published << 3 | no_local << 2 | qos - 2.3.1 Packet Identifier
        packet.append(subscribe_options)

        log.debug("[SUBSCRIBE] topic: {} ,packet: {}".format(topic, packet))

        return packet


    @staticmethod
    def publish(msg):

        command = 0x30  # 00110000
        command = command | 0 << 3 | (msg.qos << 1) | msg.retain << 0
        packet = bytearray()
        packet.append(command)
        remaining_length = 2 + len(msg.topic) + msg.pld_size
        packet.extend(pack_variable_byte_integer(remaining_length))
        packet = pack_utf8(packet, msg.topic)
        packet.extend(msg.pld)

        log.debug("[PUBLISH] topic: {} , msg: {} ,packet: {}".format(msg.topic, msg.pld, packet))

        return packet
