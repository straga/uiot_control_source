
import logging
log = logging.getLogger("SWITCH")
log.setLevel(logging.DEBUG)


class Switch:

    def __init__(self, pin, name):

        self.name = name
        self.pin = pin
        self.cb = None
        self.state = None


    def get_state(self):
        self.state = self.pin.value()
        return self.state

    def change_state(self, _set=None):

        if _set is not None:
            self.pin.value(_set)
        else:
            self.pin.value(1 - self.pin.value())

        self.state = self.pin.value()
        if self.cb:
            self.cb(self)
        return self.state


