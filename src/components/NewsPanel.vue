<template>
  <div class="news-panel">
    <div class="news-header">
      <h3>📰 资讯中心</h3>
    </div>
    
    <div class="news-categories">
      <button
        v-for="category in categories"
        :key="category.id"
        :class="['category-btn', { active: activeCategory === category.id }]"
        @click="activeCategory = category.id"
      >
        {{ category.name }}
      </button>
    </div>

    <div class="news-content">
      <div v-if="filteredNews.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <p>暂无{{ getCategoryName(activeCategory) }}内容</p>
        <p class="empty-hint">等待爬虫工具抓取数据...</p>
      </div>
      
      <div v-else class="news-list">
        <div
          v-for="item in filteredNews"
          :key="item.id"
          class="news-item"
          @click="handleNewsClick(item)"
        >
          <div class="news-item-header">
            <span class="news-title">{{ item.title }}</span>
            <span v-if="item.isNew" class="news-badge">新</span>
          </div>
          <div class="news-meta">
            <span class="news-source">{{ item.source }}</span>
            <span class="news-time">{{ formatTime(item.time) }}</span>
          </div>
          <div v-if="item.summary" class="news-summary">{{ item.summary }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { loadNews } from '../utils/newsStorage.js'

const activeCategory = ref('all')

const categories = [
  { id: 'all', name: '全部' },
  { id: 'tech', name: '技术新闻' },
  { id: 'industry', name: '行业资讯' },
  { id: 'programming', name: '编程相关' },
  { id: 'ai', name: 'AI/机器学习' }
]

// 从存储加载新闻数据
const news = ref(loadNews())

const filteredNews = computed(() => {
  if (activeCategory.value === 'all') {
    return news.value
  }
  return news.value.filter(item => item.category === activeCategory.value)
})

function getCategoryName(categoryId) {
  const category = categories.find(c => c.id === categoryId)
  return category ? category.name : '全部'
}

function formatTime(time) {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

function handleNewsClick(item) {
  if (item.url) {
    window.open(item.url, '_blank')
  }
}

// 监听新闻更新事件
function handleNewsUpdate(event) {
  if (event.detail) {
    news.value = event.detail
  } else {
    news.value = loadNews()
  }
}

onMounted(() => {
  // 加载初始数据
  news.value = loadNews()
  
  // 监听存储变化和自定义事件
  window.addEventListener('storage', () => {
    news.value = loadNews()
  })
  
  window.addEventListener('newsUpdated', handleNewsUpdate)
})

onUnmounted(() => {
  window.removeEventListener('newsUpdated', handleNewsUpdate)
})

// 暴露方法供外部调用，用于更新新闻数据
function updateNews(newNewsData) {
  news.value = newNewsData
}

// 暴露方法供外部调用，用于添加新闻
function addNews(newItem) {
  news.value.unshift(newItem)
  // 限制最多显示100条
  if (news.value.length > 100) {
    news.value = news.value.slice(0, 100)
  }
}

defineExpose({
  updateNews,
  addNews,
  news
})
</script>

<style scoped>
.news-panel {
  width: 350px;
  min-width: 300px;
  max-width: 400px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(20px);
  border-right: 2px solid rgba(0, 255, 255, 0.3);
  box-shadow: 4px 0 20px rgba(0, 255, 255, 0.1);
  flex-shrink: 0;
}

.news-header {
  padding: 20px;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  background: rgba(0, 255, 255, 0.05);
}

.news-header h3 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.3em;
  font-weight: 700;
  text-align: center;
}

.news-categories {
  padding: 15px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  background: rgba(10, 14, 39, 0.4);
}

.category-btn {
  padding: 6px 14px;
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 15px;
  color: #e0e0e0;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 12px;
  white-space: nowrap;
}

.category-btn:hover {
  border-color: rgba(0, 255, 255, 0.5);
  background: rgba(0, 255, 255, 0.1);
}

.category-btn.active {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  border-color: rgba(0, 255, 255, 0.5);
  color: #00ffff;
}

.news-content {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(224, 224, 224, 0.5);
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 3em;
  margin-bottom: 15px;
  opacity: 0.5;
}

.empty-state p {
  margin: 8px 0;
  font-size: 14px;
}

.empty-hint {
  font-size: 12px;
  color: rgba(224, 224, 224, 0.4);
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.news-item {
  background: rgba(10, 14, 39, 0.4);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 10px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.news-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.news-item:hover::before {
  left: 100%;
}

.news-item:hover {
  border-color: rgba(0, 255, 255, 0.5);
  background: rgba(0, 255, 255, 0.05);
  transform: translateX(3px);
}

.news-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  gap: 10px;
}

.news-title {
  font-size: 14px;
  font-weight: 600;
  color: #e0e0e0;
  line-height: 1.4;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-badge {
  padding: 2px 8px;
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #0a0e27;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 700;
  flex-shrink: 0;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 11px;
  color: rgba(224, 224, 224, 0.6);
}

.news-source {
  color: rgba(0, 255, 255, 0.7);
}

.news-time {
  color: rgba(224, 224, 224, 0.5);
}

.news-summary {
  font-size: 12px;
  color: rgba(224, 224, 224, 0.7);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-top: 5px;
}

/* 滚动条样式 */
.news-content::-webkit-scrollbar {
  width: 6px;
}

.news-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.news-content::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #00ffff, #0080ff);
  border-radius: 3px;
}

.news-content::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #00ffff, #00ccff);
}
</style>


