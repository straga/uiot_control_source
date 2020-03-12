path = "u_emu"
import os as uos
try:
    uos.mkdir(path)
except OSError as e:
    pass

class Pin_state:

    def __init__(self):
        self.path = path


    def write_value(self, name, value):

        with open("{}/pin_{}".format(self.path, name), "w") as file:
            file.write('{}'.format(value))


    def read_value(self, name):

        value = 0
        try:
            with open("{}/pin_{}".format(self.path, name), "r") as file:
                value = file.readline()
        except Exception as ex:
            self.write_value(name, value)
            print(ex)
            pass

        try:
            return int(value)
        except Exception as ex:
            print(ex)
            return 0


    def scan_emu(self):

        try:
            return uos.listdir(self.path)
        except OSError as e:
            print(e)
            return []
            pass

    def list_emu(self):
        _value = {}
        for scan in self.scan_emu():
            _value[scan] = self.read_value(scan)


