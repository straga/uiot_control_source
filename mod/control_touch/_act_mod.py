from mod.control_touch._runner import ControlAction


def init(core, depend=None):
    core.env(env_name="control_touch", env_action=ControlAction, env_depend=depend)


