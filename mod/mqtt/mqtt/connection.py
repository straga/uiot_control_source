
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
log.setLevel(logging.INFO)

from .package import MQTTPacket
from .handler import MQTTHandler



from core.asyn.asyn import Lock


class MQTTConnect:

    def __init__(self, client_id="", addr=None, port=1883, keepalive=40, ping_interval=20, cb=None):

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
        self.username = None
        self.password = None

        self.lock = Lock()

        self.cb = cb

        self.open_status = 0
        self.broker_status = 0

    def set_handler(self, client):
        self.handler = MQTTHandler(connect=self, client=client).handler


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

        packet = MQTTPacket.login(client_id=self.client_id, username=self.username, password=self.password,
                                  clean_session=True, keepalive=self.keepalive,
                                  protocol={"name": self.proto_name, "ver": self.proto_ver})

        async with self.lock:
            await _awrite(self.writer, packet, True)



    async def _wait_msg(self):
        while self.reader:
            try:
                byte = await self.reader.read(1)
                if byte is None:
                    return
                if byte == b'':
                    raise OSError(-1)

                m_type = struct.unpack("!B", byte)[0]
                log.debug("   -: m_type: {}".format(m_type))

                m_raw = await self._read_packet()
                log.debug("   -: m_raw: {}".format(m_raw))

                await self.handler(m_type, m_raw)

            except Exception as e:
                log.debug("Error1: wait_msg: {}".format(e))
                await self.close()

            await asyncio.sleep(0.5)



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



