
import network

try:
    import uasyncio as asyncio
except Exception:
    import asyncio as asyncio


import logging
log = logging.getLogger("WIFI")
log.setLevel(logging.DEBUG)

from core.asyn.asyn import launch

class WIFIRun:

    def __init__(self, core):
        self.core = core

        self.sta = STA(core=self.core)
        self.scan_ap = self.sta.scan_ap
        self.ap = None
        self.ap_activate()
        self._run = False


    def ap_activate(self):

        if not self.sta.ip and not self.ap:
            self.ap = AP(core=self.core)
            launch(self.ap.start, "")
        elif self.ap and self.ap.net.active():
            self.ap.stop()
        elif self.ap and not self.ap.net.active():
            self.ap = None


    async def _keepalive(self):

        while self._run:
            sleep = await self.sta.sta_keepalive()

            if self.sta.loss > 10:
                log.debug("Loss: {}".format(self.sta.loss))
                self.sta.loss = 0
                try:
                    await asyncio.wait_for(self.sta.connect(), 30)
                except asyncio.TimeoutError:
                    log.debug("timeout!: STA")
                    pass

            self.ap_activate()

            await asyncio.sleep(sleep)


    def start(self):
        if not self._run:
            self._run = True
            launch(self._keepalive, "")
            log.info("WIFI Coro Start")


# Access Point
class AP:

    def __init__(self, core):

        self.mbus = core.mbus
        self.uconf = core.uconf

        self.net = network.WLAN(network.AP_IF)
        self.ip = None
        self.delay = 120
        self.stop_progres = False



    async def start(self):

        if not self.ip:
            self.net.active(True)
            config = await self.uconf.call("select", "wifi_ap_cfg", rtype="obj", active=True)

            log.debug("AP CONFIG: {}".format(config.name))

            if config:
                try:
                    self.net.config(essid=config.essid, password=config.password, authmode=config.authmode,
                                    channel=config.channel)
                    self.delay = config.delay
                    self.ip = self.net.ifconfig()[0]
                    self.mbus.pub_h("wifi/ap/ip/set", self.ip)
                    self.mbus.pub_h("module", "net")

                except Exception as e:
                    log.error("AP CONFIG: {}".format(e))
                    self.net.active(False)
                    return




    async def _stop(self):
        self.stop_progres = True
        await asyncio.sleep(self.delay)
        self.ip = None
        self.net.active(False)
        self.mbus.pub_h("wifi/ap/ip/set", None)
        self.stop_progres = False


    def stop(self):
        if not self.stop_progres:
            launch(self._stop, "")



# Connect to AP
class STA:

    def __init__(self, core):

        self.core = core
        self.mbus = self.core.mbus
        self.uconf = self.core.uconf

        self.net = network.WLAN(network.STA_IF)
        self._activate()

        self.loss = 0
        self.ip = None

        self._run = False

    def _activate(self):

        self.net.active(True)
        self.net.config(dhcp_hostname=self.core.board.hostname)

    async def connect(self):

        self.net.disconnect()

        if self.ip is not None:
            self.ip = None
            self.mbus.pub_h("wifi/sta/ip/set", self.ip)


        configs = await self.uconf.call("select", "wifi_sta_cfg", active=True)

        if configs:
            ap_names = self.scan_ap()
            log.debug("STA: ap_names: {}".format(ap_names))

            for config in configs:
                ap_conf = await self.uconf.call("model", "wifi_sta_cfg", config)
                log.debug("STA: SSID =  {}".format(ap_conf.ssid))

                if ap_conf.ssid in ap_names:
                    self.net.connect(ap_conf.ssid, ap_conf.passwd)
                    log.debug("STA: connect to: {}".format(ap_conf.ssid))
                    await asyncio.sleep(15)
                    if await self.sta_keepalive() == 10:
                        break



    async def sta_keepalive(self):

        if self.net.isconnected():
            self.loss = 0
            sleep = 10
            ip = self.net.ifconfig()[0]

            if ip != self.ip:
                self.ip = ip
                self.mbus.pub_h("wifi/sta/ip/set", self.ip)
                self.mbus.pub_h("module", "net_sta")
        else:
            self.loss += 1
            sleep = 1

        return sleep

    def scan_ap(self, slist=False):

        if slist:
            data = []
            try:
                for ap in self.net.scan():
                    val = {
                        "ssid": ap[0].decode(),
                        "bssid": "",
                        "channel": ap[2],
                        "RSSI": ap[3],
                        "authmode": ap[4],
                        "hidden": ap[5]
                        }
                    data.append(val)

            except Exception as e:
                log.error("WiFi SCAN AP: {}".format(e))
                pass

            return {
                "head": ("ssid", "bssid", "channel", "RSSI", "authmode", "hidden"),
                "data": data,
                "options": "simple"
            }
        else:

            ap_names = []
            try:
                res = self.net.scan()
                for ap in res:
                    ap_names.append(ap[0].decode())
            except Exception as e:
                log.error("scan: {}".format(e))
                pass
            return ap_names


