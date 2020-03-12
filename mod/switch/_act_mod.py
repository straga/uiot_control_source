from mod.switch._runner import SwitchAction


def init(core, depend=None):
    core.env(env_name="switch", env_action=SwitchAction, env_depend=depend)


