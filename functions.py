from main import get_command_list, send_msg

def help(data: dict, msg: str, uid: int, gid: int, mid: int):
    commands = get_command_list()
    help_text = "命令列表: \n" + "\n".join(f"#{k}: {v['description']}" for k, v in commands.items())
    send_msg(help_text, uid, gid, None)
