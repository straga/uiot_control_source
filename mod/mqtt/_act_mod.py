from mod.mqtt._runner import MQTTAction


def init(core, depend=None):
    core.env(env_name="mqtt", env_action=MQTTAction, env_depend=depend)


