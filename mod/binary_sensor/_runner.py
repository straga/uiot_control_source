from core.loader.loader import uLoad


try:
    import uasyncio as asyncio
except Exception:
    import asyncio as asyncio
    pass

import logging
log = logging.getLogger("BINARY")
log.setLevel(logging.INFO)

import utime
from core.asyn.asyn import launch
from math import ceil


class BinaryAction(uLoad):

    async def _activate(self):
        self.bin_list = {}
        self.mbus.pub_h("module", "binary_sensor")


    async def get_binary(self, bin_name):

        binary_sensor = False
        if bin_name in self.bin_list:
            binary_sensor = self.bin_list[bin_name]

        else:
            binary_obj = await self.uconf.call("select_one", "binary_sensor_cfg", bin_name, obj=True)
            pin_env = self.core.env("pin")

            if binary_obj and pin_env:
                hw_pin = await pin_env.get_pin(pin_name=binary_obj.pin)

                if hw_pin:
                    id_binary = "{}".format(hw_pin)

                    pin_env.set_handler(pin=hw_pin, trigger=binary_obj.trigger, handler=self.cb)
                    binary_sensor = BinaryData(pin=hw_pin, name=binary_obj.name, on=binary_obj.on)

                    self.mbus.pub_h("binary_sensor/{}/init".format(binary_obj.name), [id_binary, binary_obj.on])

                    self.bin_list[id_binary] = binary_sensor

        return binary_sensor


    def cb(self, pin):
        launch(self.binary_callback, (pin, utime.ticks_ms()))


    async def binary_callback(self, pin, pin_tick):
        id_pin = "{}".format(pin)
        binary_pin = self.bin_list[id_pin]
        if not binary_pin.lock:
            binary_pin.lock = True

            pin_value = pin.value()
            await asyncio.sleep(binary_pin.delay)
            pin_value_debounce = pin.value()

            log.debug("pin: {}({}), val: {} == {}, tick: {}".format(binary_pin.name, binary_pin.pin, pin_value,
                                                                    pin_value_debounce, pin_tick))

            if pin_value == pin_value_debounce:
                try:
                    br_func = getattr(self, binary_pin.on)
                    br_func(binary_pin, pin_value, pin_tick)

                except Exception as e:
                    log.debug("Error: getattr: {}".format(e))
                    pass

            binary_pin.lock = False


    def touch(self, binary_pin, pin_value, pin_tick):
        result = False
        if pin_value is not binary_pin.init_val:
            result = "press"
            binary_pin.on_data = "press"
        elif binary_pin.on_data == "press":
            binary_pin.on_data = None
            result = "release"

        if result:
            self.mbus.pub_h("binary_sensor/{}/touch".format(binary_pin.name), result)


    def state(self, binary_pin, pin_value, pin_tick):

        if binary_pin.on_data == pin_value:
            binary_pin.on_data = 1-pin_value
        else:
            binary_pin.on_data = pin_value

        self.mbus.pub_h("binary_sensor/{}/state".format(binary_pin.name), binary_pin.on_data)


    def period(self, binary_pin, pin_value, pin_tick):

        if pin_value is not binary_pin.init_val:
            binary_pin.on_data = pin_tick
        else:

            priod_diff = pin_tick - binary_pin.on_data
            binary_pin.on_data = 0

            period = ceil(priod_diff/1000)
            self.mbus.pub_h("binary_sensor/{}/period".format(binary_pin.name), period)

            log.debug("Click Diff {} - {}".format(priod_diff, period))


class BinaryData:

    def __init__(self, pin, name, on=None, delay=0.1):
        self.name = name
        self.pin = pin
        self.lock = False
        self.on = on
        self.on_data = None
        self.delay = delay
        self.init_val = pin.value()

















