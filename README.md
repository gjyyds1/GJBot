# GJBot

GJBot 是一个基于 Flask 的轻量级 QQ 机器人，支持命令配置和消息处理，方便用户快速部署和自定义。

## 注意事项

1. 该程序需搭配 [`LLBot`](https://www.llonebot.com/) 使用
2. functions.py代码请自行辨别是否会损害设备，第三方代码与作者无关
3. dev分支为开发版，功能未经测试，请不要在生产环境使用
4. bug反馈请提交issues(有能力修复的可以提交PR)

## 特性

- 使用 Flask 提供 HTTP 接口。
- 支持自定义命令配置，包含权限管理和命令启用状态。
- 提供基础的消息发送功能。
- 自动生成必要的配置文件，便于快速初始化。

## 文件结构

```plaintext
.
├── main.py           # 主程序文件，包含核心逻辑
├── functions.py      # 自定义功能函数
├── config.yml        # 机器人配置文件
├── commands.yml      # 机器人命令配置文件
```

## 快速开始

### 环境要求

- Python3
- Flask
- PyYAML
- requests

### 安装依赖

运行以下命令安装必要的依赖：

```bash
pip3 install flask pyyaml requests
```

### 初始化项目

1. 下载或克隆项目代码：

```bash
git clone https://github.com/gjyyds1/GJBot.git
cd GJBot
```

2. 运行程序：

```bash
python main.py
```

如果配置文件（`config.yml` 和 `commands.yml`）不存在，程序会自动生成默认配置文件。请根据需要修改配置后重启程序。

### 配置文件说明

#### `config.yml`

- `work_port`: 程序监听的端口号。
- `admin`: 管理员 QQ 号列表。
- `run_host`: 程序运行的主机地址。

#### 示例

```yaml
work_port: 3003
admin:
 - 2712878343
run_host: 127.0.0.1
```

#### `commands.yml`

`command_list`: 命令列表配置。
 `description`: 命令描述。
 `usage`: 命令用法。
 `permission`: 权限要求（`everyone` 或 `admin`）。
 `enabled`: 是否启用命令。
 `fn`: 对应的功能函数。
 `send`: 
    - `发送的消息内容。

#### 示例

```yaml
command_list:
 help:
  description: 获取命令帮助
  usage: "#help"
  permission: everyone
  enabled: true
  fn: help_command
  send:
   - null
 test:
  description: 测试
  usage: "#test"
  permission: admin
  enabled: true
  fn: null
  send:
   - "test"
```

## 自定义功能

### 添加新命令

1. 在 `functions.py` 文件中定义新功能函数。例如：

```python
from main import send_msg

def new_command(msg, uid, gid, mid):
    send_msg("这是一个新命令的响应！", uid, gid, None)
```

2. 在 `commands.yml` 文件中添加新命令配置。例如：

```yaml
 new:
  description: 新命令
  usage: "#new"
  permission: everyone
  enabled: true
  fn: new_command
  send:
   - null
```

3. 重启程序使配置生效。

### 消息处理

所有接收到的消息会通过 `/` 接口进行处理，支持解析 OneBot 标准上报的数据。

## 注意事项

- 确保配置文件的格式正确，否则程序可能无法运行。
- 管理员权限命令仅限于 `config.yml` 中指定的 QQ 号。

## 开发者

- 作者: `gjyyds1`
- 联系方式: `QQ 2712878343` & `Email: 2712878343@qq.com`
- 赞助我: [`爱发电`](https://afdian.com/a/gjyyds1)
