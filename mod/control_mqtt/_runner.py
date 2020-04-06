
from core.loader.loader import uLoad

import logging
log = logging.getLogger("CTRL_mqtt")
log.setLevel(logging.DEBUG)


class ControlAction(uLoad):


    async def _activate(self):


        self.kitchen_light = False

        mqtt_env = self.core.env("mqtt")
        if mqtt_env:
            self.sub_h(topic="dev/kitchen_light/local/switch/led_status", func="binary_sensor_act")

            mqtt_env.mqtt.add_sbt(tpc="dev/kitchen_light/local/switch/led_status/state")

            self.sub_h(topic="dev/kitchen_light", func="binary_sensor_act")

            mqtt_env.mqtt.add_sbt(tpc="dev/kitchen_light/status")

            await mqtt_env.mqtt.sbt_subscribe()

        self.mbus.pub_h("module", "control_mqtt")

    async def light_control(self, sw_name, val, change=True):
        switch_env = self.core.env("switch")
        switch = await switch_env.get_switch(sw_name)
        if switch:
            if change:
                switch.change_state(val)
            else:
                switch.state = val



    async def binary_sensor_act(self, _id, _key, _pld, _rt):

        log.debug("id: {}, t: {}, k: {}, p: {}".format(_id , _key, _pld, _rt))

        if _id == "dev/kitchen_light/local/switch/led_status" and _key == "state":
            if self.kitchen_light:
                await self.light_control("led_status", _pld)
            else:
                await self.light_control("led_status", _pld, False)


        if _id == "dev/kitchen_light" and _key == "status":

            if _pld == "offline":
                self.kitchen_light = False
                await self.light_control("led_status", 0)

            elif _pld == "online":
                self.kitchen_light = True
                await self.light_control("led_status", -1)

