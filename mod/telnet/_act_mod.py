from mod.telnet._runner import TelnetAction


def init(core, depend=None):
    core.env(env_name="telnet", env_action=TelnetAction, env_depend=depend)


