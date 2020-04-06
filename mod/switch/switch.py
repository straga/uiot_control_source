
import logging
log = logging.getLogger("SWITCH")
log.setLevel(logging.DEBUG)


class Switch:

    def __init__(self, pin, name):

        self.name = name
        self.pin = pin
        self.cb = None
        self.state = None
        self.restore = None


    def get_state(self):
        return self.pin.value()


    def change_state(self, _set=None):

        if _set is not None:
            if isinstance(_set, int):
                self.pin.value(_set)
        elif _set == -1:
            self.pin.value(self.state)
        else:
            self.pin.value(1 - self.pin.value())

        state = self.pin.value()
        if self.cb:
            self.cb(self)
        return state


