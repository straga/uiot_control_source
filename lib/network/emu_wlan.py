from random import randint

class WLAN:

    def __init__(self, wtype):

        self.wtype = wtype
        self.status = False
        self.enable = False


    def active(self, active):
        self.enable = active


    def isconnected(self):
        return self.status

    @staticmethod
    def r_snr():
        return -1 * randint(30, 90)

    def scan(self):

        scan_result = [
            (b'TP-LINK_6555', b'4\xce\x00\x1c\x0e\x04', 5, self.r_snr(), 4, False),
            (b'TP-LINK_0942', b'4\xce\x00\x1c\x0e\x04', 5, self.r_snr(), 4, False),
            (b'TP-LINK_8842', b'\xd4n\x0e\xd6\xe3l',    5, self.r_snr(), 3, False),
            (b'TP-LINK_6642', b'\x8c\rv\xfb\x1dB',      1, self.r_snr(), 3, False),
            (b'TP-LINK_4542', b'\xd4n\x0e\xd6\xc2|',    9, self.r_snr(), 3, False),
            (b'TP-LINK_6542', b'\xf4\xf2moeB',          2, self.r_snr(), 3, False)
                     ]

        return scan_result

    def ifconfig(self):
        # import socket
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.connect(("8.8.8.8", 80))
        # _ip = s.getsockname()[0]
        # s.close()
        _ip = "127.0.0.1"

        return (_ip, '255.255.255.0', '127.0.0.1', '8.8.8.8')

    def disconnect(self):
        self.status = False

    def connect(self, ssid=None, password=None, *, bssid=None):
        self.status = True


    def config(self, essid=None, authmode=None, password=None, channel=None, hidden=False, dhcp_hostname=None):
        """"

        "essid": "uPy-Dev-8888888",
        "channel": 11,
        "hidden": false,
        "password": "12345678",
        "authmode": 3

        """
        pass
