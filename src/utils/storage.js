const STORAGE_KEY = 'algorithm_problems'

export function loadProblems() {
  try {
    const data = localStorage.getItem(STORAGE_KEY)
    return data ? JSON.parse(data) : {}
  } catch (error) {
    console.error('加载数据失败:', error)
    return {}
  }
}

export function saveProblems(problems) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(problems))
    // 触发自定义事件，通知其他组件数据已更新
    window.dispatchEvent(new Event('problemsUpdated'))
  } catch (error) {
    console.error('保存数据失败:', error)
  }
}

export function getDateKey(date) {
  if (typeof date === 'string') {
    return date
  }
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}



