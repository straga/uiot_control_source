
class Signal:


    def __init__(self, pin_obj=None, invert=False):

        self.pin = pin_obj
        self.invert = 0



    def value(self, val=None):

        if val is None:
            return self.pin.value()
        else:
            if self.invert:
                return self.pin.value(1 - val)
            else:
                return self.pin.value(val)


    def on(self):
        self.value(1)

    def off(self):
        self.value(0)

    def __repr__(self):
        return "Pin({})".format(self.pin.id)


