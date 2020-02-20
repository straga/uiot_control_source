
from .emu_state import Pin_state


class Pin:

    OUT = 4
    IN = 5
    PULL_UP = 6
    PULL_DOWN = 6


    def __init__(self, id=None, mode=None, pull=None, value=None):

        self.id = id
        self.mode = mode
        self.pull = pull

        self._state = Pin_state()

        if value:
            self.value(value)

    def value(self, val=None):

        if val is None:
            return self._state.read_value(self.id)
        else:
            return self._state.write_value(self.id, val)



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



