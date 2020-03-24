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

import logging
log = logging.getLogger("FTP")
log.setLevel(logging.INFO)


from .store import DataStore
from .cmd import FtpCmd


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
        self.client_list = {}
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

        if port_id not in self.client_list:
            request = FtpRequest(config=self, client_id=port_id)
            self.client_list[port_id] = request
        else:
            request = self.client_list[port_id]

        return request


    async def cmd_server(self, reader, writer):
        addr = writer.get_extra_info('peername')
        log.info("Client <- Start {}".format(addr))
        await _awrite(writer, "220 Welcome to micro FTP server\r\n")

        _ftp_cmd = FtpCmd(reader, writer, self)
        port_id = addr[1]
        request = self.get_request(port_id)

        while True:
            log.debug("")
            log.debug("++++++++++++++++++++++++++++++++++++++++")
            log.debug("Wait - CMD")
            data = None
            try:
                data = await reader.readline()
            except Exception as err:
                log.error(err)
                pass

            # log.debug("Read - CMD")

            if not data:
                log.debug("no data, break")
                break
            else:
                # log.debug("recv = %s" % data)
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

                if not result:
                    break

            log.debug("---------------------------------------+")


        if port_id in self.client_list:
            del self.client_list[port_id]

        await _aclose(writer)
        log.info("Client <- Stop {}".format(addr))


class FtpRequest:

    def __init__(self, config, client_id):

        self.cwd = config.cwd
        self.data_start = False
        self.transfer = False
        self.transfer_path = False
        self.transfer_rpl = False
        self.con_type = False
        self.client_id = client_id


    async def wait_transfer(self):

        log.debug(" + s3. Start: wait transfer")
        log.debug("  s3. Type: {}".format(self.con_type))
        log.debug("  s3. Transfer: {}".format(self.transfer))

        if self.con_type is "passive":
            self.data_start = True
            while True:
                await asyncio.sleep(0.1)
                # wait 100ms for next check start. Lite =100, Hard = 0
                if not self.data_start:
                    break

        log.debug(" - s3. Stop: wait transfer")
        return True













