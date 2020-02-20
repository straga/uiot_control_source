
import secrets


def unique_id():
    return secrets.token_hex(4).encode()

