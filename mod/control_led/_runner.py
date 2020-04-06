
from core.loader.loader import uLoad

# import logging
# log = logging.getLogger("CTRL_LED")
# log.setLevel(logging.DEBUG)


class ControlAction(uLoad):

    async def _activate(self):

        await self.core.env("switch").get_switch("led_status")
        self.mbus.pub_h("module", "control_led")





