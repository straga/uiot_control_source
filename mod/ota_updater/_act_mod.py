from mod.ota_updater._runner import OtaAction


def init(core, depend=None):
    core.env(env_name="ota_upd", env_action=OtaAction, env_depend=depend)


