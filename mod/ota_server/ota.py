
try:

    import uasyncio as asyncio

except Exception:

    import asyncio as asyncio


import logging

log = logging.getLogger("OTA_SERVER")
log.setLevel(logging.DEBUG)


from core.asyn.asyn import launch

class OtaClient:

    def __init__(self, http):

        self.http = http
        self.board = "esp32_test"
        self.test()

    async def run(self):

        addr = "http://127.0.0.1"
        port = "8080"

        url = "{}:{}/rpc".format(addr, port)

        # mqtt_host = await self.umod.call_db("_sel", "cfg_mqtt", type="default")

        _fields = {
            "board": "esp32"
        }

        method = "call"
        params = {
                  'action': "call_db",
                  'model': "cfg_ota_server",
                  'method': "_sel",
                  '_kwargs': _fields
        }

        log.info("Start Update: {}".format(url))


        resp = await self.http.client.request(url, method, params)
        log.debug("Resp:{}".format(resp))

        # Data Json
        if resp:

            data = await resp.read()
            log.debug("Data:{}".format(data))



        # Data File
        method = "GET"
        params = {}
        url = "{}:{}/boards/esp32_test/ota_bin.bin".format(addr, port)

        resp = await self.http.client.request(url, method, params, rtype="any")

        if resp:
            while True:
                data = await resp.read_data()
                if data:
                    log.debug("Data Stream:{}".format(data))


                elif data is None:
                    pass
                else:
                    break



            # await resp.done()
            #log.debug("Data:{}".format(data))


    def test(self):
        launch(self.run, "")



    # def __call__(self, *args):
    #     json = dict(method=self.name,
    #                 id=None,
    #                 params=list(args))
    #     req = Request.blank(self.parent._url)
    #     req.method = 'POST'
    #     req.content_type = 'application/json'
    #     req.body = dumps(json)
    #     resp = req.get_response(self.parent.proxy)
    #     if resp.status_code != 200 and not (
    #             resp.status_code == 500
    #             and resp.content_type == 'application/json'):
    #         raise ProxyError(
    #             "Error from JSON-RPC client %s: %s"
    #             % (self._url, resp.status),
    #             resp)
    #     json = loads(resp.body)
    #     if json.get('error') is not None:
    #         e = Fault(
    #             json['error'].get('message'),
    #             json['error'].get('code'),
    #             json['error'].get('error'),
    #             resp)
    #         raise e
    #     return json['result']
