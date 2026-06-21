# AI 对话全栈应用

## 项目简介
基于通义千问大模型的对话式分析工具，支持多轮对话和历史记录查看。

## 技术栈
- 后端：Python + FastAPI + SQLite
- 前端：Vue 3 + Element Plus
- AI：通义千问 API

## 如何运行

### 1. 克隆项目
git clone https://github.com/scan068/ai-chat-app.git
cd ai-chat-app

### 2. 安装后端依赖
pip install fastapi uvicorn requests

### 3. 配置 API Key
打开 main.py，将 `你的API-KEY` 替换为你的通义千问 API Key

### 4. 启动后端
uvicorn main:app --reload

### 5. 启动前端
cd frontend
npm install
npm run dev

### 6. 打开浏览器访问
http://localhost:5173
