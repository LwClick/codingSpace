// 认证工具 - 管理用户登录状态

const AUTH_KEY = 'codingSpace_auth'
const USER_KEY = 'codingSpace_user'

/**
 * 检查用户是否已登录
 * @returns {boolean}
 */
export function isAuthenticated() {
  try {
    const auth = localStorage.getItem(AUTH_KEY)
    if (!auth) return false
    
    const authData = JSON.parse(auth)
    // 检查token是否过期（7天）
    if (authData.expiresAt && new Date(authData.expiresAt) < new Date()) {
      logout()
      return false
    }
    
    return authData.isAuthenticated === true
  } catch (error) {
    console.error('检查登录状态失败:', error)
    return false
  }
}

/**
 * 登录
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise<{success: boolean, message: string}>}
 */
export function login(username, password) {
  // 简单的登录验证（实际项目中应该调用后端API）
  // 这里使用硬编码的账号密码，您可以根据需要修改
  const validUsers = [
    { username: 'admin', password: 'admin123' },
    { username: 'user', password: 'user123' },
    { username: 'test', password: 'test123' }
  ]
  
  const user = validUsers.find(u => u.username === username && u.password === password)
  
  if (user) {
    const expiresAt = new Date()
    expiresAt.setDate(expiresAt.getDate() + 7) // 7天后过期
    
    const authData = {
      isAuthenticated: true,
      expiresAt: expiresAt.toISOString(),
      loginTime: new Date().toISOString()
    }
    
    const userData = {
      username: user.username,
      loginTime: new Date().toISOString()
    }
    
    localStorage.setItem(AUTH_KEY, JSON.stringify(authData))
    localStorage.setItem(USER_KEY, JSON.stringify(userData))
    
    // 触发登录事件
    window.dispatchEvent(new CustomEvent('authStateChanged', { detail: { isAuthenticated: true } }))
    
    return { success: true, message: '登录成功' }
  } else {
    return { success: false, message: '用户名或密码错误' }
  }
}

/**
 * 登出
 */
export function logout() {
  localStorage.removeItem(AUTH_KEY)
  localStorage.removeItem(USER_KEY)
  
  // 触发登出事件
  window.dispatchEvent(new CustomEvent('authStateChanged', { detail: { isAuthenticated: false } }))
}

/**
 * 获取当前用户信息
 * @returns {Object|null}
 */
export function getCurrentUser() {
  try {
    const userData = localStorage.getItem(USER_KEY)
    if (userData) {
      return JSON.parse(userData)
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
  return null
}

/**
 * 注册新用户（可选功能）
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @returns {Promise<{success: boolean, message: string}>}
 */
export function register(username, password) {
  // 简单的注册逻辑（实际项目中应该调用后端API）
  const usersKey = 'codingSpace_users'
  
  try {
    let users = []
    const stored = localStorage.getItem(usersKey)
    if (stored) {
      users = JSON.parse(stored)
    }
    
    // 检查用户名是否已存在
    if (users.find(u => u.username === username)) {
      return { success: false, message: '用户名已存在' }
    }
    
    // 添加新用户
    users.push({ username, password })
    localStorage.setItem(usersKey, JSON.stringify(users))
    
    return { success: true, message: '注册成功，请登录' }
  } catch (error) {
    console.error('注册失败:', error)
    return { success: false, message: '注册失败，请重试' }
  }
}

