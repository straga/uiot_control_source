from core.loader.loader import uLoad
# from .mqtt.mqtt import MQTTClient

from .mqtt.client import MQTTClient

import logging
log = logging.getLogger("MQTT")
log.setLevel(logging.INFO)

try:
    import ujson as json
except Exception:
    import json
    pass

class MQTTAction(uLoad):

    async def _activate(self):

        self.brocker_name = "MQTT"

        mqtt_cfg = await self.uconf.call("select", "mqtt_cfg", rtype="obj", active=True)
        board = await self.uconf.call("select_one", "board_cfg", "default", True)

        if mqtt_cfg and board:

            self.client_pub = board.topic
            self.mqtt = MQTTClient(client_id=board.uid, addr=mqtt_cfg.addr, port=mqtt_cfg.port)

            self.client_sub = "{}/{}".format(self.client_pub, self.brocker_name)

            self.mqtt.add_sbt(tpc="{}/#".format(self.client_sub))
            self.mqtt.set_callback(self.mqtt_cb)

            self.sub_h("ALL", "mbus_act")  # short
            # self.mbus.sub_h("MQTT-ALL", "ALL", self.env, "mbus_act") # direct

            #MQTT playload decoder
            self.core.mbus.MQTT = self.MQTT_decode

            self.mqtt.start()
            self.mbus.pub_h("module", "mqtt")


    # Publish from mqtt to mbus
    def mqtt_cb(self, topic, msg, retain):
        tpc_list = topic.rsplit(self.client_sub + "/", 1)
        self.core.mbus.pub_h(tpc_list[-1], msg, brk=self.brocker_name, retain=retain)


    # Publish from mbus to mqtt
    def mbus_act(self, _id, _key, _pld, _rt):

        log.debug("[MQTT-MBUS]: _id:{}, _key:{}, _pld:{}, _rt:{} ->mqtt".format(_id, _key, _pld, _rt))

        if _id not in [self.brocker_name, "private"]:

            val = {
                    "tp": "{}/{}/{}".format(self.client_pub, _id, _key), #topic gen
                    "msg": _pld,  #play load -> message
                    "rt": _rt #retain
                   }
            self.mqtt.pub(val)


    #MQTT playload decoder
    def MQTT_decode(self, msg):
        log.debug("[brk MQTT]: {}".format(msg))

        # decode
        try:
            msg["pld"] = msg["pld"].decode()
        except Exception as e:
            log.debug("[brk MQTT decode]: {}".format(e))
            pass

        # from json to python
        try:
            msg["pld"] = json.loads(msg["pld"])
        except Exception as e:
            log.debug("[brk MQTT decode]: {}".format(e))
            pass

        return msg


