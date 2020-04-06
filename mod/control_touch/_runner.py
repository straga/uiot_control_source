
from core.loader.loader import uLoad

import logging
log = logging.getLogger("CTRL")
log.setLevel(logging.DEBUG)
try:
    import uasyncio as asyncio
except Exception:
    import asyncio as asyncio
    pass

class ControlAction(uLoad):


    async def _activate(self):

        self.sub_h(topic="binary_sensor/#", func="binary_sensor_act")

        binary_sensor = self.core.env("binary_sensor")
        #Activate sensor buttons
        await binary_sensor.get_binary("push_left")
        await binary_sensor.get_binary("push_period")
        await binary_sensor.get_binary("push_right")

        self.mbus.pub_h("module", "control_touch")
        switch_env = self.core.env("switch")
        self.switch = await switch_env.get_switch("led_status")



    async def binary_sensor_act(self, _id, _key, _pld, _rt):

        # MQTT
        led = "dev/kitchen_light/MQTT/light_control/light_status/set"
        mqtt_env = self.core.env("mqtt")

        # Touch
        if _id == "binary_sensor/push_left" and _key == "touch":

            pld = 0
            if _pld == "press":
                pld = 1

            self.switch.change_state(pld)

            if mqtt_env:
                mqtt_env.mqtt.pub({"tp": led,"msg": pld,"rt": False })

        # Period
        elif _id == "binary_sensor/push_period" and _key == "period":

            if mqtt_env:
                mqtt_env.mqtt.pub({"tp": led, "msg": 1, "rt": False})

            self.switch.change_state(1)
            await asyncio.sleep(_pld)


            if mqtt_env:
                mqtt_env.mqtt.pub({"tp": led, "msg": 0, "rt": False})

            self.switch.change_state(0)

        # State
        elif _id == "binary_sensor/push_right" and _key == "state":

            if mqtt_env and self.switch:

                mqtt_env.mqtt.pub({"tp": led, "msg": 1-self.switch.get_state(), "rt": False})
                self.switch.change_state()