from mod.pin._runner import PinAction


def init(core, depend=None):
    core.env(env_name="pin", env_action=PinAction, env_depend=depend)


