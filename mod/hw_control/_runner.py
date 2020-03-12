from core.loader.loader import uLoad

import logging
log = logging.getLogger("HW")
log.setLevel(logging.INFO)

import asyncio as asyncio
from core.asyn.asyn import launch

class HwAction(uLoad):

    async def _activate(self):

        self.mbus.pub_h("module", "hw_control")


    async def pin_value(self, hw_mod):

        hw_list = []

        hw_scan = await self.uconf.call("scan", hw_mod)
        pin_env = self.core.env("pin")

        for hw_cfg in hw_scan:

            hw_pin = await pin_env.get_pin(pin_name=hw_cfg["name"])

            if hw_pin:
                hw_list.append({"name": "{}".format(hw_pin), "value": hw_pin.value()})

        return hw_list


    async def pin_wait(self, pin_name, hold, val=-1):

        pin_env = self.core.env("pin")
        hw_pin = await pin_env.get_pin(pin_name=pin_name)
        if hw_pin:
            val_1nd = val
            val_2nd = 1-val_1nd

            if val == -1:
                val_2nd = hw_pin.value()
                val_1nd = 1-val_2nd

            hw_pin.value(val_1nd)
            await asyncio.sleep(hold)
            hw_pin.value(val_2nd)



