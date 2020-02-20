# Copyright (c) 2020 Viktor Vorobjov


try:

    import uos
    import uerrno
    import uasyncio as asyncio
    from core.platform import upy_awrite as _awrite
    from core.platform import upy_aclose as _aclose

except Exception:

    import os as uos
    import errno as uerrno
    import asyncio as asyncio
    from core.platform import pc_awrite as _awrite
    from core.platform import pc_aclose as _aclose
    pass


import logging
log = logging.getLogger("FTP")
log.setLevel(logging.INFO)


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

        log.debug("cwd {} arg: {}".format(cwd, argument))
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

        log.debug("Argument - {}".format(argument))
        request.transfer_rpl = "550 File i/o error.\r\n"

        try:
            with open(argument, "wb") as f:
                log.debug("WB")

                while True:
                    try:
                        data = await reader.read(max_chuck_size)
                        w = f.write(data)
                        if not data or w < max_chuck_size:
                            break

                    except Exception as e:
                        log.error("exception .. {}".format(e))
                        break

            request.transfer_rpl = self.check_file(argument)

        except OSError as e:
            log.error("exception .. {}".format(e))
        finally:
            request.transfer_path = False

        log.info("<- Transfer: {} - {}".format(argument, request.transfer_rpl))


    def check_file(self, _file):
        return "226 Transfer complete\r\n"


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


class FtpDataClient:
    def __init__(self, config):
        self.config = config
        self.port_id = []

    async def data_server(self, reader, writer):

        addr = writer.get_extra_info('peername')
        log.debug("+ Data Server <- client from {}".format(addr))

        port_id = False

        try:
            port_id = self.port_id.pop(0)
        except Exception as e:
            log.debug("port_id {}".format(e))
            pass

        if port_id:
            request = self.config.get_request(port_id)

            log.debug("Data Start {}".format(request.data_start))
            log.debug("ps0. Data Transfer {}".format(request.transfer))

            while True:
                if request.transfer:

                    if request.transfer is "LIST":
                        log.debug("s1. List Dir")
                        await self.config.data_store.send_list_data(request, writer)
                        request.transfer = False

                    elif request.transfer is "SEND":
                        log.debug("s1. Send File")
                        await self.config.data_store.send_file_data(request, writer)
                        request.transfer = False

                    elif request.transfer is "SAVE":
                        log.debug("s1. Save File")
                        await self.config.data_store.save_file_data(request, reader)
                        request.transfer = False

                    elif request.transfer:
                        log.debug("s1. State Start")
                        # Time for wait Open Socker Activite if not active = Close connection
                        await asyncio.sleep(0.5)
                        request.transfer = False

                else:
                    request.data_start = False
                    break

        await _aclose(writer)
        log.debug("- Data Server <- client from {}".format(addr))
        log.debug("ps2. Data Server = Close")


class FtpRequest:

    def __init__(self, config):

        self.cwd = config.cwd
        self.data_start = False
        self.transfer = False
        self.transfer_path = False
        self.transfer_rpl = False
        self.con_type = False


    async def wait_transfer(self):

        log.debug("SEND Type: {}".format(self.con_type))
        log.debug("SEND Transfer: {}".format(self.transfer))

        if self.con_type is "passive":
            self.data_start = True
            while True:
                await asyncio.sleep(0.1)
                # wait 100ms for next check start. Lite =100, Hard = 0
                if not self.data_start:
                    break

        log.debug("s3. Send Data Done")
        return True


class FTPServer:

    def __init__(self, data_addr=None, cmd_port=25, data_port=26, usr=None, psswd=None, anonym=False, cwd="/"):

        self.data_addr = data_addr
        self.data_port = data_port
        self.cmd_port = cmd_port
        self.usr = usr
        self.psswd = psswd
        self.anonym = anonym
        self.max_chuck_size = 512
        self.run_cmd_serv = False
        self.run_data_serv = False
        self.cwd = cwd
        self.act_client = {}
        self.data_store = DataStore(self.max_chuck_size)


    def start(self):

        if not self.run_cmd_serv:
            self.run_cmd_serv = True

            loop = asyncio.get_event_loop()
            loop.create_task(asyncio.start_server(self.cmd_server, "0.0.0.0", self.cmd_port))
            log.info("FTP run on = {}:{}".format("0.0.0.0", self.cmd_port))

        else:
            log.info("FTP already run on = {}:{}".format("0.0.0.0", self.cmd_port))

        return True

    def get_request(self, port_id):

        if port_id not in self.act_client:
            request = FtpRequest(self)
            self.act_client[port_id] = request
        else:
            request = self.act_client[port_id]

        return request


    async def cmd_server(self, reader, writer):
        addr = writer.get_extra_info('peername')
        log.info("Client <- Start {}".format(addr))
        await _awrite(writer, "220 Welcome to micro FTP server\r\n")

        _ftp_cmd = FtpCmd(reader, writer, self)
        port_id = addr[1]
        request = self.get_request(port_id)

        while True:
            log.debug("Wait - CMD")
            data = None
            try:
                data = await reader.readline()
            except Exception as err:
                log.error(err)
                pass

            log.debug("Read - CMD")

            if not data:
                log.debug("no data, break")
                break
            else:
                log.debug("recv = %s" % data)
                cmd = None
                argument = None
                try:
                    data = data.decode("utf-8")
                    split_data = data.split(' ')
                    cmd = split_data[0].strip('\r\n')
                    argument = split_data[1].strip('\r\n') if len(split_data) > 1 else None
                    log.debug("cmd is %s, argument is %s" % (cmd, argument))
                except Exception as err:
                    log.error(err)
                    pass

                result = await _ftp_cmd.query(request, cmd, argument)

                if result is None:
                    await _awrite(writer, "520 not implement.\r\n")

        if port_id in self.act_client:
            del self.act_client[port_id]

        await _aclose(writer)
        log.info("Client <- Stop {}".format(addr))













