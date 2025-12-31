<template>
  <div class="ai-models-panel">
    <div class="panel-header">
      <h3>🤖 AI 助手</h3>
    </div>
    <div class="models-grid">
      <a
        v-for="model in models"
        :key="model.id"
        :href="model.url"
        target="_blank"
        rel="noopener noreferrer"
        class="model-card"
        :title="model.name"
      >
        <img 
          :src="model.icon" 
          :alt="model.name" 
          class="model-icon"
          @error="handleImageError($event, model)"
        />
        <div class="model-name">{{ model.name }}</div>
      </a>
    </div>
  </div>
</template>

<script setup>
const models = [
  {
    id: 'gemini',
    name: 'Gemini',
    url: 'https://gemini.google.com/',
    icon: '/images/gemini-icon.png',
    fallbackIcon: '💎',
    altIcons: ['/images/gemini.png', '/images/Gemini.png']
  },
  {
    id: 'chatgpt',
    name: 'ChatGPT',
    url: 'https://chat.openai.com/',
    icon: '/images/chatgpt-icon.png',
    fallbackIcon: '💬',
    altIcons: ['/images/chatgpt.png', '/images/ChatGPT.png']
  },
  {
    id: 'doubao',
    name: '豆包',
    url: 'https://www.doubao.com/',
    icon: '/images/doubao-icon.png',
    fallbackIcon: '🫘',
    altIcons: ['/images/doubao.png', '/images/豆包.png', '/images/豆包-icon.png']
  },
  {
    id: 'qianwen',
    name: '千问',
    url: 'https://tongyi.aliyun.com/qianwen/',
    icon: '/images/qianwen-icon.png',
    fallbackIcon: '❓',
    altIcons: ['/images/qianwen.png', '/images/千问.png', '/images/千问-icon.png', '/images/qwen-icon.png']
  }
]

function handleImageError(event, model) {
  const img = event.target
  const currentSrc = img.src
  
  // 尝试使用备用图标路径
  if (model.altIcons && model.altIcons.length > 0) {
    // 找到当前使用的图标在备用列表中的索引
    const currentIndex = model.altIcons.findIndex(alt => 
      currentSrc.includes(alt.replace('/images/', ''))
    )
    
    // 如果当前不是备用图标，或者还有未尝试的备用图标
    if (currentIndex === -1 || currentIndex < model.altIcons.length - 1) {
      const nextIndex = currentIndex === -1 ? 0 : currentIndex + 1
      const nextIcon = model.altIcons[nextIndex]
      img.src = nextIcon
      return
    }
  }
  
  // 如果所有图标都加载失败，使用fallback图标
  if (model.fallbackIcon) {
    img.style.display = 'none'
    // 检查是否已经存在fallback元素
    const existingFallback = img.parentNode.querySelector('.model-icon-fallback')
    if (!existingFallback) {
      const fallback = document.createElement('div')
      fallback.className = 'model-icon-fallback'
      fallback.textContent = model.fallbackIcon
      img.parentNode.insertBefore(fallback, img)
    }
  }
}
</script>

<style scoped>
.ai-models-panel {
  width: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(20px);
  border-top: 2px solid rgba(0, 255, 255, 0.3);
  box-shadow: 0 -4px 20px rgba(0, 255, 255, 0.1);
  flex: 0 0 auto;
  max-height: 280px;
  min-height: 240px;
}

.panel-header {
  padding: 12px 20px;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  background: rgba(0, 255, 255, 0.05);
}

.panel-header h3 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.1em;
  font-weight: 700;
  text-align: center;
}

.models-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding: 15px;
  overflow-y: auto;
}

.model-card {
  background: rgba(10, 14, 39, 0.6);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  padding: 15px 10px;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.model-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.model-card:hover::before {
  left: 100%;
}

.model-card:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
  background: rgba(0, 255, 255, 0.05);
}

.model-icon {
  width: 48px;
  height: 48px;
  object-fit: contain;
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.4));
  transition: transform 0.3s;
  border-radius: 8px;
}

.model-card:hover .model-icon {
  transform: scale(1.15);
  filter: drop-shadow(0 0 12px rgba(0, 255, 255, 0.5));
}

.model-name {
  font-size: 0.85em;
  font-weight: 600;
  color: #00ffff;
  text-align: center;
  transition: color 0.3s;
  white-space: nowrap;
}

.model-card:hover .model-name {
  color: #ffffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.model-icon-fallback {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.4));
  transition: transform 0.3s;
}

/* 滚动条样式 */
.models-grid::-webkit-scrollbar {
  width: 6px;
}

.models-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.models-grid::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #00ffff, #0080ff);
  border-radius: 3px;
}

.models-grid::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #00ffff, #00ccff);
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .models-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    padding: 12px;
  }
  
  .model-card {
    padding: 12px 8px;
  }
  
  .model-icon {
    width: 36px;
    height: 36px;
  }
  
  .model-name {
    font-size: 0.8em;
  }
}
</style>

