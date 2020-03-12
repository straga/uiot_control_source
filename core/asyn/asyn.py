
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


async def _g():
    pass
type_coro = type(_g())


def is_coro(func):
    if isinstance(func, type_coro):
        return True
    return False


def launch(func, _args=None, _kwargs=None):
    if _kwargs is None:
        _kwargs = {}
    if _args is None:
        _kwargs = ()

    try:
        res = func(*_args, **_kwargs)
        if isinstance(res, type_coro):
            loop = asyncio.get_event_loop()
            loop.create_task(res)
    except Exception as e:
        print(e)
        pass



class Lock():
    def __init__(self, delay_ms=0):
        self._locked = False
        self.delay_ms = delay_ms

    def locked(self):
        return self._locked

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, *args):
        self.release()
        await asyncio.sleep(0)

    async def acquire(self):
        while True:
            if self._locked:
                await asyncio.sleep(self.delay_ms)
            else:
                self._locked = True
                break


    def release(self):
        if not self._locked:
            raise RuntimeError('Attempt to release a lock which has not been set')
        self._locked = False

