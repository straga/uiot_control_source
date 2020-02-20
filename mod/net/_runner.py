from core.asyn.asyn import launch

import logging

log = logging.getLogger("NET")
log.setLevel(logging.DEBUG)

from core.loader.loader import uLoad

from mod.net.wifi import WIFIRun

class NetAction(uLoad):

    async def _activate(self):

        self.wifi = WIFIRun(self.core)
        self.wifi.start()

        # self.mbus.pub_h("module", "net")


