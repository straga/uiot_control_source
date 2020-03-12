
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

class MQTTConnect:

    def __init__(self, client_id="", addr=None, port=1883, keepalive=0, ping_interval=20, cb=None):

        self.client_id = client_id
        self.addr = addr
        self.port = port
        self.keepalive = keepalive
        self.ping_interval = ping_interval
        self.proto_name = b'MQTT'
        self.proto_ver = 4  #MQTTv311 = 4

        self.writer = None
        self.reader = None
        self.handler = None
        self.client = None

        self.cb = cb

        self.open_status = 0
        self.broker_status = 0

    def set_handler(self, client):
        self.handler = MQTTHandler(self, client).handler


    async def create_connect(self, clean):

        try:
            log.info("[CONNECT] addr:{} port:{}".format(self.addr, self.port))
            self.reader, self.writer = await asyncio.open_connection(self.addr, self.port)
            loop = asyncio.get_event_loop()
            loop.create_task(self._wait_msg())
            log.info("Connect Open")
        except Exception as e:
            log.debug("ERROR open connect: {}".format(e))
            return


        # MQTT Commands CONNECT
        command = 0x10
        remaining_length = 2 + len(self.proto_name) + 1 + 1 + 2 + 2 + len(self.client_id)

        connect_flags = 0
        if clean:
            connect_flags |= 0x02 #clean session

        packet = bytearray()
        packet.append(command)

        packet.extend(pack_variable_byte_integer(remaining_length))
        packet.extend(struct.pack("!H" + str(len(self.proto_name)) + "sBBH",
                                  len(self.proto_name),
                                  self.proto_name,
                                  self.proto_ver,
                                  connect_flags,
                                  self.keepalive))

        packet = pack_utf8(packet, self.client_id)

        await _awrite(self.writer, packet, True)


    async def _wait_msg(self):

        while self.reader:
            try:
                log.debug("_msg_start: wait_msg: {}")
                byte = await self.reader.read(1)
                m_type = struct.unpack("!B", byte)[0]
                m_raw = await self._read_packet()
                log.debug("_msg_end: wait_msg: {}".format(m_raw))
                await self.handler(m_type, m_raw)

            except Exception as e:
                log.debug("Error1: wait_msg: {}".format(e))
                await self.close()
                pass

            await asyncio.sleep(0.3)


    async def _read_packet(self):
        remaining_count = []
        remaining_length = 0
        remaining_mult = 1

        while True:
            byte, = struct.unpack("!B", await self.reader.read(1))
            remaining_count.append(byte)

            if len(remaining_count) > 4:
                log.warning('[MQTT ERR PROTO] RECV MORE THAN 4 bytes for remaining length.')
                return None

            remaining_length += (byte & 127) * remaining_mult
            remaining_mult *= 128

            if byte & 128 == 0:
                break

        packet = b''
        while remaining_length > 0:
            chunk = await self.reader.read(remaining_length)
            remaining_length -= len(chunk)
            packet += chunk

        return packet

    async def close(self):

        try:
            self.open_status = 0
            self.broker_status = 0
            self.reader = None
            await _aclose(self.writer)
            self.writer = None
        except Exception as e:
            log.debug("Error: close: {}".format(e))
            pass

        log.debug("Connect Close{}")

        await asyncio.sleep(1)



