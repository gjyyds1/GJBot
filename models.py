import sqlite3
from datetime import datetime

# 数据库文件路径
DB_PATH = "messages.db"

# 创建数据库并创建表（如果尚未存在）
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        msg TEXT,
        gid TEXT,
        uid TEXT,
        mid TEXT,
        timestamp TEXT
    )
    ''')
    conn.commit()
    conn.close()

# 保存消息到数据库
def save_message(msg, gid, uid, mid):
    # 获取当前时间
    timestamp = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')

    # 将消息数据插入数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO messages (msg, gid, uid, mid, timestamp)
    VALUES (?, ?, ?, ?, ?)
    ''', (msg, gid, uid, mid, timestamp))
    conn.commit()
    conn.close()

# 调用创建表函数
create_table()
