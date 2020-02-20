from mod.ftp._runner import FtpAction


def init(core, depend=None):
    core.env(env_name="ftp", env_action=FtpAction, env_depend=depend)


