#t

import logging
log = logging.getLogger("PLATFORM_PC")
log.setLevel(logging.INFO)

#PC
async def pc_aclose(writer):
    try:
        await writer.close()
    except Exception as e:
        log.debug("close: {}".format(e))
        pass


async def pc_awrite(writer, data, b=False):
    try:
        if not b:
            data = data.encode('utf-8')

        writer.write(data)
        await writer.drain()
    except Exception as e:
        log.debug("Error1: awrite: {}".format(e))
        pass


def pc_buffer(default=1024):
    return bytearray(default)


async def pc_buffer_writer(awrite, writer, buf, x):
    await awrite(writer, buf, True)



# _try_alloc_byte_array

