from mod.board._runner import BoardAction


def init(core, depend=None):
    core.env(env_name="board", env_action=BoardAction, env_depend=depend)




