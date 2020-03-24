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
                _kwargs = {}

                if pin_obj.mode:
                    _kwargs["mode"] = getattr(Pin, pin_obj.mode)
                if pin_obj.pull:
                    _kwargs["pull"] = getattr(Pin, pin_obj.pull)
                if pin_obj.value is not None:
                    _kwargs["value"] = pin_obj.value
                if pin_obj.drive:
                    _kwargs["drive"] = getattr(Pin, pin_obj.drive)
                if pin_obj.alt:
                    _kwargs["alt"] = getattr(Pin, pin_obj.alt)

                pin = Pin(pin_obj.number, **_kwargs)

                if pin:
                    if pin_obj.inverted is not None:
                        pin = Signal(pin, invert=pin_obj.inverted)
                    self.pin_list[pin_obj.name] = pin
                    self.mbus.pub_h("pin/{}/init".format(pin_obj.name), [pin_obj.number, pin_obj.mode, pin_obj.pull])


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
