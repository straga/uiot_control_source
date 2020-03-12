
import uasyncio as asyncio
import machine, _thread
import uos
import gc

# WDT
async def run_wdt():
    wdt = machine.WDT(timeout=120000)
    print("WDT RUN")
    while True:
        wdt.feed()
        gc.collect()
        # print("WDT RESET")
        await asyncio.sleep(10)

# Lloader
async def loader():

    # VFS SIZE
    fs_stat = uos.statvfs('/')
    fs_size = fs_stat[0] * fs_stat[2]
    fs_free = fs_stat[0] * fs_stat[3]
    print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))

    part_name = uos.getcwd()
    print(part_name)
    #Import
    from core.mbus.mbus import MbusManager
    from core.config.config import ConfigManager

    # MBUS
    print("MBUS START")
    _mbus = MbusManager()
    _mbus.start()

    # CONF
    print("CONF START")
    _conf = ConfigManager("./u_config")


    # Core/Modules
    from core.loader.loader import uCore
    from core.loader.loader import uModule

    print("CORE: init")
    global g_core
    g_core = uCore(_mbus, _conf)
    g_core.part_name = part_name

    print("Module: Init")
    _umod = uModule(g_core)

    print("Module: List")
    await _umod.module_list()

    print("Module: Schema")
    await _umod.module_schema()

    print("Module: Data")
    await _umod.module_data()

    print("Module: Act")
    await _umod.module_act()

    _ = _thread.stack_size(4 * 1024)




def main():

    loop = asyncio.get_event_loop()
    _ = _thread.stack_size(8 * 1024)
    _thread.start_new_thread(loop.run_forever, ())

    # loop.set_debug(True)

    loop.create_task(run_wdt())
    loop.create_task(loader())



if __name__ == '__main__':

    print("MAIN")
    main()


    #if error - run manualy in UART:
    # import network
    # sta = network.WLAN(network.STA_IF)
    # sta.active(True)
    # sta.connect("ssid", "psswd")
    #
    # import ftp
    # ftp.ftpserver()


    # from esp32 import Partition
    # ota_0 = Partition('ota_0')
    # Partition.set_boot(ota_0)

    # import _thread
    # _thread.stack_size(4 * 1024)





