from mod.net._runner import NetAction


def init(core, depend=None):
    core.env(env_name="net", env_action=NetAction, env_depend=depend)


