from core.loader.loader import uLoad
from .ftp import FTPServer

import logging
log = logging.getLogger("FTP")
log.setLevel(logging.INFO)


class FtpAction(uLoad):

    async def _activate(self):

        self.mbus.sub_h("inetFTP", "wifi/sta/ip", self.env, "ftp_act")

        self.ftp = FTPServer()
        self.ap_ip = "192.168.4.1"

        ftp_cfg = await self.uconf.call("select_one", "ftp_cfg", "default", True)
        if ftp_cfg:
            self.ftp.data_addr = self.ap_ip
            self.ftp.data_port = ftp_cfg.dport
            self.ftp.cmd_port = ftp_cfg.cport
            self.ftp.usr = ftp_cfg.usr
            self.ftp.passwd = ftp_cfg.passwd
            self.ftp.anonym = ftp_cfg.anonym

        self.ftp.start()
        self.mbus.pub_h("module", "ftp")



    async def ftp_act(self, _id, _key, _pld, _rt):
        log.debug("[ACT]: id: {}, key: {}, pld: {}, rt: {}".format(_id, _key, _pld, _rt))

        if _id == "wifi/sta/ip":

            if _pld:
                self.ftp.data_addr = _pld
            else:
                self.ftp.data_addr = self.ap_ip

            self.ftp.start()

