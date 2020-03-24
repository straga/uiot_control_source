from mod.ctrl_kitchen_light._runner import ControlAction


def init(core, depend=None):
    core.env(env_name="kitchen_light", env_action=ControlAction, env_depend=depend)


