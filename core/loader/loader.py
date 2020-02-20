
import logging

log = logging.getLogger("LOADER")
log.setLevel(logging.DEBUG)

import sys
from core.asyn.asyn import launch

try:
    import uasyncio as asyncio
except Exception:
    import asyncio as asyncio


class uLoad:

    def __init__(self, env, core, depend):
        self.core = core
        self.mbus = core.mbus
        self.uconf = core.uconf
        self.env = env
        self.depend = depend
        if self.depend:
            self.usub = self.sub_h(topic="module/#", func="_wait_depend")
        else:
            launch(self._activate, "")

    def sub_h(self, topic, func):
        return self.mbus.sub_h(uid=self.env, topic=topic, env=self.env, func=func)

    async def _activate(self):
        self.mbus.pub_h("module", self.env)


    def _wait_depend(self, _id, _key, _pld, _rt):
        # log.debug("[ACT]: id: {}, key: {}, pld: {}, rt: {}".format(_id, _key, _pld, _rt))

        if _pld in self.depend:
            self.depend.remove(_pld)

        if not self.depend and self.usub:
            self.mbus.usub(self.usub)
            launch(self._activate, "")


class uEnv:
    def __init__(self, core):
        self.core = core

    def env(self, env_name=None, env_action=None, env_depend=None):

        env_att = hasattr(self, env_name or "")

        if env_name and not env_att and env_action:
            setattr(self, env_name, env_action(env=env_name, core=self.core, depend=env_depend))
            return True

        elif env_name is None:
            return self.__dict__

        elif env_att:
            return getattr(self, env_name)



class uCore:
    __slots__ = ('__dict__', 'env', 'mbus', 'uconf')

    def __init__(self, mbus, uconf):
        self.mbus = mbus
        self.mbus.core = self
        self.uconf = uconf
        self.part_name = "."
        self.env = uEnv(self).env


class uModule:

    __slots__ = ('mbus', 'uconf', 'core', '_modules')

    def __init__(self, core):

        self.core = core
        self.mbus = self.core.mbus
        self.uconf = self.core.uconf

        self.uconf.from_file("./core/loader/board_mod.json")

        self._modules = {}

    async def module_list(self):
        await self.uconf.call("from_file", "./_conf/_mod.json")


    async def module_schema(self):

        _mod_list = await self.uconf.call("scan_name", "board_mod")

        for name_mod in _mod_list or []:
            _mod = await self.uconf.call("select_one", "board_mod", name_mod, True)

            log.info("Mod Name: {} - active:{}".format(_mod.name, _mod.active))

            if _mod.active:
                self._modules[_mod.name] = _mod.depend
                await self.uconf.call("from_file", "./mod/{}/_schema.json".format(_mod.name))
                log.info("SCH: Loaded")



    async def module_data(self):
        for _mod in self._modules.keys():
            await self.uconf.call("from_file", "./_conf/data_{}.json".format(_mod))



    async def module_act(self):

        for _mod, depend in self._modules.items():

            mod_act = None
            log.info(" MOD: Activate: {} ".format(_mod))

            # import module
            m_path = "{}/mod/{}".format(self.core.part_name, _mod)
            sys.path.append(m_path)
            try:
                import _act_mod as mod_act
                del sys.modules["_act_mod"]
            except Exception as e:
                log.error("MOD: {} - : {}".format(_mod, e))
                pass
            sys.path.remove(m_path)

            # activate module
            if mod_act:
                try:
                    mod_act.init(self.core, depend)
                    log.info(" MOD: Done:     {}".format(_mod))
                except Exception as e:
                    log.error("MOD: {} - : {}".format(_mod, e))
                    pass


