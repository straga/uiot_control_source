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



    def select(self, sch_name, rtype=None, **kwargs):
        if self.schema_conf_init(sch_name):
            if rtype is None:
                return self.store.select(**kwargs)
            elif rtype == "obj":
                #first in where
                for res in self.store.select(**kwargs):
                    return self.model(sch_name, res )
            elif rtype == "list":
                r_list=[]
                for res in self.store.select(**kwargs):
                    r_list.append(res)
                return r_list



    def select_one(self, sch_name, cfg_name, obj=False):
        if self.schema_conf_init(sch_name):
            result = self.store.select_one(cfg_name)
            if obj:
                result = self.model(sch_name, result)
            return result


    def scan(self, sch_name):

        if self.schema_conf_init(sch_name):
            return self.store.scan()


    def scan_name(self, sch_name):

        if self.schema_conf_init(sch_name):
            return self.store.scan_name()


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



    #
    #     self.sch_detect()
    #
    # def sch_detect(self):


    #     self._config = None
    #     self._config_name = None
    #
    #     if self._config:
    #         self.mbus = self._config.core.mbus
    #         self.core = self._config.core
    #         self.name = self._config_name
    #
    #
    # async def write(self, **kwargs):
    #
    #     if self._config:
    #
    #         return await self._config.update({"name": self.name}, **kwargs)










    #
    # def sch_load(self, name):
    #     pass
    #
    # def sch_validate(self, sch, data):
    #     pass

    # def sch_save(self, sch_name=None, sch_conf=None):
    #
    #     if not sch_name:
    #         sch_name = self._sch
    #         sch_conf = self._sch_conf
    #     self.store.__schema__ = sch_name
    #     self.store.__config__ = sch_conf
    #     self.store.create_schema()
    #
    #     log.debug("SCH SAVE: {},  {}".format(sch_name, sch_conf))
    #
    # def sch_load(self, name):
    #     pass
    #
    # def sch_validate(self, sch, data):
    #     pass

# import builtins
# rt = getattr(builtins, "str")()

    # def mod_get(self, m_name):
    #     self.tbl_add()
    #     if self._tbl == m_name:
    #         return self._sch
    #
    #     s_mod = self.mod_sel(m_name)
    #     if len(s_mod):
    #         sch = OrderedDict(s_mod[0]["sch"])
    #         self.tbl_add(s_mod[0]["name"], sch)
    #         return sch
    #     return False
    #
    #
    # def tbl_add(self, tb_name=None, tb_sch=None):
    #     if not tb_name:
    #         tb_name = self._tbl
    #         tb_sch = self._sch
    #     self.model.__table__ = tb_name
    #     self.model.__schema__ = tb_sch
    #     self.model.create_table()
    #     log.debug("TBL SELECT: {},  {}".format(tb_name, tb_sch))
    #
    # def mod_sel(self, m_name):
    #     self.tbl_add()
    #     return list(self.model.select(name=m_name))
    #
    # def mod_add(self, tb_name, tb_sch, **fields):
    #
    #     self.tbl_add(tb_name, tb_sch)
    #     self.tbl_add()
    #     log.debug("MOD ADD: {} {}".format(tb_name, tb_sch))
    #     if not len(self.mod_sel(tb_name)):
    #         log.debug("CREATE MODEL: {}".format( tb_name ))
    #
    #         self.model.create(name=tb_name, sch=list(tb_sch.items()), **fields)
    #
    #
    #
    #
    #
    # def _call_cmd(self, method, table, *args, **kwargs):
    #
    #     result = []
    #     if hasattr(self, method):
    #
    #         try:
    #             func = getattr(self, method)
    #             res = func(table, *args, **kwargs)
    #
    #             if res:
    #
    #                 if not isinstance(res, (list, tuple, dict)):
    #                     res = list(res)
    #
    #                 if len(res):
    #                     result = res
    #
    #         except Exception as e:
    #             log.debug("Err : {}, {}, {}, {}, {}".format(e, method, table, args, kwargs))
    #             pass
    #
    #     return result
    #
    # def data_load(self, table, **kwargs):
    #     self._call_cmd("_add", table, **kwargs)
    #
    #
    #
    # async def call_db(self, method, table, *args, **kwargs):
    #
    #     await lock.acquire()
    #
    #     # result = await run_in_executer(self._call_cmd, method, table, *args, **kwargs)
    #
    #     result = self._call_cmd(method, table, *args, **kwargs)
    #
    #     lock.release()
    #
    #     return result
    #
    #
    #
    #
    # def _add(self, mod_name, **fields):
    #
    #     if self.mod_get(mod_name):
    #         return self.model.create(**fields)
    #
    #     return False
    #
    #
    # def _scan(self, mod_name, **kwargs):
    #     if self.mod_get(mod_name):
    #         return self.model.scan()
    #
    # def _scan_name(self, mod_name, **kwargs):
    #     if self.mod_get(mod_name):
    #         return self.model.scan_name()
    #
    # def _scan_db(self, mod_name, **kwargs):
    #     return self.model.scan_db()
    #
    # def _scan_head(self, mod_name, **kwargs):
    #     sch = self.mod_get(mod_name)
    #     if sch:
    #         return {
    #             "head": list(sch),
    #             "data": list(self.model.scan())
    #         }
    #
    # def _sel(self, mod_name, **fields):
    #     if self.mod_get(mod_name):
    #         return list(self.model.select(**fields))
    #
    #
    # def _upd(self, mod_name, where, **fields):
    #     if self.mod_get(mod_name):
    #         return self.model.update(where, **fields)
    #
    # def _del(self, mod_name, where, **kwargs):
    #     if self.mod_get(mod_name):
    #         return self.model.delete(where)
    #
    #
    # def _by_id(self, mod_name, pkey):
    #     if self.mod_get(mod_name):
    #         return self.model.get_id(pkey)
    #
    #
    # def _sel_one(self, mod_name, **fields):
    #
    #     rcds = self._sel(mod_name, **fields)
    #
    #     if rcds and len(rcds):
    #         return rcds[0]
    #     else:
    #         return False











