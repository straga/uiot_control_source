from mod.binary_sensor._runner import BinaryAction


def init(core, depend=None):
    core.env(env_name="binary_sensor", env_action=BinaryAction, env_depend=depend)


