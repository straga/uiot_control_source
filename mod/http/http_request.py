import gc
try:
    from uos import stat
    import uasyncio as asyncio
    from ujson import dumps

except Exception:
    from os import stat
    import asyncio as asyncio
    from json import dumps


from .http_response import HttpResponse

import logging
log = logging.getLogger("HTTP_RG")
log.setLevel(logging.INFO)


class HttpRequest:

    MAX_RECV_HEADER_LINES = 50

    def __init__(self, web_srv):
        self._web_srv = web_srv

    async def request_init(self, reader, writer, id):
        self.reader = reader
        self.writer = writer
        self.id = id
        self._method   = ''
        self._resPath     = ''
        self._headers  = {}
        self._status = None
        self._queryParams = {}
        self._response = HttpResponse(self._web_srv, self)


    async def _read_data(self, sz=-1):

        data_post = False
        try:
            data_post = await self.reader.read(sz)
        except Exception as err:
            log.error(err)
            pass
        return data_post


    async def _read_line(self):

        request = False

        try:
            request = await self.reader.readline()
        except Exception as err:
            log.error(err)
            pass

        if not request or request == b'':
            request = False
        else:

            try:
                request = request.decode()
            except Exception as err:
                log.error(err)
                pass

        return request



    async def request_response_line(self):
        line = await self._read_line()

        try:
            elements = line.strip().split()
            self._status = int(elements[1])
        except Exception as err:
            log.error(err)
            pass

        log.debug("> {}: Response Line: {}".format(self.id, line))



    async def request_connect_line(self):

        line = await self._read_line()
        # log.debug("< : L raw: {}".format(line))

        elements = ""
        try:
            if line:
                elements = line.strip().split()
        except Exception as err:
            log.error(err)
            pass

        log.debug("> {}: Fist Line: {}".format(self.id, line))

        if len(elements) == 3:
            _httpVer = elements[2].upper()
            self._method = elements[0].upper()
            path = elements[1]

            log.debug("> : ver: {} method :{}".format(_httpVer, self._method))

            elements = path.split('?', 1)
            if len(elements) > 0:
                self._resPath = elements[0]

                log.debug("> : _resPath : {}".format(self._resPath))

                # get query and params
                if len(elements) > 1:
                    _queryString = elements[1]
                    elements = _queryString.split('&')
                    log.debug("> : Get query : {}".format(_queryString))

                    for s in elements:
                        param = s.split('=', 1)

                        if len(param) > 0:
                            value = param[1] if len(param) > 1 else ''
                            self._queryParams[param[0]] = value

                    log.debug("> : queryParams : {}".format(self._queryParams))



    async def reguest_header(self):

        log.debug(" = : HEADER")

        while True:
            header_line = await self._read_line()
            if not header_line or header_line == "\r\n":
                break

            if len(self._headers) < HttpRequest.MAX_RECV_HEADER_LINES \
                    and not header_line.startswith("Cookie:"):

                elements = header_line.strip().split(':', 1)

                self._headers[elements[0].strip().lower()] = elements[1].strip()

                log.debug("> : {}".format(elements))



    async def reguest_process(self):

        process = False
        route_handler = self._web_srv._get_route_handler(self)
        log.debug("= : Handler : {}".format(route_handler))
        gc.collect()

        if self._method == "OPTIONS":

            self._response.set_header('Access-Control-Allow-Methods', '*')
            self._response.set_header('Access-Control-Allow-Headers', '*')
            self._response.set_header('Access-Control-Allow-Credentials', 'true')
            self._response.set_header('Access-Control-Max-Age', '86400')

            await self._response.return_ok()
            process = True


        elif self._method == "POST" and route_handler:
            process = await route_handler(self)


        elif self._method in ('GET', 'HEAD'):

            if route_handler:
                await route_handler(self)
            else:

                filepath = self._web_srv._phys_path_from_url(self._resPath)
                log.debug("= : File Path : {}".format(filepath))

                if filepath:
                    process = await self._response.response_file(filepath)

        if not process:
            await self._response.return_not_found()



    @property
    def is_keep_alive(self):
        return ('keep-alive' in self._headers.get('connection', '').lower())