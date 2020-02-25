
from core.loader.loader import uLoad

import logging
log = logging.getLogger("msg")
log.setLevel(logging.DEBUG)


class MessageAction(uLoad):
    """'
    Just print ALL message form MBUS in console
    """

    def _activate(self):

        self.sub_h(topic="ALL", func="print_mbus")
        self.mbus.pub_h("module", "message")

    @staticmethod
    def print_mbus(*msg):
        print("MBUS: {}".format(msg))

