
from core.loader.loader import uLoad

import logging
log = logging.getLogger("CTRL")
log.setLevel(logging.DEBUG)


class ControlAction(uLoad):


    async def _activate(self):

        self.sub_h(topic="binary_sensor/#", func="binary_sensor_act")

        binary_sensor = self.core.env("binary_sensor")
        await binary_sensor.get_binary("push_right")

        self.mbus.pub_h("module", "control_led")


    async def binary_sensor_act(self, _id, _key, _pld, _rt):

        switch_env = self.core.env("switch")

        if _id == "binary_sensor/push_right" and _key == "state":
            switch = await switch_env.get_switch("led_status")
            switch.change_state(_pld)



