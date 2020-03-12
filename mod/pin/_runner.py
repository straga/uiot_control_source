from core.loader.loader import uLoad

import logging
log = logging.getLogger("PIN")
log.setLevel(logging.INFO)

import machine
from machine import Pin, Signal


class PinAction(uLoad):

    async def _activate(self):

        self.pin_list = {}
        self.mbus.pub_h("module", "pin")


    async def get_pin(self, pin_name):

        pin = False
        if pin_name in self.pin_list:
            pin = self.pin_list[pin_name]

        else:
            pin_obj = await self.uconf.call("select_one", "pin_cfg", pin_name, obj=True)

            if pin_obj:

                if pin_obj.mode == "OUT":
                    hw_pin = Pin(pin_obj.number, mode=getattr(Pin, pin_obj.mode))
                    pin = Signal(hw_pin, invert=pin_obj.inverted)
                elif pin_obj.mode == "IN":
                    pin = Pin(pin_obj.number, mode=getattr(Pin, pin_obj.mode), pull=getattr(Pin, pin_obj.pull))

                if pin:
                    self.mbus.pub_h("pin/{}/init".format(pin_obj.name), [pin_obj.number, pin_obj.mode, pin_obj.pull])
                    self.pin_list[pin_obj.name] = pin

        return pin

    @staticmethod
    def set_handler(pin, trigger=None, handler=None, priority=None, wake=None, hard=None):

        _kwargs = {
            "handler": handler
        }
        if trigger:
            _kwargs["trigger"] = getattr(Pin, trigger)
        if priority:
            _kwargs["priority"] = priority
        if wake:
            _kwargs["wake"] = getattr(machine, wake)
        if hard is not None:
            _kwargs["hard"] = hard

        pin.irq(**_kwargs)
