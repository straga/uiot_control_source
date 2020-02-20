# Copyright (c) 2019 Viktor Vorobjov
import logging

try:
    import uos
    import uasyncio as asyncio

except Exception:
    import os as uos
    import asyncio as asyncio


from .telnetio import TelnetIO

log = logging.getLogger("telnet")
log.setLevel(logging.INFO)


class TelnetServer:

    def __init__(self, pswd="micro"):

        self.pswd = pswd
        self.port = 23
        self.sw_client = None
        self.run = False


    # On accepting client connection
    async def server(self, reader, writer):

        remote_addr = writer.extra["peername"]
        log.info("Telnet connection from: {}".format(remote_addr))

        if self.sw_client:
            log.info("Close previous connection ...")
            self.stop()

        log.info("Get client connection ...")
        self.sw_client = TelnetIO(writer.s, self.pswd)

        self.sw_client.socket.setblocking(False)
        self.sw_client.socket.sendall(bytes([255, 252, 34]))  # dont allow line mode
        self.sw_client.socket.sendall(bytes([255, 251, 1]))  # turn off local echo
        uos.dupterm(self.sw_client)

        loop = asyncio.get_event_loop()
        loop.create_task(self.client_rx())

        await asyncio.sleep(0.1)


    # On receiving client data
    async def client_rx(self):

        while True:
            if self.sw_client != None:
                try:
                    yield asyncio.IORead(self.sw_client.socket)
                    uos.dupterm_notify(True)  # dupterm_notify will somehow make a copy of sw_client

                except:
                    # clean up
                    log.info("Telnet client disconnected ...")
                    yield asyncio.IOReadDone(self.sw_client.socket)
                    self.stop()

                await asyncio.sleep_ms(1)
            else:
                await asyncio.sleep(1)


    def stop(self):

        if self.sw_client:
            self.sw_client.close()
            uos.dupterm_notify(self.sw_client.socket)  # deactivate dupterm
            uos.dupterm(None)
            self.sw_client = None


    # Add server tasks to asyncio event loop
    # Server will run after loop has been started
    def start(self, addr="0.0.0.0"):

        loop = asyncio.get_event_loop()
        if not self.run:
            loop.create_task(asyncio.start_server(self.server, addr, self.port))
            log.info("Telnet server started on {}:{}".format(addr, self.port))
            self.run = "{};{}".format(addr, self.port)
        else:
            log.info("Telnet server already on {}:{}".format(addr, self.port))

        return True


