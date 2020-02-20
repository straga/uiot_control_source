class I2C:

    OUT = 4
    IN = 5
    PULL_UP = 6
    PULL_DOWN = 6

    def __init__(self, id=-1, *, sda=None, scl=None, freq=400000):

        self.sda = sda
        self.scl = scl

    def scan(self):
        print("I2C: {} - {} : scnan".format(self.sda, self.scl))
        return [126, 125, 127]
