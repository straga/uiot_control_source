from core.loader.loader import uLoad

import logging
log = logging.getLogger("SWITCH")
log.setLevel(logging.INFO)

from core.asyn.asyn import launch

from .switch import Switch

class SwitchAction(uLoad):

    async def _activate(self):

        self.sw_list = {}
        self.mbus.pub_h("module", "switch")


    async def get_switch(self, sw_name):

        switch = False

        if sw_name in self.sw_list:
            switch = self.sw_list[sw_name]
        else:
            #Get switch object
            switch_obj = await self.uconf.call("select_one", "switch_cfg", sw_name, obj=True)
            #Get pin_env from env
            pin_env = self.core.env("pin")
            if switch_obj and pin_env:
                #Make hardware pin
                switch_pin = await pin_env.get_pin(pin_name=switch_obj.pin)
                if switch_pin:
                    #Make switch
                    switch = Switch(pin=switch_pin, name=switch_obj.name)
                    switch.cb = self.cb
                    self.mbus.pub_h("switch/{}/init".format(switch_obj.name), [switch_obj.pin])
                    self.sw_list[switch_obj.name] = switch

                    #Restore mode
                    if switch_obj.restore is not None:
                        if switch_obj.restore == "ON":
                            switch.change_state(1)
                        elif switch_obj.restore == "OFF":
                            switch.change_state(0)
                        elif switch_obj.restore == "STATE":
                            switch.restore = True
                            switch.change_state(switch_obj.state)

        return switch

    async def save_stage(self, switch):
        switch_obj = await self.uconf.call("select_one", "switch_cfg", switch.name, obj=True)
        switch_obj.state = switch.state
        await switch_obj.update()

    def cb(self, sw):
        self.mbus.pub_h("switch/{}/state".format(sw.name), sw.get_state(), retain=True)
        if sw.restore:
            launch(self.save_stage, (sw,))

















