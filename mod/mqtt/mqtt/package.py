
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

from .utils import pack_variable_byte_integer, _pack_str16


class MQTTPacket:

    @staticmethod
    def ping():
        # command = 0xC0 #11000000 PINGREQ
        return struct.pack('!BB', 0xC0, 0)

    @staticmethod
    def subscribe(sbt, mid=0):

        command = 0x80 ##SUBSCRIBE fixed header 0x80 + 0010 reserved
        command = command | 0 << 3 | 0 << 2 | 1 << 1 | 0 << 0
        remaining_length = 2

        topics = []
        for topic in sbt:
            remaining_length += 2 + len(topic) + 1
            topics.append(topic)

        packet = bytearray()
        packet.append(command)
        packet.extend(pack_variable_byte_integer(remaining_length))
        packet.extend(struct.pack("!H", mid))

        for topic in sbt:
            _pack_str16(packet, topic)
            # topic.retain_handling_options | topic.retain_as_published | topic.no_local | topic.qos
            subscribe_options = 0 << 3 | 0 << 2 | 0 << 1 | 0 << 0
            packet.append(subscribe_options)

        log.debug("[SUBSCRIBE] mid: {},  topic: {} ,packet: {}".format(mid, topics, packet))

        return packet


    @staticmethod
    def publish(msg):

        command = 0x30  # 00110000
        command = command | 0 << 3 | (msg.qos << 1) | msg.retain << 0
        packet = bytearray()
        packet.append(command)
        remaining_length = 2 + len(msg.topic) + msg.pld_size
        packet.extend(pack_variable_byte_integer(remaining_length))
        _pack_str16(packet, msg.topic)
        packet.extend(msg.pld)

        log.debug("[PUBLISH] topic: {} , msg: {} ,packet: {}".format(msg.topic, msg.pld, packet))

        return packet



    @staticmethod
    def login(client_id, username, password, clean_session, keepalive, protocol, will_message=None, **kwargs):
        # MQTT Commands CONNECT
        proto_name = protocol["name"]
        proto_ver = protocol["ver"]
        command = 0x10
        remaining_length = 2 + len(proto_name) + 1 + 1 + 2 + 2 + len(client_id)

        connect_flags = 0
        if clean_session:
            connect_flags |= 0x02 #clean session

        #will_message
        if will_message:
            qos = 0
            remaining_length += 2 + len(will_message["tp"]) + 2 + len(will_message["msg"])
            connect_flags |= 0x04 | ((qos & 0x03) << 3) | ((will_message["rt"] & 0x01) << 5)


        #user
        if username is not None:
            remaining_length += 2 + len(username)
            connect_flags |= 0x80
            if password is not None:
                connect_flags |= 0x40
                remaining_length += 2 + len(password)


        packet = bytearray()
        packet.append(command)

        packet.extend(pack_variable_byte_integer(remaining_length))
        packet.extend(struct.pack("!H" + str(len(proto_name)) + "sBBH",
                                  len(proto_name),
                                  proto_name,
                                  proto_ver,
                                  connect_flags,
                                  keepalive))

        _pack_str16(packet, client_id)

        if will_message:
            _pack_str16(packet, will_message["tp"])
            _pack_str16(packet, will_message["msg"])

        if username is not None:
            _pack_str16(packet, username)

            if password is not None:
                _pack_str16(packet, password)

        return packet

