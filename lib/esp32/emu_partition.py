

# # Constructors
# Partition(Partition.FIRST, type=Partition.TYPE_APP)
# Partition(Partition.FIRST, type=Partition.TYPE_DATA)
# Partition(Partition.FIRST, type=Partition.TYPE_DATA, subtype=2, label='nvs')
# Partition(Partition.BOOT) # get boot partition
# Partition(Partition.RUNNING) # get currently running partition
#
# # Methods
# part.info() # returns a 6-tuple of (type, subtype, addr, size, label, encr)
# part.readblocks(block_num, buf)
# part.writeblocks(block_num, buf)
# part.eraseblocks(block_num, size)
# part.set_boot() # sets current as bootable, for next reset
# part.get_next_update() # returns new Partition
#
# app_parts = Partition.find(Partition.TYPE_APP)
# data_parts = Partition.find(Partition.TYPE_DATA)
# nvs_parts = Partition.find(Partition.TYPE_DATA, label='nvs')
#
#
# from esp32 import Partition
# bootpart = Partition(Partition.BOOT)
# runningpart = Partition(Partition.RUNNING)
# fatfs = Partition('fatfs')


class Partition:

    TYPE_DATA = 4
    TYPE_APP = 5
    BOOT  = 6
    RUNNING = 6


    def __init__(self, id, type=None, subtype=None, label=None):

        self.id = id
        self.type = type
        self.subtype = subtype
        self.label = label

    @classmethod
    def find(cls, type=TYPE_APP, subtype=0xff, label=None):
        return[
            Partition(Partition.BOOT)
        ]

    def info(self):
        type = Partition.TYPE_DATA
        subtype = 2
        addr = 5000
        size = 2000
        label = "factory"
        encrypted = 0
        return (type, subtype, addr, size, label, encrypted)



    def readblocks(self, block_num, buf):
        pass

    def readblocks(self, block_num, buf, offset):
        pass

    def writeblocks(self, block_num, buf):
        pass

    def writeblocks(self, block_num, buf, offset):
        pass

    def ioctl(self, cmd, arg):
        pass

    def set_boot(self):
        pass

    def get_next_update(self):
        pass

