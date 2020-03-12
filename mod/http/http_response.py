
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
log = logging.getLogger("HTTP_RS")
log.setLevel(logging.INFO)


class HttpResponse:

    def __init__(self, web, request):
        self._web = web
        self._request = request
        self._headers = {}
        self._allow_origin = "*"
        self._content_type = None
        self._content_length = 0
        self.chunk_sz = 512


    async def awrite(self, writer, data, b=False):
        if not b:
            data = data.encode('utf-8')
        await _awrite(writer, data, True)

    def set_header(self, name, value):
        if name and name:
            self._headers[name] = str(value)

    def make_base_headers(self, code):

        if self._web.origin:
            self.set_header('Access-Control-Allow-Origin', self._allow_origin)
        self.set_header('Server', 'uWEBserv straga')
        hdr = ''
        for n in self._headers :
            hdr += "{}: {}\r\n".format(n, self._headers[n])
        reason = 'OK'
        resp = "HTTP/1.1 {} {}\r\n{}\r\n".format(code, reason, hdr)
        return resp.encode('UTF-8')


    def make_content_type_header(self, charset=None):
        if self._content_type:
            ct = self._content_type + (("; charset={}".format(charset)) if charset else "")
        else:
            ct = "application/octet-stream"

        self.set_header('Content-Type', ct)

    def make_headers(self, code):
        if 200 <= code < 300:
            self._keep_alive = self._request.is_keep_alive
        else:
            self._keep_alive = False

        if self._keep_alive :
            self.set_header('Connection', 'Keep-Alive')
            self.set_header('Keep-Alive', 'timeout={}'.format(self._web._timeout_sec))
        else:
            self.set_header('Connection', 'Close')

        return self.make_base_headers(code)


    async def return_response(self, code, content=None, b=True):

        data = self.make_headers(code)
        log.debug("< : Return : {}".format(data))

        await self.awrite(self._request.writer, data, b)


    async def response_file(self, filepath):

        gzip_size = self._web._file_exists("{}.gz".format(filepath))
        self._content_type = self._web.get_mime_type_from_filename(filepath)

        if gzip_size:
            size = gzip_size
            filepath = "{}.gz".format(filepath)
            self.set_header('Content-Encoding', 'gzip')

        else:
            size = self._web._file_exists(filepath)

        if size > 0:

            # self._content_type = self._web.get_mime_type_from_filename(filepath)
            self.make_content_type_header()

            self._content_length = size
            self.set_header('Content-Length', size)

            log.debug("= : File: {},  type: {}, sz: {}".format(filepath, self._content_type, size))

        if self._content_type:

            log.debug("< : Send: {}".format(self._headers["Content-Type"]))

            with open(filepath, 'rb') as file:

                await self.return_response(200)

                try_num = 0
                while True:

                    buf = _abuffer(1024)

                    if buf:
                        x = file.readinto(buf)
                        if not x:
                            break

                        await _awriter_buf(self.awrite, self._request.writer, buf, x)
                        size -= x

                    else:
                        try_num += 1

                    if try_num > 1000:
                        return False
                return True

        elif size > 0:

            log.debug("< : Send: {}".format(self._headers["Content-Type"]))
            self.set_header('Transfer-Encoding', "chunked")
            with open(filepath, 'rb') as file:
                await self.return_response(200)

                chunk = file.read(self.chunk_sz)
                while chunk:
                    sen = b"".join([hex(len(chunk))[2:].encode(), "\r\n".encode(), chunk, "\r\n".encode()])
                    await self.awrite(self._request.writer, sen, True)
                    chunk = file.read(self.chunk_sz)

            await self.awrite(self._request.writer, b"0\r\n\r\n", True)

            return True

        return False


    async def response_request(self, content, b=False):
        size = 0
        if content is not None:
            size = len(content)


        if size > 0:
            self.set_header('Content-Length', size)
            await self.return_response(200)
            await self.awrite(self._request.writer, content, b)

        else:
            await self.return_response(404)


    async def return_json(self, obj):
        content = None
        self._content_type = 'application/json'
        self.make_content_type_header("UTF-8")
        try:
            content = dumps(obj)
        except Exception as err:
            log.error(err)
            pass

        await self.response_request(content)


    async def return_not_found(self):
        await self.return_response(404)

    async def return_ok(self):
        await self.return_response(200)



