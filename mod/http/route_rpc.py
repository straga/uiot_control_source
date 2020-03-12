
import json
import logging
log = logging.getLogger("HTTP-RPC-ROUTE")
log.setLevel(logging.INFO)
from core.asyn.asyn import is_coro

class Handler:

    def __init__(self, core):

        self.core = core
        self.route_handler = ("/rpc", "POST", self._handler)


    @staticmethod
    def _error_response(e, msg):
        return {
            "code": 0,
            "message": msg,
            "data": {
                "arguments": ["_"],
                "exception_type": "rpc_error",
                "message": "{}".format(e),
                "debug": ""
            }
        }

    @staticmethod
    def query_params(params):

        if "args" in params:
            params["args"] = tuple(params["args"])
        else:
            params["args"] = tuple()

        if "kwargs" in params:
            params["kwargs"] = params["kwargs"]
        else:
            params["kwargs"] = dict()

        return params



    @staticmethod
    def isgenerator(iterable):
        return hasattr(iterable, '__iter__') and not hasattr(iterable, '__len__')

    async def _handler(self, request):

        upd_size = 0
        if "content-length" in request._headers:
            upd_size = int(request._headers["content-length"])


        log.debug("= : POST DATA (content size): {}".format(upd_size))
        data_post = await request._read_data(upd_size)
        log.debug("> : POST DATA : {}".format(data_post))

        self._queryParams = data_post
        query_params = data_post

        response = {}
        _query = False
        _id = 0

        # JSON DECODE
        try:
            query_decode = query_params.decode()
            _query = json.loads(query_decode)
        except Exception as e:
            response["error"] = self._error_response(e, "RPC-JSON")
            log.error("RPC-JSON: {}".format(e))
            pass

        response["result"] = None
        if _query:

            params = _query["params"]
            _action = params["action"]
            _id = _query["id"]


            # CALL DB
            if _action == "call_db":
                try:

                    parse_query = self.query_params(params)

                    response["result"] = await self.core.uconf.call(
                        parse_query["method"],
                        parse_query["param"],
                        *parse_query["args"],
                        **parse_query["kwargs"]
                    )

                except Exception as e:
                    response["error"] = self._error_response(e, "RPC-ENV")
                    log.error("RPC-DB: {}".format(e))
                    pass



            # CALL ENV
            if _action == "call_env":

                params = _query["params"]
                _action = params["action"]

                try:
                    parse_query = self.query_params(params)

                    env_param = self.core.env(parse_query["param"])
                    path_method = parse_query["method"]

                    func_method = env_param
                    for _attr in path_method.split("."):
                        func_method = getattr(func_method, _attr)

                    if callable(func_method):
                        func_result = func_method(*parse_query["args"], **parse_query["kwargs"])
                        if is_coro(func_result):
                            response["result"] = await func_result
                        else:
                            response["result"] = func_result
                    else:
                        response["result"] = func_method

                except Exception as e:
                    response["error"] = self._error_response(e, "RPC-ENV")
                    log.error("RPC-ENV: {}".format(e))
                    pass

        response["jsonrpc"] = "2.0"
        response["id"] = _id

        if self.isgenerator(response["result"]):
            response["result"] = list(response["result"])


        # log.debug("RPC: {}".format(response["result"]))

        await request._response.return_json(response)

        return True





