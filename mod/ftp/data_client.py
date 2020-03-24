import logging
log = logging.getLogger("FTP")
log.setLevel(logging.INFO)

try:
    import uasyncio as asyncio
    from core.platform import upy_aclose as _aclose

except Exception:
    import asyncio as asyncio
    from core.platform import pc_aclose as _aclose


class FtpDataClient:
    def __init__(self, config):
        self.config = config
        self.port_id = []

    async def data_server(self, reader, writer):

        addr = writer.get_extra_info('peername')
        log.debug("(   ")
        log.info("  + Data Server <- client from {}".format(addr))
        log.debug("  s2. Data Server = Open")

        port_id = False
        await asyncio.sleep(0.5)

        try:
            port_id = self.port_id.pop(0)
        except Exception as e:
            log.info("  port_id {}".format(e))
            pass

        if port_id:
            request = self.config.get_request(port_id)

            log.debug("    ID: {}".format(port_id))
            log.debug("    Start Request: {}".format(request.data_start))
            log.debug("    Request Transfer: {}".format(request.transfer))

            while True:
                if request.transfer:

                    if request.transfer is "LIST":
                        log.debug("      Activate: List Dir")
                        await self.config.data_store.send_list_data(request, writer)
                        request.transfer = False

                    elif request.transfer is "SEND":
                        log.debug("      Activate: Send File")
                        await self.config.data_store.send_file_data(request, writer)
                        request.transfer = False

                    elif request.transfer is "SAVE":
                        log.debug("      Activate: Save File")
                        await self.config.data_store.save_file_data(request, reader)
                        request.transfer = False

                    elif request.transfer:
                        log.debug("      Activate: State Start")
                        # Time for wait Open Socker Activite if not active = Close connection
                        await asyncio.sleep(0.5)
                        request.transfer = False

                else:
                    request.data_start = False
                    break

        await _aclose(writer)
        log.info("  - Data Server <- client from {}".format(addr))
        log.debug("  s2. Data Server = Close")
        log.debug(")")


