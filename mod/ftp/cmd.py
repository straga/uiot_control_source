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


from .data_client import FtpDataClient

class FtpCmd:

    def __init__(self, reader, writer, config):
        self.reader = reader
        self.writer = writer
        self.config = config

    async def query(self, request, cmd, argument):
        result = None
        _cmd = "_{}".format(cmd.lower())
        if hasattr(self, _cmd):
            func = getattr(self, _cmd)
            result = await func(request, argument)
            if result is None:
                result = True
        return result


    async def c_awrite(self, msg):
        await _awrite(self.writer, msg)

    async def _user(self, request, argument):

        if self.config.anonym and argument == "anonymous":
            await self.c_awrite("230 Logged in.\r\n")

        elif self.config.usr == argument:
            await self.c_awrite("331 User Ok.\r\n")
        else:
            await self.c_awrite("430 Invalid username or password.\r\n")
            return False

    async def _pass(self, request, argument):
        if self.config.passwd == argument:
            await self.c_awrite("230 Passwd Ok.\r\n")
        else:
            await self.c_awrite("430 Invalid username or password.\r\n")
            return False

    async def _syst(self, request, argument):
        await self.c_awrite("215 UNIX Type: L8\r\n")

    async def _noop(self, request, argument):
        await self.c_awrite("200 OK\r\n")

    async def _feat(self, request, argument):
        await self.c_awrite("211 no-features\r\n")

    async def _cdup(self, request, argument):
        argument = '..' if not argument else '..'
        log.debug("CDUP argument is %s" % argument)
        try:
            request.cwd = self.config.data_store.get_path(request, argument)
            await self.c_awrite("250 Okey.\r\n")
        except Exception as e:
            await self.c_awrite("550 {}.\r\n".format(e))

    async def _cwd(self, request, argument):
        log.debug("CWD argument is %s" % argument)
        try:
            request.cwd = self.config.data_store.get_path(request, argument)
            await self.c_awrite("250 Okey.\r\n")
        except Exception as e:
            await self.c_awrite("550 {}.\r\n".format(e))

    async def _pwd(self, request, argument):
        try:
            await self.c_awrite('257 "{}".\r\n'.format(request.cwd))
        except Exception as e:
            await self.c_awrite('550 {}.\r\n'.format(e))

    async def _type(self, request, argument):
        # Always use binary mode 8-bit
        await self.c_awrite("200 Binary mode.\r\n")

    async def _mkd(self, request, argument):
        try:
            uos.mkdir(self.config.data_store.get_path(request, argument))
            await self.c_awrite("257 Okey.\r\n")
        except OSError as e:
            if e.args[0] == uerrno.EEXIST:
                await self.c_awrite("257 Okey.\r\n")
            else:
                await self.c_awrite("550 {}.\r\n".format(e))

    async def _rmd(self, request, argument):
        try:
            uos.rmdir(self.config.data_store.get_path(request, argument))
            await self.c_awrite("257 Okey.\r\n")
        except Exception as e:
            await self.c_awrite("550 {}.\r\n".format(e))

    async def _size(self, request, argument):
        try:
            size = uos.stat(self.config.data_store.get_path(request, argument))[6]
            await self.c_awrite('213 {}\r\n'.format(size))
        except Exception as e:
            await self.c_awrite('550 {}.\r\n'.format(e))

    async def _retr(self, request, argument):
        await self.c_awrite("150 Opening data connection\r\n")

        request.transfer = "SEND"
        request.transfer_path = self.config.data_store.get_path(request, argument)
        await request.wait_transfer()

        if request.transfer_rpl:
            await self.c_awrite(request.transfer_rpl)
        else:
            await self.c_awrite("550 File Load Error.\r\n")


    async def _stor(self, request, argument):
        await self.c_awrite("150 Opening data connection\r\n")

        request.transfer = "SAVE"
        request.transfer_path = self.config.data_store.get_path(request, argument)
        await request.wait_transfer()

        if request.transfer_rpl:
            await self.c_awrite(request.transfer_rpl)
        else:
            await self.c_awrite("550 File Save Error.\r\n")


    async def _quit(self, request, argument):
        await self.c_awrite("221 Bye!.\r\n")
        return False


    async def _dele(self, request, argument):
        try:
            uos.remove(self.config.data_store.get_path(request, argument))
            await self.c_awrite("257 Okey.\r\n")
        except Exception as e:
            await self.c_awrite("550 {}.\r\n".format(e))


    async def _pasv(self, request, argument):

        # Send to client server adress
        if self.config.data_addr:

            result = '227 Entering Passive Mode ({},{},{}).\r\n'.format(
                self.config.data_addr.replace('.', ','), self.config.data_port >> 8, self.config.data_port % 256)

            log.debug("PASV: {}".format(result))

            await self.c_awrite(result)

            if not self.config.run_data_serv:
                self.config.run_data_serv = FtpDataClient(self.config)

                log.info("Start Passive Data Server to {} {}".format("0.0.0.0", self.config.data_port))
                loop = asyncio.get_event_loop()
                loop.create_task(asyncio.start_server(self.config.run_data_serv.data_server, "0.0.0.0", self.config.data_port))
                # loop.call_soon(asyncio.start_server(self.ftp_data_server, "0.0.0.0", self.dport))
                # self.config.run_data_serv = True

            addr = self.writer.get_extra_info('peername')
            # self.config.run_data_serv.port_id = addr[1]
            self.config.run_data_serv.port_id.append(addr[1])

            request.con_type = "passive"


        else:
            await self.c_awrite("221 Bye!.\r\n")
            return False


    async def _list(self, request, argument):

        await self.c_awrite("150 Here comes the directory listing.\r\n")
        request.transfer = "LIST"

        await request.wait_transfer()
        await self.c_awrite("226 Directory send okey.\r\n")


    async def _mdtm(self, request, argument):

        # Dummy for File Modification Time.
        await self.c_awrite("213 {}.\r\n".format(argument))
        return True