
from .emu_state import Pin_state

from core.asyn.asyn import launch
import asyncio as asyncio

class Pin:

    IN = 4
    OUT = 5
    OPEN_DRAIN = 6
    ALT = 7
    ALT_OPEN_DRAIN = 8

    PULL_UP = 9
    PULL_DOWN = 10
    PULL_HOLD = 11

    LOW_POWER = 12
    MED_POWER = 13
    HIGH_POWER = 14

    IRQ_FALLING = 15
    IRQ_RISING = 16
    IRQ_LOW_LEVEL = 17
    IRQ_HIGH_LEVEL = 18


    def __init__(self, id=None, mode=-1, pull=-1):

        self.id = id
        self.mode = mode
        self.pull = pull

        self._state = Pin_state()
        dafault_val = 0
        if pull is self.PULL_UP:
            dafault_val = 1

        self.value(dafault_val)

        self.trigger = None
        self.irq_run = False
        self.irq_state = None

    async def wait_value(self, handler):
        self.irq_run = True
        self.irq_state = self._state.read_value(self.id)
        while self.irq_run:
            result = False
            irq_value = self._state.read_value(self.id)
            if irq_value is not self.irq_state:
                if self.trigger is self.IRQ_FALLING and irq_value is 0:
                    result = True
                elif self.trigger is self.IRQ_RISING and irq_value is 1:
                    result = True
                elif self.trigger is None:
                    result = True

                # print(irq_value)
                self.irq_state = irq_value

            if result:
                handler(self)

            await asyncio.sleep(0.5)




    def value(self, val=None):

        if val is None:
            return self._state.read_value(self.id)
        else:
            return self._state.write_value(self.id, val)



    def irq(self, trigger=None, handler=None, priority=None, wake=None, hard=False):

        self.trigger = trigger
        if handler is not None:
            launch(self.wait_value, (handler,))
        else:
            self.irq_run = False

    def on(self):
        self.value(1)

    def off(self):
        self.value(0)


    def __repr__(self):
        return "Pin({})".format(self.id)



class PWM:

    def __init__(self, pin, freq=0, duty=50, timer=0):
        self._pin = pin
        self._freq = freq
        self._duty = duty
        self._timer = timer

    def init(self, freq=0, duty=50, timer=0):

        self._freq = freq
        self._duty = duty
        self._timer = timer

    def freq(self, freq):
        self._freq = freq

    def duty(self, duty):
        self._duty = duty

    def timer(self, timer):
        self._timer = timer



