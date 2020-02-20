
import sys

part_name = "."

sys.path.append("{}/".format(part_name))
sys.path.append("{}/{}".format(part_name, "lib"))

import asyncio
import _thread

import logging
log = logging.getLogger('TEST')
logging.basicConfig(level=logging.DEBUG)


from core.config.config import ConfigManager
from utests.core_config.test import config_simple, config_async


g_config = ConfigManager("./u_test")


async def loader(g_config):

    await config_async(g_config)

async def killer():
    await asyncio.sleep(10)

def test_simple():

    config_simple(g_config, "./utests/core_config/json_data")


def test_async(loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    loop.create_task(loader(g_config))
    loop.run_until_complete(killer())
    loop.close()


def test_thread():

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    _ = _thread.stack_size(100 * 1024)

    _thread.start_new_thread(test_async, (loop,))

if __name__ == '__main__':

    log.warning("SIMPLE")
    test_simple()

    log.warning("ASYNC")
    test_async()

    log.warning("THREAD")
    test_thread()


