# import gc
# import time


try:
    from uos import stat
    import uasyncio as asyncio
    from ujson import dumps

    from core.platform import upy_awrite as _awrite
    from core.platform import upy_aclose as _aclose
    from core.platform import upy_buffer as _abuffer
    from core.platform import upy_buffer_writer as _awriter_buf

except Exception:
    from os import stat
    import asyncio as asyncio
    from json import dumps

    from core.platform import pc_awrite as _awrite
    from core.platform import pc_aclose as _aclose
    from core.platform import pc_buffer as _abuffer
    from core.platform import pc_buffer_writer as _awriter_buf

import logging
log = logging.getLogger("HTTP_SERVER")
log.setLevel(logging.INFO)

from .http_request import HttpRequest



class WebServer:

    _mimeTypes = {
        ".html": "text/html",
        ".css": "text/css",
        ".js":  "application/javascript",
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".ico": "image/x-icon",
        ".xml": "text/xml",
    }

    def __init__(self, addr="0.0.0.0", port=8080, path="./www"):

        self.addr = addr
        self.port = port
        self.path = path
        self._routeHandlers = []
        self._timeout_sec = 2
        self.run = False
        self.origin = True


    def set_route_handler(self, handler):
        self._routeHandlers.append(handler)


    def _get_route_handler(self, request):

        if self._routeHandlers and request._method:

            for route in self._routeHandlers:

                if len(route) == 3 and route[0] == request._resPath \
                        and route[1].upper() == request._method.upper():
                    return route[2]
        return None


    def get_mime_type_from_filename(self, filename):
        filename = filename.lower()
        for ext in self._mimeTypes :
            if filename.endswith(ext) :
                return self._mimeTypes[ext]
        return None


    def _file_exists(self, path):
        try:
            return stat(path)[6]
        except:
            return False


    def _phys_path_from_url(self, url_path):
        if url_path == '/':
            phys_path = self.path + '/index.html'
            if self._file_exists(phys_path):
                return phys_path
        elif url_path:
            phys_path = self.path + url_path
            if self._file_exists(phys_path):
                return phys_path
        return None




    async def server(self, reader, writer):

        addr = writer.get_extra_info('peername')
        log.debug("+ from {}".format(addr))
        port_from = 0
        if len(addr) > 0:
            port_from = addr[1]

        request = HttpRequest(self)
        await request.request_init(reader, writer, port_from)
        await request.request_connect_line()
        await request.reguest_header()
        await request.reguest_process()

        await asyncio.sleep(1)
        await _aclose(writer)

        log.debug("- from {}".format(writer.get_extra_info('peername')))

    def start(self):

        if not self.run:
            loop = asyncio.get_event_loop()
            loop.create_task(asyncio.start_server(self.server, self.addr, self.port))

            log.info("Run on = {}:{}".format(self.addr, self.port))
            self.run = True
        else:
            log.info("HTTP already run on = {}:{}".format(self.addr, self.port))

        return True
