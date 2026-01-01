// 认证工具 - 管理用户登录状态
import api, { API_BASE_URL } from './api.js'
import { encryptPassword } from './encryption.js'

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
    
    // 检查是否有access_token
    if (!authData.access_token) {
      return false
    }
    
    return authData.isAuthenticated === true
  } catch (error) {
    console.error('检查登录状态失败:', error)
    return false
  }
}

/**
 * 获取访问token
 * @returns {string|null}
 */
export function getAccessToken() {
  try {
    const auth = localStorage.getItem(AUTH_KEY)
    if (!auth) return null
    
    const authData = JSON.parse(auth)
    return authData.access_token || null
  } catch (error) {
    console.error('获取token失败:', error)
    return null
  }
}

/**
 * 登录（使用加密密码）
 * @param {string} username - 用户名
 * @param {string} password - 明文密码
 * @returns {Promise<{success: boolean, message: string, data?: object}>}
 */
export async function login(username, password) {
  try {
    // 加密密码
    const encryptedPassword = await encryptPassword(password, API_BASE_URL)
    
    // 调用后端登录接口
    const response = await api.post('/api/v1/auth/login-encrypted', {
      username,
      encrypted_password: encryptedPassword
    })
    
    if (response.data && response.data.access_token) {
      const expiresAt = new Date()
      expiresAt.setDate(expiresAt.getDate() + 7) // 7天后过期
      
      const authData = {
        isAuthenticated: true,
        access_token: response.data.access_token,
        token_type: response.data.token_type,
        expiresAt: expiresAt.toISOString(),
        loginTime: new Date().toISOString()
      }
      
      const userData = {
        username: username,
        loginTime: new Date().toISOString()
      }
      
      localStorage.setItem(AUTH_KEY, JSON.stringify(authData))
      localStorage.setItem(USER_KEY, JSON.stringify(userData))
      
      // 触发登录事件
      window.dispatchEvent(new CustomEvent('authStateChanged', { 
        detail: { isAuthenticated: true } 
      }))
      
      return { 
        success: true, 
        message: '登录成功',
        data: response.data
      }
    } else {
      return { success: false, message: '登录失败，未收到有效token' }
    }
  } catch (error) {
    console.error('登录错误:', error)
    
    if (error.response) {
      // 服务器返回了错误响应
      const status = error.response.status
      const detail = error.response.data?.detail || '登录失败'
      
      if (status === 401) {
        return { success: false, message: '用户名或密码错误' }
      } else if (status === 403) {
        return { success: false, message: '用户账户已被禁用' }
      } else if (status === 400) {
        return { success: false, message: detail }
      } else {
        return { success: false, message: `登录失败: ${detail}` }
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      return { success: false, message: '无法连接到服务器，请检查网络连接' }
    } else {
      // 其他错误
      return { success: false, message: error.message || '登录失败，请重试' }
    }
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

