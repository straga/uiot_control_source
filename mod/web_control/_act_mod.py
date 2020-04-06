from mod.web_control._runner import ControlAction


def init(core, depend=None):
    core.env(env_name="web_control", env_action=ControlAction, env_depend=depend)


