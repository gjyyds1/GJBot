import os
import flask
import yaml
import requests
from functions import *

version = "v0.5.0-dev-2"
bot_server = flask.Flask(__name__)
api_url = "http://127.0.0.1:3000"

def load_config():
    global api_url
    with open("config.yml", "r", encoding="UTF-8") as read_config:
        config = yaml.safe_load(read_config)
    port = int(config["work_port"])
    run_host = str(config["run_host"])
    admin = list(config["admin"])
    return port, run_host, admin

def init():
    if not os.path.exists("config.yml"):
        print("未找到配置文件! 正在生成...\nCannot found config file! Creating...")
        with open("config.yml", "w", encoding="UTF-8") as f:
            f.write(f"# GJBot 配置文件 版本: {version}\n# GJBot Config File Version: {version}\n\n# 这是LLOneBot的json数据上报地址\n# This is LLOneBot's json data report host\nwork_port: 3003\n"
                   f"# 管理员QQ号\n# Admin's qqid(uid)\nadmin:\n - 0\n"
                   f"# Bot运行地址，不要添加端口！\n# Bot's running address. Do not add port!\nrun_host: localhost\n"
                   f"\n# 以下为默认配置\n# Default Config\n"
                   f"# work_port: 3003\n# admin:\n#  - 0\n# run_host: localhost\n")
        if not os.path.exists("commands.yml"):
            print("未找到命令配置文件! 正在生成...\nCannot found commands file! Creating...")
            with open("commands.yml", "w", encoding="UTF-8") as f:
                f.write("# GJBot 命令配置文件\n# GJBot Commands Config File\n\n# 请在下方添加命令\n# Please add commands below\n"
                        "command_list:\n test:\n  description: 测试命令\n  usage: #test\n  permission: admin\n  enabled: true\n  fn: null\n"
                        " help:\n  description: 帮助命令\n  usage: #help\n  permission: everyone\n  enabled: true\n  fn: help_command\n")
        print("创建成功! 请修改配置后重启程序!\nCreated Succeed! Please mod it and then restart!")
        return False
    else:
        print("找到配置文件! 加载中...\nFound config file! Loading...")
        return True

def main():
    if not init():
        print("Exited! Code: 1")
        exit(1)
    else:
        pass

def get_command_list():
    with open("commands.yml", "r", encoding="UTF-8") as command_list:
        commands = yaml.safe_load(command_list)
    return commands["command_list"]

def send_msg(msg: str | None, uid: str | int, gid: str | int | None,
             mid: str | int | None = None):  # 发送信息函数,msg: 正文,uid: QQ号,gid: 群号,mid: 消息编号
    data = {}
    if msg is None:
        return
    if mid is not None:  # 当消息编号不为None时,则发送的消息为回复
        data.update({"message": f"[CQ:reply,id={mid}]{msg}"})
    else:  # 反之为普通消息
        data.update({"message": msg})
    if gid is not None:  # 当群号不为None时,则发送给群聊
        url = f"http://127.0.0.1:3000/send_group_msg"
        data.update({"group_id": gid})
    else:  # 反之为私聊
        url = f"http://127.0.0.1:3000/send_private_msg"
        data.update({"user_id": uid})
    try:
        requests.post(url, json=data, timeout=5)  # 提交发送消息
    except requests.exceptions.RequestException as e:
        print(e)

def command_process(msg: str, uid: str | int, gid: str | int | None, mid: str | int | None):
    commands = get_command_list()
    if msg in commands:
        detail = commands[msg]
        if detail["enabled"] is True:
            if detail["permission"] == "everyone":
                if detail["fn"] is not None:
                    globals()[detail["fn"]](msg, uid, gid, mid)
                if detail.get("send") is not None:
                    for need_msg in detail["send"]:
                        send_msg(need_msg, uid, gid, mid)
            elif detail["permission"] == "admin":
                admin = load_config()[-1]
                if uid in admin:
                    if detail["fn"] is not None:
                        globals()[detail["fn"]](msg, uid, gid, mid)
                    if detail.get("send") is not None:
                        for need_msg in detail["send"]:
                            send_msg(need_msg, uid, gid, mid)
                else:
                    send_msg("权限不足!", uid, gid, mid)
        else:
            send_msg("命令未启用!", uid, gid, mid)

@bot_server.post("/")
def process():
    data = flask.request.get_json()  # 获取提交数据
    uid = data.get("user_id")
    gid = data.get("group_id")
    mid = data.get("message_id")
    msg = data.get("raw_message")
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;",
                                                                                            ",")  # 消息需要将URL编码替换到正确内容
        if msg.startswith("#"):
            # 去除msg的#
            msg = msg.replace("#", "")
            command_process(msg, uid, gid, mid)  # 处理命令
    return "", 204

if __name__ == "__main__":
    main()
    port, host, _ = load_config()
    bot_server.run(port=port, host=host)
