<template>
  <div class="chat-container">
    <h2>🤖 我的AI全栈助手</h2>
    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, index) in messages" :key="index"
           :class="['message', msg.role === 'user' ? 'user' : 'ai']">
        <strong>{{ msg.role === 'user' ? '我' : 'AI' }}：</strong>
        <span>{{ msg.content }}</span>
      </div>
    </div>
    <div class="input-area">
      <el-input v-model="inputMsg" placeholder="输入消息..." @keyup.enter="sendMsg"></el-input>
      <el-button type="primary" @click="sendMsg">发送</el-button>
    </div>
    <el-button type="text" @click="loadHistory">查看最近对话记录</el-button>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const inputMsg = ref('')
const messages = ref([])
const chatBox = ref(null)

// 后端地址（如果后端在本地8000端口）
const API_BASE = 'http://127.0.0.1:8000'

const sendMsg = async () => {
  const msg = inputMsg.value.trim()
  if (!msg) return

  // 显示用户消息
  messages.value.push({ role: 'user', content: msg })
  inputMsg.value = ''
  scrollToBottom()

  try {
    const res = await axios.post(`${API_BASE}/chat`, { message: msg })
    // 显示AI回复
    messages.value.push({ role: 'ai', content: res.data.reply })
  } catch (e) {
    messages.value.push({ role: 'ai', content: '出错啦，请确认后端已启动。' })
  }
  scrollToBottom()
}

const loadHistory = async () => {
  try {
    const res = await axios.get(`${API_BASE}/history`)
    const history = res.data.history.reverse() // 让旧消息在上面
    messages.value = []
    history.forEach(item => {
      messages.value.push({ role: 'user', content: item.user })
      messages.value.push({ role: 'ai', content: item.ai })
    })
  } catch (e) {
    alert('加载历史失败')
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBox.value) {
      chatBox.value.scrollTop = chatBox.value.scrollHeight
    }
  })
}
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 20px auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
}
.chat-box {
  height: 400px;
  overflow-y: auto;
  background: #f9f9f9;
  padding: 10px;
  margin-bottom: 10px;
}
.message {
  margin-bottom: 12px;
}
.user {
  color: #1a73e8;
}
.ai {
  color: #0d904f;
}
.input-area {
  display: flex;
  gap: 8px;
}
</style>