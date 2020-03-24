
import logging
log = logging.getLogger("CTRL")
log.setLevel(logging.DEBUG)


try:
    import uasyncio as asyncio
except Exception:
    import asyncio as asyncio

from core.loader.loader import uLoad


class ControlAction(uLoad):

    async def _activate(self):

        switch_env = self.core.env("switch")
        await switch_env.get_switch("led_status")

        self.mbus.pub_h("module", "ctrl_kithcen_light")
        self.sub_h(topic="light_control/#", func="light_act")


    async def light_act(self, _id, _key, _pld, _rt):

        switch_env = self.core.env("switch")

        if _id == "light_control/light_status" and _key == "set":

            switch = await switch_env.get_switch("led_status")
            switch.change_state(_pld)

            log.debug("_pld: {}".format(_pld))


