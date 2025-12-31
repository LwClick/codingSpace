// 新闻数据存储工具
// 用于管理爬虫工具抓取的新闻数据

const STORAGE_KEY = 'codingSpace_news'
const MAX_NEWS_COUNT = 500 // 最多保存500条新闻

/**
 * 加载新闻数据
 * @returns {Array} 新闻列表
 */
export function loadNews() {
  try {
    const data = localStorage.getItem(STORAGE_KEY)
    if (data) {
      return JSON.parse(data)
    }
  } catch (error) {
    console.error('加载新闻数据失败:', error)
  }
  return []
}

/**
 * 保存新闻数据
 * @param {Array} news - 新闻列表
 */
export function saveNews(news) {
  try {
    // 限制数量，只保留最新的
    const limitedNews = news.slice(0, MAX_NEWS_COUNT)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(limitedNews))
    
    // 触发自定义事件，通知组件更新
    window.dispatchEvent(new CustomEvent('newsUpdated', { detail: limitedNews }))
  } catch (error) {
    console.error('保存新闻数据失败:', error)
  }
}

/**
 * 添加单条新闻
 * @param {Object} newsItem - 新闻项
 * @param {string} newsItem.title - 标题
 * @param {string} newsItem.source - 来源
 * @param {string} newsItem.url - 链接
 * @param {string} newsItem.category - 分类 (tech, industry, programming, ai)
 * @param {string} [newsItem.summary] - 摘要
 * @param {string|Date} [newsItem.time] - 时间
 */
export function addNewsItem(newsItem) {
  const news = loadNews()
  
  // 检查是否已存在（根据标题和来源判断）
  const exists = news.some(
    item => item.title === newsItem.title && item.source === newsItem.source
  )
  
  if (!exists) {
    const newItem = {
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      title: newsItem.title,
      source: newsItem.source,
      url: newsItem.url,
      category: newsItem.category || 'all',
      summary: newsItem.summary || '',
      time: newsItem.time ? new Date(newsItem.time).toISOString() : new Date().toISOString(),
      isNew: true
    }
    
    // 添加到开头
    news.unshift(newItem)
    saveNews(news)
  }
}

/**
 * 批量添加新闻
 * @param {Array} newsItems - 新闻项数组
 */
export function addNewsBatch(newsItems) {
  const news = loadNews()
  const existingTitles = new Set(
    news.map(item => `${item.title}||${item.source}`)
  )
  
  const newItems = newsItems
    .filter(item => {
      const key = `${item.title}||${item.source}`
      return !existingTitles.has(key)
    })
    .map(item => ({
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      title: item.title,
      source: item.source,
      url: item.url,
      category: item.category || 'all',
      summary: item.summary || '',
      time: item.time ? new Date(item.time).toISOString() : new Date().toISOString(),
      isNew: true
    }))
  
  if (newItems.length > 0) {
    news.unshift(...newItems)
    saveNews(news)
  }
  
  return newItems.length
}

/**
 * 清除所有新闻
 */
export function clearNews() {
  localStorage.removeItem(STORAGE_KEY)
  window.dispatchEvent(new CustomEvent('newsUpdated', { detail: [] }))
}

/**
 * 标记新闻为已读（移除 isNew 标记）
 * @param {string} newsId - 新闻ID
 */
export function markNewsAsRead(newsId) {
  const news = loadNews()
  const item = news.find(n => n.id === newsId)
  if (item) {
    item.isNew = false
    saveNews(news)
  }
}

/**
 * 获取新闻统计信息
 * @returns {Object} 统计信息
 */
export function getNewsStats() {
  const news = loadNews()
  const stats = {
    total: news.length,
    byCategory: {},
    newCount: news.filter(n => n.isNew).length
  }
  
  news.forEach(item => {
    const cat = item.category || 'all'
    stats.byCategory[cat] = (stats.byCategory[cat] || 0) + 1
  })
  
  return stats
}


