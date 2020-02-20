
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

from threading import Thread


class RunInThread(Thread):
    """
    """
    def __init__(self, action, *args, **kwargs):
        """Инициализация потока"""
        Thread.__init__(self)
        self.status = True
        self.result = None
        self.action = action
        self._args = args
        self._kwargs = kwargs


    def run(self):
        """Запуск потока"""
        # print("Thread Act Run")

        try:
            self.result = self.action(*self._args, **self._kwargs)
        except Exception as e:
            print("Err: thread Act: {}".format(e))
            return False

        self.status = False
        # print("Thread Act Done")


async def run_in_executer(action, *args, **kwargs):

    thread = RunInThread(action, *args, **kwargs)
    thread.start()

    while True:
        if not thread.status:
            break
        await asyncio.sleep(0.05)

    return thread.result

