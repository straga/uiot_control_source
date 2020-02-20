import logging

def mod_debug():

    log = logging.getLogger("PIN")
    log.setLevel(logging.INFO)

    log = logging.getLogger("FDB")
    log.setLevel(logging.INFO)

    log = logging.getLogger("MOD")
    log.setLevel(logging.INFO)

    log = logging.getLogger("MBUS")
    log.setLevel(logging.DEBUG)

    log = logging.getLogger("PUSH")
    log.setLevel(logging.INFO)

    log = logging.getLogger("Control")
    log.setLevel(logging.INFO)

    log = logging.getLogger("RELAY")
    log.setLevel(logging.INFO)

    log = logging.getLogger("WIFI")
    log.setLevel(logging.INFO)

    log = logging.getLogger('PIN')
    log.setLevel(logging.DEBUG)

    log = logging.getLogger('PUSH')
    log.setLevel(logging.DEBUG)

import logging
log = logging.getLogger("MBUS")
log.setLevel(logging.DEBUG)