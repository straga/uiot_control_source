from mod.message._runner import MessageAction


def init(core, depend=None):
    core.env(env_name="msg", env_action=MessageAction, env_depend=depend)


