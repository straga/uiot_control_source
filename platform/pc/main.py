
import sys

part_name = "."

sys.path.append("{}/".format(part_name))
sys.path.append("{}/{}".format(part_name, "lib"))
sys.path.append("{}/{}".format(part_name, "app"))

import _thread
import asyncio

from core.mbus.mbus import MbusManager
from core.config.config import ConfigManager

import logging

log = logging.getLogger('MAIN')
logging.basicConfig(level=logging.DEBUG)


# from core.umod.config import uTable
#
# class MAIN(uTable):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.part_name = "."
#         self.core.mbus.sub_h(uid="MAIN", topic="ALL", env=self.env, func="print_mbus")
#
#     def print_mbus(self, *msg):
#         print("MAIN: {}".format(msg))
#
# g_core.env["main"] = MAIN(tb_name="cfg_main", env="main", core=g_core)


async def loader(core_mbus, core_conf):

    from core.loader.loader import uCore
    from core.loader.loader import uModule

    log.info("CORE: init")
    global g_core
    g_core = uCore(core_mbus, core_conf)
    g_core.part_name = part_name

    log.info("Module: Init")
    _umod = uModule(g_core)

    log.info("Module: List")
    await _umod.module_list()

    log.info("Module: Schema")
    await _umod.module_schema()

    log.info("Module: Data")
    await _umod.module_data()

    log.info("Module: Act")
    await _umod.module_act()


def main():

    # AsyncIO
    loop = asyncio.get_event_loop()
    _ = _thread.stack_size(100 * 1024)

    # MBUS
    log.info("MBUS START")
    _mbus = MbusManager()
    _mbus.start()

    # CONF
    log.info("CONF START")
    _conf = ConfigManager("./u_config")

    _thread.start_new_thread(loop.run_forever, ())

    # loop.set_debug(True)
    loop.create_task(loader(_mbus, _conf))


def clean_emu():

    import os
    from pathlib import Path
    folder = './u_emu'

    _folder = Path(folder)
    if not _folder.exists():
        _folder.mkdir()


    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)



if __name__ == '__main__':
    log.info("MAIN")

    log = logging.getLogger("FJSON")
    log.setLevel(logging.DEBUG)


    log = logging.getLogger("CONF")
    log.setLevel(logging.DEBUG)


    log = logging.getLogger("LOADER")
    log.setLevel(logging.DEBUG)

    log = logging.getLogger("MBUS")
    log.setLevel(logging.DEBUG)


    clean_emu()
    main()

