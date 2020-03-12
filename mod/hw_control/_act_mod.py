from mod.hw_control._runner import HwAction


def init(core, depend=None):
    core.env(env_name="hw_control", env_action=HwAction, env_depend=depend)


