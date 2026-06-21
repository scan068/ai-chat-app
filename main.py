from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 【新增：导入跨域处理】
from pydantic import BaseModel
import sqlite3
import requests
import json

app = FastAPI()

# 【新增：在这里配置 CORS 跨域中间件】
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 这里务必填你前端 Vue 的运行地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法（包括 OPTIONS，解决你的 405 报错）
    allow_headers=["*"],
)

# 1. 初始化数据库，建一张表存聊天记录
conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_msg TEXT,
        ai_msg TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# 2. 定义请求体的格式：前端要发 message
class ChatRequest(BaseModel):
    message: str

# 3. 核心：与通义千问对话的函数
def ask_qwen(user_message):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": "Bearer sk-ws-H.REEILYD.6La2.MEUCIQC1pZW7EIeW3M9itYfNBT0J_WzJpZVhd1sm1rw8wtqFmAIgF4SpKwysKETVFqe0yMScxKOeNo-F2NfoZ56hw9q9KuI",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [{"role": "user", "content": user_message}]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    # 提取 AI 的回复
    return result["output"]["choices"][0]["message"]["content"]

# 4. 定义一个接口：前端发消息过来，返回AI回答并存入数据库
@app.post("/chat")
def chat_with_ai(req: ChatRequest):
    user_msg = req.message
    ai_msg = ask_qwen(user_msg)

    # 存入数据库
    cursor.execute("INSERT INTO history (user_msg, ai_msg) VALUES (?, ?)", (user_msg, ai_msg))
    conn.commit()

    return {"reply": ai_msg}

# 5. 再定义一个接口：拉取历史记录
@app.get("/history")
def get_history():
    cursor.execute("SELECT user_msg, ai_msg, time FROM history ORDER BY time DESC LIMIT 20")
    rows = cursor.fetchall()
    history_list = []
    for user, ai, t in rows:
        history_list.append({"user": user, "ai": ai, "time": t})
    return {"history": history_list}