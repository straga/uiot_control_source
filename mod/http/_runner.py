from .http_server import WebServer

import sys
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import logging
log = logging.getLogger("HTTP")
log.setLevel(logging.DEBUG)

from core.loader.loader import uLoad

class HTTPAction(uLoad):

    async def _activate(self):

        self.server = WebServer()

        http_cfg = await self.uconf.call("select_one", "http_cfg", "default", obj=True)

        if http_cfg:
            self.server.addr = http_cfg.addr
            self.server.port = http_cfg.port
            self.server.path = http_cfg.path

            route_cfgs = await self.uconf.call("select", "http_route_cfg", active=True)

            for route_cfg in route_cfgs:

                log.info("Route: {}".format(route_cfg))

                _route = route_cfg["handler"]
                handler = __import__('mod.http.{}'.format(_route), None, None, [_route], 0).Handler

                self.server.set_route_handler(handler(self.core).route_handler)

                del sys.modules['mod.http.{}'.format(_route)]

            self.server.start()

            self.mbus.pub_h("module", "http")
