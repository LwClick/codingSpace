<template>
  <div class="home-container">
    <div class="search-section">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜索工具..." 
          v-model="searchQuery"
          class="search-input"
        />
        <button class="search-btn">搜索</button>
      </div>
    </div>

    <div class="categories-section">
      <div class="category-tabs">
        <button 
          v-for="category in categories" 
          :key="category.id"
          :class="['category-tab', { active: activeCategory === category.id }]"
          @click="activeCategory = category.id"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <div class="tools-section">
      <div class="section-header">
        <h2>{{ getCategoryName(activeCategory) }}</h2>
      </div>
      <div class="tools-grid">
        <div 
          v-for="tool in filteredTools" 
          :key="tool.id"
          class="tool-card"
          @click="navigateToTool(tool)"
        >
          <div class="tool-icon">{{ tool.icon }}</div>
          <div class="tool-name">{{ tool.name }}</div>
          <div class="tool-desc">{{ tool.description }}</div>
          <div v-if="tool.hot" class="tool-badge hot">hot</div>
          <div v-if="tool.new" class="tool-badge new">new</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')
const activeCategory = ref('all')

const categories = [
  { id: 'all', name: '全部' },
  { id: 'algorithm', name: '算法工具' },
  { id: 'code', name: '代码工具' },
  { id: 'data', name: '数据处理' },
  { id: 'other', name: '其他工具' }
]

const tools = [
  {
    id: 'calendar',
    name: '算法刷题日历',
    description: '记录每天的算法刷题内容，管理学习进度',
    icon: '📅',
    category: 'algorithm',
    route: '/calendar',
    hot: true
  },
  {
    id: 'code-runner',
    name: '代码运行器',
    description: '在线运行Python代码，实时查看结果',
    icon: '💻',
    category: 'code',
    route: '/code-runner'
  },
  {
    id: 'algorithm-visualizer',
    name: '算法可视化',
    description: '可视化展示各种算法的执行过程',
    icon: '🎨',
    category: 'algorithm',
    route: '/algorithm-visualizer'
  },
  {
    id: 'data-converter',
    name: '数据转换',
    description: 'JSON、XML、CSV等格式转换',
    icon: '🔄',
    category: 'data',
    route: '/data-converter'
  }
]

const filteredTools = computed(() => {
  let result = tools

  // 按分类筛选
  if (activeCategory.value !== 'all') {
    result = result.filter(tool => tool.category === activeCategory.value)
  }

  // 按搜索关键词筛选
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(tool => 
      tool.name.toLowerCase().includes(query) ||
      tool.description.toLowerCase().includes(query)
    )
  }

  return result
})

function getCategoryName(categoryId) {
  const category = categories.find(c => c.id === categoryId)
  return category ? category.name : '全部工具'
}

function navigateToTool(tool) {
  router.push(tool.route)
}
</script>

<style scoped>
.home-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px 20px;
}

.search-section {
  margin-bottom: 40px;
}

.search-box {
  display: flex;
  gap: 10px;
  max-width: 600px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 25px;
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(10px);
  color: #e0e0e0;
  font-size: 16px;
  outline: none;
  transition: all 0.3s;
}

.search-input:focus {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.search-input::placeholder {
  color: rgba(224, 224, 224, 0.5);
}

.search-btn {
  padding: 15px 30px;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  color: #00ffff;
  border: 2px solid rgba(0, 255, 255, 0.5);
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s;
}

.search-btn:hover {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #0a0e27;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.categories-section {
  margin-bottom: 30px;
}

.category-tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.category-tab {
  padding: 10px 20px;
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 20px;
  color: #e0e0e0;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.category-tab:hover {
  border-color: rgba(0, 255, 255, 0.5);
  background: rgba(0, 255, 255, 0.1);
}

.category-tab.active {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  border-color: rgba(0, 255, 255, 0.5);
  color: #00ffff;
}

.tools-section {
  margin-top: 30px;
}

.section-header {
  margin-bottom: 25px;
}

.section-header h2 {
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.8em;
  font-weight: 700;
  text-align: center;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.tool-card {
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.tool-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.tool-card:hover::before {
  left: 100%;
}

.tool-card:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
}

.tool-icon {
  font-size: 3em;
  margin-bottom: 15px;
  text-align: center;
}

.tool-name {
  font-size: 1.2em;
  font-weight: 700;
  color: #00ffff;
  margin-bottom: 10px;
  text-align: center;
}

.tool-desc {
  color: rgba(224, 224, 224, 0.8);
  font-size: 0.9em;
  line-height: 1.5;
  text-align: center;
}

.tool-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75em;
  font-weight: 700;
  text-transform: uppercase;
}

.tool-badge.hot {
  background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
  color: white;
}

.tool-badge.new {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #0a0e27;
}
</style>

