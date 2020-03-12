try:
    import uasyncio as asyncio
    from core.platform import upy_awrite as _awrite
    from core.platform import upy_aclose as _aclose
    import ujson as json

except Exception:
    import asyncio as asyncio
    from core.platform import pc_awrite as _awrite
    from core.platform import pc_aclose as _aclose
    import json

import random

import logging
log = logging.getLogger("HTTP_CLIENT")
log.setLevel(logging.DEBUG)
# log.setLevel(logging.INFO)

from .http_request import HttpRequest


class ClientResponse:

    def __init__(self, request):
        self.content = request.reader
        self.status = request._status
        self.headers = request._headers
        self.request = request

    async def read_data(self):

        size_hex = await self.request._read_line()
        size = False
        data = False
        if size_hex and size_hex != "\r\n":
            try:
                size = int(size_hex, 16)
            except Exception as e:
                log.error("Size:{}".format(e))
                data = None
                pass
        if size_hex == "\r\n":
            data = None

        if size:
            data = await self.readexactly(size)

        return data

    async def read(self, sz=-1):
        return await self.request._read_data(sz)

    async def readexactly(self, sz):
        return await self.content.readexactly(sz)

    async def done(self):
        await _aclose(self.content)


    def __repr__(self):
        return "<ClientResponse %d %s>" % (self.status, self.headers)


class WebClient:

    def __init__(self,):
        self.JsonrRpc = JsonrRpc

    async def open_connect(self, url):
        try:
            proto, dummy, host, path = url.split("/", 3)

        except ValueError as e:
            log.error("Open:{}".format(e))
            proto, dummy, host = url.split("/", 2)
            path = ""
            pass

        # if proto != "http:":
        #     raise ValueError("Unsupported protocol: " + proto)

        port = 80
        if ":" in host:
            host, port = host.split(":", 1)
            port = int(port)

        log.debug("Host:{} Port:{}".format(host, port))

        reader, writer = await asyncio.open_connection(host, port)
        return reader, writer, path, host


    async def request(self, url, method, params, rtype="json", headers=None):

        result = False
        rgen = False
        if rtype == "json":
            rgen = JsonrRpc(method, params, headers)
        elif rtype == "any":
            rgen = AnyReq(method, params, headers)


        # OPEN CONNECT

        host = False
        try:
            reader, writer, path, host = await self.open_connect(url=url)
        except Exception as e:
            log.error("Resp:{}".format(e))
            pass

        if rgen and host:

            addr = writer.get_extra_info('peername')
            log.info("+ from {}".format(addr))

            request = HttpRequest(self)
            await request.request_init(reader, writer, addr[1])


            # MAKE QUERY
            query = "{} /{} HTTP/1.1\r\n".format(rgen.method, path)

            # MAKE BODY
            content = b""
            try:
                content = rgen.body.encode()
            except Exception as e:
                log.error("Encode:{}".format(e))
                pass

            content_length = len(content)
            rgen.headers['Content-Length'] = content_length


            # MAKE HEADER
            rgen.headers['Host'] = host
            rgen.headers['Connection'] = "keep-alive"

            header = ''
            for n in rgen.headers:
                header += "{}: {}\r\n".format(n, rgen.headers[n])

            header += "\r\n"

            await request._response.awrite(request.writer, query, False)
            await request._response.awrite(request.writer, header, False)
            if content_length > 0:
                await request._response.awrite(request.writer, content, True)

            await request.request_response_line()
            await request.reguest_header()

            result = ClientResponse(request)

        return result


class AnyReq:
    def __init__(self, method, params, headers=None):
        default_headers = {
            "Accept": "*/*",
        }
        self.body = json.dumps(params)
        self.method = method
        self.headers = default_headers.update(headers) if headers else default_headers



class JsonrRpc:

    def __init__(self, method, params, headers=None):

        last_id = random.randint(0, 10000)
        default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        body = {
            "jsonrpc": "2.0",
            "id": last_id,
            "method": method,
            "params": params,
        }

        self.body = False
        try:
            self.body = json.dumps(body)
        except Exception as e:
            log.error("JSON:{}".format(e))
            pass

        self.method = "POST"
        self.headers = default_headers.update(headers) if headers else default_headers

