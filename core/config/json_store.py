# Copyright (c) 2020 Viktor Vorobjov

try:
    import uos
    import utime
    import ujson
    from ucollections import OrderedDict
    from uos import ilistdir as _isdir
    # from uos import listdir as listdir

except Exception:

    import os as uos
    import time as utime
    from collections import OrderedDict
    import json as ujson
    from os.path import isdir as _isdir
    # from os import listdir
    pass

import builtins

import logging
log = logging.getLogger("FJSON")
log.setLevel(logging.INFO)


def isdir(dir_path):
    try:
        if _isdir(dir_path):
            return True
        else:
            return False
    except OSError as e:
        log.debug("IS DIR: {} - {}".format(e, dir_path))
        return False


def isfile(file_path):
    try:
        if uos.stat(file_path)[6]:  # size more 0
            return True
        else:
            return False
    except OSError as e:
        log.debug("IS FILE: {} - {}".format(e, file_path))
        return False


def exists(path):
    result = False

    if isdir(path):
        result = "dir"
    elif isfile(path):
        result = "file"

    return result


class Store:

    @classmethod
    def path_to_store(cls):
        return "{}".format(cls.__store__)



    @classmethod
    def path_to_schema(cls):
        return "{}/{}".format(cls.__store__, cls.__schema__)



    @classmethod
    def path_to_config(cls, config):
        return "{}/{}/{}".format(cls.__store__, cls.__schema__, config)



    @classmethod
    def list_dir(cls, path):
        try:
            return uos.listdir(path)
        except OSError as e:
            log.debug("LSDIR: {}".format(e))
            return None



    @classmethod
    def create_dir(cls, name):
        try:
            uos.mkdir(name)
        except OSError as e:
            log.debug("MKDIR: {}, {}".format(e, name))
            return False
        log.info("MKDIR: {}".format(name))
        return True



    @classmethod
    def check_dir(cls, store=None):

        if store:
            _path = cls.path_to_store()
        else:
            _path = cls.path_to_schema()

        if not isdir(_path):
            cls.create_dir(_path)


    @staticmethod
    def default(default):
        if callable(default):
            default = default()
        return default


    @staticmethod
    def str2bool(val):
        return val.lower() in ("yes", "true", "1")

    @classmethod
    def validate(cls, cfg):
        '''
            val[0] = type
            val[1] = default value
        '''
        remove = [k for k in cfg.keys() if k.startswith("_")]
        for k in remove:
            del cfg[k]

        for key, val in cls.__config__.items():

            _type = getattr(builtins, val[0])

            if key not in cfg:
                cfg[key] = cls.default(val[1])

            elif type(cfg[key]) != _type and not callable(val[1]):

                try:
                    if val[0] == "bool":
                        cfg[key] = cls.str2bool(cfg[key])
                    else:
                        cfg[key] = _type(cfg[key])
                except Exception as e:
                    log.error("VALIDATE:{}".format(e, ))
                    cfg[key] = cls.default(val[1])
                    pass

        # log.debug("VALIDATE: {}".format(cfg))
        log.debug("VALIDATE: {}".format("OK"))
        return cfg



    @classmethod
    def from_file(cls, file):
        result = {}
        if isfile(file):
            with open(file) as f:
                try:
                    fc = f.read()
                    result = ujson.loads(fc)
                except Exception as e:
                    log.error("Error: from file: {} - {}".format(file, e, ))
                    pass

        return result



    @classmethod
    def write(cls, config):

        if "name" in config:

            _name = config["name"]
            _upd = None
            if "_upd" in config:
                _upd = config["_upd"]

            mode = False
            is_file = isfile(cls.path_to_config(_name))

            if not is_file:
                mode = "w"
            elif _upd:
                mode = "w+"
                new_config = cls.select_one(_name)
                if new_config:
                    del config["name"]
                    new_config.update(config)
                    config = new_config

            if _upd is not None and not _upd:
                mode = False

            log.debug("Mode: {},  path:{}".format(mode, cls.path_to_config(_name)))

            if mode:
                cls.validate(config)
                with open(cls.path_to_config(_name), mode) as f:
                    f.write(ujson.dumps(config))



    @classmethod
    def select_one(cls, cfg):
        if isfile(cls.path_to_config(cfg)):
            with open(cls.path_to_config(cfg)) as f:
                f_cfg = f.read()
                if f_cfg:
                    return ujson.loads(f_cfg)


    @classmethod
    def select(cls, **fields):

        for cfg_name in cls.list_dir(cls.path_to_schema()):

            with open(cls.path_to_config(cfg_name)) as f:
                f_cfg = f.read()
                if f_cfg:
                    row = ujson.loads(f_cfg)

                    for key in cls.__config__:
                        if key in fields and key in row:
                            if row[key] == fields[key]:
                                yield row


    @classmethod
    def scan(cls):
        _list = []
        for cfg_name in cls.list_dir(cls.path_to_schema()):
            _list.append(cls.select_one(cfg_name))

        return _list



    @classmethod
    def scan_name(cls):
        for file_name in cls.list_dir(cls.path_to_schema()):
            yield file_name



    @classmethod
    def scan_store(cls):
        for file_name in cls.list_dir(cls.path_to_store()):
            yield file_name


    @classmethod
    def delete(cls, where):

        _name = "name"

        if len(where) == 1 and _name in where:
            uos.remove(cls.path_to_config(where[_name]))
            return True

