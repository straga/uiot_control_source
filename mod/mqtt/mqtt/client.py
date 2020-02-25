# Copyright (c) 2020 Viktor Vorobjov

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
from .connection import MQTTConnect
from .message import MQTTMessage
from .utils import pack_variable_byte_integer, pack_utf8


class MQTTClient:

    class Message(MQTTMessage):
        pass

    def __init__(self, client_id, addr, port):

        self.connect = MQTTConnect(client_id, addr, port)
        self.packet = MQTTPacket(self)

        self.pid = 0
        self.cb = None

        self.sbt = None
        self.mpub = []

        self.fail = 0
        self._run = False


    def newpid(self):
        return self.pid + 1 if self.pid < 65535 else 1


    def set_callback(self, f):
        self.cb = f


    async def sbt_subscribe(self):
        log.info('[SUB TPC] : {}'.format(self.sbt))
        if self.sbt:
            packet = self.packet.subscribe(self.sbt)
            await _awrite(self.connect.writer, packet, True)


    def pub(self, value):
        self.mpub.append(value)


    async def task_ping_msg(self):
        while self._run:
            log.debug("[FAIL] {}, brocker: {}".format(self.fail, self.connect.broker_status))
            if self.connect.broker_status:
                packet = self.packet.ping()
                await _awrite(self.connect.writer, packet, True)

            if self.fail > 3:
                self.fail = 0
                await self.close()

            self.fail += 1


            await asyncio.sleep(self.connect.ping_interval)


    async def task_publish(self):
        while self._run:
            while len(self.mpub) > 0:
                val = self.mpub.pop(0)
                if self.connect.broker_status:
                    msg = MQTTClient.Message(val["tp"], val["msg"], val["rt"] if "rt" in val else False)
                    packet = self.packet.publish(msg)
                    await _awrite(self.connect.writer, packet, True)
            await asyncio.sleep(0.3)


    async def task_connect(self, clean=True):
        while self._run:
            if self.connect.open_status == 0:
                self.connect.set_handler(self)
                await self.connect.create_connect(clean)
                log.debug("Try CONNECT to MQTT")
            await asyncio.sleep(5.0)


    async def close(self):
        await self.connect.close()


    def start(self):

        if not self._run and self.connect.addr:
            self._run = True

            loop = asyncio.get_event_loop()
            loop.create_task(self.task_connect())
            loop.create_task(self.task_publish())
            loop.create_task(self.task_ping_msg())

            log.info("MQTT Coonect to = {}:{}".format(self.connect.addr, self.connect.port))


    def stop(self):
        self._run = False
        loop = asyncio.get_event_loop()
        loop.create_task(self.close())








