# Copyright (c) 2020 Viktor Vorobjov

from . import json_store as uorm

try:
    import uasyncio as asyncio
    from ucollections import OrderedDict
    import ujson

except ImportError:
    from collections import OrderedDict
    import json as ujson
    import asyncio

from core.asyn.asyn import Lock
lock = Lock()


#from core.asyn.asyn import run_in_executer

import logging
log = logging.getLogger("CONF")
log.setLevel(logging.INFO)


class ConfigManager:
    # __slots__ = ('__dict__', 'db', '_tbl', '_sch')

    def __init__(self, store="u_config"):

        self.store = uorm.Store
        self.store.__store__ = store

        self._sch_name = "_schema"
        self.store.__schema__ = self._sch_name

        self._sch_conf = OrderedDict([
            ("name", ("str", "")),
            ("sch", ("dict", ())),
        ])

        # store
        self.store.check_dir(store=True)
        # schema
        self.store.check_dir()


    def schema_init(self, sch_name=None):

        if sch_name and sch_name != self._sch_name:
            sch_name = sch_name
        else:
            sch_name = self._sch_name

        self.store.__schema__ = sch_name
        self.store.check_dir()



    def schema_conf_init(self, sch_name=None):

        if sch_name and self.store.__schema__ == sch_name and hasattr(self.store, "__config__"):
            log.debug("CONF SCH: HAS {}".format(sch_name))
            return True

        self.schema_init()
        sch_conf = self._sch_conf

        if sch_name and sch_name != self._sch_name:
            sch_conf = False
            sch_obj = self.store.select_one(sch_name)
            if sch_obj:
                sch_conf = OrderedDict(sch_obj["sch"])
                self.schema_init(sch_name)

        # log.debug("CONF SCH: {}".format(sch_conf))

        if sch_conf:
            self.store.__config__ = sch_conf
            # self.store.__keys__ = list(sch_conf)
            log.debug("CONF SCH: {}".format(sch_name))
            return True


    def delete(self, sch, where):
        if self.schema_conf_init(sch):
            return self.store.delete(where)


    def save_data(self, data):

        if "_schema" in data:
            log.debug("SAVE DATA: {}".format(data["_schema"]))

            if self.schema_conf_init(data["_schema"]):
                self.store.write(data)


    def from_dict(self, sch, name, data):
        data["name"] = name
        data["_schema"] = sch
        data["_upd"] = True
        self.save_data(data)


    def from_file(self, file):

        for data in self.store.from_file(file).values():
            self.save_data(data)


    def from_string(self, json_string):

        try:
            json_data = ujson.loads(json_string)
        except Exception as e:
            log.error("Error: from string: {}".format(e))
            return False

        for data in json_data.values():
            self.save_data(data)


    def model(self, sch_name, result ):
        if result:
            return ObjModel(result, _schema=sch_name, _config=self)


    def select(self, sch_name, rtype="list", **kwargs):
        if self.schema_conf_init(sch_name):

            if rtype == "list":
                return self.generate_list(self.store.select(**kwargs))

            elif rtype == "obj":
                #first in where
                for res in self.store.select(**kwargs):
                    return self.model(sch_name, res)


    def select_one(self, sch_name, cfg_name, obj=False):
        if self.schema_conf_init(sch_name):
            result = self.store.select_one(cfg_name)
            if obj:
                result = self.model(sch_name, result)
            return result


    def scan(self, sch_name):

        if self.schema_conf_init(sch_name):
            return self.store.scan()


    @staticmethod
    def generate_list(generator):
        r_list = []
        for res in generator:
            r_list.append(res)
        return r_list


    def scan_name(self, sch_name):

        if self.schema_conf_init(sch_name):
            return self.generate_list(self.store.scan_name())


    def _call_cmd(self, method, param, *args, **kwargs):

        result = None
        if hasattr(self, method):

            try:
                func = getattr(self, method)
                result = func(param, *args, **kwargs)

            except Exception as e:
                log.error("Err : {}, {}, {}, {}, {}".format(e, method, param, args, kwargs))
                pass

        return result

    async def call(self, method, param, *args, **kwargs):
        async with lock:
            result = self._call_cmd(method, param, *args, **kwargs)
        return result


class ObjModel:

    def __init__(self, *args, **kwargs):

        self._schema = None
        self._config = None

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    async def update(self):
        if self._schema and self._config:
            self._upd = True
            await self._config.call("save_data", self.__dict__)


