# import logging
# log = logging.getLogger("HTTP-FLASH-ROUTE")
# log.setLevel(logging.DEBUG)


class Handler:

    def __init__(self, core):

        self.core = core
        self.route_handler = ("/flash", "POST", self._handler)


    async def _handler(self, request):

        result = False
        ota = self.core.env("ota_upd")
        if ota:
            _updater = ota.OtaUpdater()
            ota.status = _updater.get_status
            result = await _updater.update(request)

        if result:
            await request._response.return_ok()
            return True
        else:
            return False
