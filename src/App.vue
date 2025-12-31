<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <div class="logo-container" @click="$router.push('/')">
          <div class="taiji-logo">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <circle cx="50" cy="50" r="50" fill="none" stroke="rgba(0, 255, 255, 0.3)" stroke-width="1"/>
              <circle cx="50" cy="50" r="48" fill="#0a0e27"/>
              <path d="M 50 2 A 48 48 0 0 1 50 98 A 24 24 0 0 0 50 50 A 24 24 0 0 1 50 2 Z" fill="rgba(0, 255, 255, 0.8)"/>
              <circle cx="50" cy="26" r="11" fill="#0a0e27"/>
              <circle cx="50" cy="74" r="11" fill="rgba(0, 255, 255, 0.8)"/>
              <circle cx="50" cy="50" r="48" fill="none" stroke="rgba(0, 255, 255, 0.2)" stroke-width="0.5"/>
            </svg>
          </div>
          <h1>codingSpace</h1>
        </div>
        <div class="header-center">
          <div class="search-box-header">
            <input 
              type="text" 
              placeholder="搜索工具..." 
              v-model="searchQuery"
              class="search-input-header"
            />
            <button class="search-btn-header">搜索</button>
          </div>
        </div>
        <div class="header-right">
          <div class="time-display">{{ currentTime }}</div>
          <div class="avatar-container">
            <div class="avatar">
              <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="50" fill="rgba(0, 255, 255, 0.2)"/>
                <circle cx="50" cy="35" r="15" fill="rgba(0, 255, 255, 0.8)"/>
                <path d="M 20 85 Q 20 65 50 65 Q 80 65 80 85" fill="rgba(0, 255, 255, 0.8)"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </header>
    <main class="app-main">
      <div class="main-layout">
        <NewsPanel ref="newsPanelRef" />
        <div class="content-area">
          <router-view />
        </div>
        <div class="right-sidebar">
          <CalendarWidget :problems="problems" />
          <AIModelsPanel />
        </div>
      </div>
    </main>
    <footer class="app-footer">
      <span>© 2024 codingSpace. All rights reserved.</span>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, provide } from 'vue'
import CalendarWidget from './components/CalendarWidget.vue'
import NewsPanel from './components/NewsPanel.vue'
import AIModelsPanel from './components/AIModelsPanel.vue'
import { loadProblems } from './utils/storage.js'

const problems = ref({})
const currentTime = ref('')
const searchQuery = ref('')
const newsPanelRef = ref(null)

// 提供搜索查询给子组件使用
provide('searchQuery', searchQuery)

function updateTime() {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  currentTime.value = `${hours}:${minutes}:${seconds}`
}

let timeInterval = null

onMounted(() => {
  problems.value = loadProblems()
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  
  // 监听存储变化，更新数据
  window.addEventListener('storage', () => {
    problems.value = loadProblems()
  })
  
  // 监听自定义事件，当数据保存时更新
  window.addEventListener('problemsUpdated', () => {
    problems.value = loadProblems()
  })
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: 
    radial-gradient(circle at 20% 50%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 40% 20%, rgba(0, 100, 255, 0.1) 0%, transparent 50%),
    linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
  background-size: 100% 100%;
  position: relative;
  overflow: hidden;
}

#app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20% 30%, #00ffff, transparent),
    radial-gradient(2px 2px at 60% 70%, #0080ff, transparent),
    radial-gradient(1px 1px at 50% 50%, #ffffff, transparent),
    radial-gradient(1px 1px at 80% 10%, #00ffff, transparent),
    radial-gradient(2px 2px at 90% 40%, #0080ff, transparent),
    radial-gradient(1px 1px at 33% 60%, #ffffff, transparent),
    radial-gradient(2px 2px at 10% 80%, #00ffff, transparent);
  background-repeat: repeat;
  background-size: 200% 200%;
  animation: float 20s ease-in-out infinite;
  opacity: 0.4;
  pointer-events: none;
  z-index: 0;
}

.app-header {
  background: rgba(10, 14, 39, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 2px solid rgba(0, 255, 255, 0.3);
  box-shadow: 0 4px 30px rgba(0, 255, 255, 0.2);
  position: relative;
  z-index: 1;
  flex-shrink: 0;
  padding: 10px 20px;
}

.app-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(0, 255, 255, 0.8), 
    rgba(0, 128, 255, 0.8), 
    rgba(0, 255, 255, 0.8), 
    transparent
  );
  animation: shimmer 3s infinite;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.header-center {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.logo-container:hover {
  opacity: 0.8;
}

.taiji-logo {
  width: 35px;
  height: 35px;
  animation: rotate 10s linear infinite;
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.5));
  flex-shrink: 0;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.taiji-logo svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.6));
}

.app-header h1 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.6em;
  font-weight: 700;
  letter-spacing: 2px;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
  animation: pulse 3s ease-in-out infinite;
  white-space: nowrap;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-box-header {
  display: flex;
  gap: 8px;
  align-items: center;
}

.search-input-header {
  width: 400px;
  padding: 10px 20px;
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 20px;
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(10px);
  color: #e0e0e0;
  font-size: 15px;
  outline: none;
  transition: all 0.3s;
}

.search-input-header:focus {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
  width: 450px;
}

.search-input-header::placeholder {
  color: rgba(224, 224, 224, 0.5);
}

.search-btn-header {
  padding: 10px 16px;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  color: #00ffff;
  border: 2px solid rgba(0, 255, 255, 0.5);
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s;
  white-space: nowrap;
}

.search-btn-header:hover {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #0a0e27;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
}

.app-footer {
  padding: 15px 20px;
  border-top: 1px solid rgba(0, 255, 255, 0.1);
  background: rgba(10, 14, 39, 0.5);
  text-align: center;
  font-size: 12px;
  color: rgba(224, 224, 224, 0.6);
  letter-spacing: 1px;
  flex-shrink: 0;
  z-index: 1;
  position: relative;
}

@media (max-width: 768px) {
  .header-content {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .header-center {
    order: 3;
    width: 100%;
    margin-top: 10px;
  }
  
  .search-box-header {
    width: 100%;
    max-width: 100%;
  }
  
  .search-input-header {
    flex: 1;
    width: auto;
  }
  
  .search-input-header:focus {
    width: auto;
  }
  
  .header-right {
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .app-header h1 {
    font-size: 1.3em;
  }
  
  .time-display {
    font-size: 0.9em;
  }
}

.time-display {
  font-size: 1.1em;
  font-weight: 600;
  color: #00ffff;
  font-family: 'Courier New', monospace;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  letter-spacing: 1px;
}

.avatar-container {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid rgba(0, 255, 255, 0.5);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  background: rgba(0, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar:hover {
  border-color: rgba(0, 255, 255, 0.8);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
  transform: scale(1.05);
}

.avatar svg {
  width: 100%;
  height: 100%;
}

.app-main {
  flex: 1;
  padding: 0;
  position: relative;
  z-index: 1;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.main-layout {
  display: flex;
  height: 100%;
  width: 100%;
}

.content-area {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 15px 20px;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.content-area > * {
  max-width: 1400px;
  width: 100%;
}

.right-sidebar {
  width: 350px;
  min-width: 300px;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  height: 100%;
  flex-shrink: 0;
  border-left: 2px solid rgba(0, 255, 255, 0.3);
  overflow: hidden;
}

/* 响应式布局 */
@media (max-width: 1400px) {
  .right-sidebar {
    width: 320px;
    min-width: 280px;
  }
}

@media (max-width: 1024px) {
  .main-layout {
    flex-direction: column;
  }
  
  .news-panel {
    max-height: 300px;
    border-right: none;
    border-bottom: 2px solid rgba(0, 255, 255, 0.3);
  }
  
  .right-sidebar {
    width: 100%;
    max-width: 100%;
    max-height: 500px;
    border-left: none;
    border-top: 2px solid rgba(0, 255, 255, 0.3);
    flex-direction: row;
  }
  
  .calendar-widget {
    flex: 1;
    border-bottom: none;
    border-right: 2px solid rgba(0, 255, 255, 0.3);
  }
  
  .ai-models-panel {
    flex: 1;
    border-top: none;
    max-height: 100%;
  }
}
</style>
