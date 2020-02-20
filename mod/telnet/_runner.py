from core.loader.loader import uLoad
from .telnet import TelnetServer

import logging
log = logging.getLogger("Telnet")
log.setLevel(logging.INFO)


class TelnetAction(uLoad):

    async def _activate(self):

        self.telnet = TelnetServer()

        telnet_cfg = await self.uconf.call("select_one", "telnet_cfg", "default", True)
        if telnet_cfg:
            self.telnet.port = telnet_cfg.port
            self.telnet.pswd = telnet_cfg.pswd

        self.telnet.start()

        self.mbus.pub_h("module", "ftp")
