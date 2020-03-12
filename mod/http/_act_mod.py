from mod.http._runner import HTTPAction


def init(core, depend=None):
    core.env(env_name="http", env_action=HTTPAction, env_depend=depend)


