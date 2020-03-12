
from core.loader.loader import uLoad

import logging
log = logging.getLogger("ota")
log.setLevel(logging.DEBUG)

from mod.ota_updater.ota import OtaUpdater

class OtaAction(uLoad):

    def _activate(self):

        self.OtaUpdater = OtaUpdater
        self.mbus.pub_h("ota_updater", "message")



