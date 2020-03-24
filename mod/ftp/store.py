
import logging
log = logging.getLogger("FTP")
log.setLevel(logging.DEBUG)


try:
    import uos
    import uerrno
    import uasyncio as asyncio
    from core.platform import upy_awrite as _awrite

except Exception:
    import os as uos
    import errno as uerrno
    import asyncio as asyncio
    from core.platform import pc_awrite as _awrite


class DataStore:

    def __init__(self, max_chuck_size):
        self.max_chuck_size = max_chuck_size

    @staticmethod
    def get_absolute_path(cwd, payload):
        # Just a few special cases "..", "." and ""
        # If payload start's with /, set cwd to /
        # and consider the remainder a relative path
        if payload.startswith('/'):
            cwd = "/"
        for token in payload.split("/"):
            if token == '..':
                if cwd != '/':
                    cwd = '/'.join(cwd.split('/')[:-1])
                    if cwd == '':
                        cwd = '/'
            elif token != '.' and token != '':
                if cwd == '/':
                    cwd += token
                else:
                    cwd = cwd + '/' + token
        return cwd


    def get_path(self, request, argument):
        cwd = request.cwd

        # log.debug("cwd {} arg: {}".format(cwd, argument))

        path = self.get_absolute_path(cwd, argument)

        log.debug("Get path is %s" % path)
        return path

    @staticmethod
    async def send_list_data(request, writer):

        path = request.cwd

        try:
           uos.stat(path)
        except OSError as e:
            log.debug("PATH: {}".format(e))
            return False

        items = uos.listdir(path)

        if path == '/':
            path = ''
        for i in items:
            file_stat = uos.stat(path + "/" + i)

            file_permissions = "drwxr-xr-x" if (file_stat[0] & 0o170000 == 0o040000) else "-rw-r--r--"
            file_size = file_stat[6]
            description = "{}    1 owner group {:>10} Jan 1 2000 {}\r\n".format(
                file_permissions, file_size, i)

            try:
                await _awrite(writer, description)
            except Exception as err:
                log.error(err)
                pass


    async def send_file_data(self, request, writer):

        max_chuck_size = self.max_chuck_size
        buf = bytearray(max_chuck_size)

        argument = request.transfer_path
        remaining_size = uos.stat(argument)[-4]

        try:
            with open(argument, "rb") as f:
                while remaining_size:
                    chuck_size = f.readinto(buf)
                    remaining_size -= chuck_size
                    mv = memoryview(buf)
                    # await writer.awrite(mv[:chuck_size])
                    await _awrite(writer, mv[:chuck_size], True)
            request.transfer_rpl = "226 Transfer complete.\r\n"
        except OSError as e:
            if e.args[0] == uerrno.ENOENT:
                request.transfer_rpl = "550 No such file.\r\n"
            else:
                request.transfer_rpl = "550 Open file error.\r\n"
        finally:
            request.transfer_path = False
            del buf

        log.info("-> Transfer: {} - {}".format(argument, request.transfer_rpl))
        return True


    async def save_file_data(self, request, reader):
        max_chuck_size = self.max_chuck_size
        argument = request.transfer_path

        _file = "{}.svd".format(argument)

        log.debug("Argument - {}".format(_file))
        request.transfer_rpl = "550 File i/o error.\r\n"

        try:
            with open(_file, "wb") as f:
                log.debug("write byte")

                while True:
                    data = await reader.read(max_chuck_size)
                    if not data:
                        log.debug("not more data")
                        break
                    f.write(data)
            request.transfer_rpl = self.check_file(argument)

        except OSError as e:
            log.error("exception .. {}".format(e))
        finally:
            request.transfer_path = False

        log.info("<- Transfer: {} - {}".format(argument, request.transfer_rpl))

    @staticmethod
    def file_exist(_file):

        try:
            uos.stat(_file)[6]
        except OSError as e:
            log.debug("IS FILE: {} - {}".format(e, _file))
            return False
        return True


    @staticmethod
    def file_rename(_target, _file):
        try:
            uos.rename(_target, _file)
        except OSError as e:
            log.debug("IS FILE: {} - {}".format(e, _file))
            return False
        return True


    def check_file(self, _file):
        step1 = step2 = result = False
        _saved = "{}.svd".format(_file)
        _rename = "{}.rnm".format(_file)

        # esli exist file to rename ego
        if self.file_exist(_file):
            if self.file_rename(_file, _rename):
                step1 = True

        # esli exist saved to rename to file
        if self.file_exist(_saved):
            if self.file_rename(_saved, _file):
                step2 = True


        if step1 and step2:
            uos.remove(_rename)
            result = True
        elif step1:
            self.file_rename(_rename, _file)
        elif step2:
            result = True

        if result:
            return "226 Transfer complete\r\n"
        else:
            return "550 File i/o error.\r\n"