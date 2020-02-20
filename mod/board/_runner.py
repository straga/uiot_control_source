import logging
log = logging.getLogger("BOARD")
log.setLevel(logging.DEBUG)

try:
    import ubinascii
except Exception:
    import binascii as ubinascii


import machine
from core.loader.loader import uLoad
from core.asyn.asyn import launch

class BoardAction(uLoad):

    async def _activate(self):

        _mod = await self.uconf.call("select_one", "board_cfg", "default", True)
        if _mod:
            # BOARD ID
            board_id = ubinascii.hexlify(machine.unique_id()).decode()
            log.info("BOARD ID: {}".format(board_id))

            _mod.uid = board_id
            await _mod.update()

            self.board = _mod
            self.core.board = self.board
            # self.mbus.pub_h("board/activate", board_id)

            self.mbus.pub_h("module", "board")
