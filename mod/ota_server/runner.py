from .ota import OtaClient

import logging
log = logging.getLogger("OTA_SRV")
log.setLevel(logging.DEBUG)

from core.umod.config import uConfig

class OTARunner(uConfig):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.ota_client = OtaClient(self.core.env["http"])





