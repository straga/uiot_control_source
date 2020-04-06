from mod.control_mqtt._runner import ControlAction


def init(core, depend=None):
    core.env(env_name="control_mqtt", env_action=ControlAction, env_depend=depend)


