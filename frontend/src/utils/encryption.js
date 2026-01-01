/**
 * RSA加密工具
 * 用于前端加密敏感数据（如密码）
 */
import JSEncrypt from 'jsencrypt'

// 公钥缓存
let cachedPublicKey = null
const PUBLIC_KEY_CACHE_KEY = 'codingSpace_rsa_public_key'
const PUBLIC_KEY_CACHE_EXPIRY = 24 * 60 * 60 * 1000 // 24小时

/**
 * 从后端获取RSA公钥
 * @param {string} apiBaseUrl - API基础URL
 * @returns {Promise<string>} 公钥PEM字符串
 */
export async function fetchPublicKey(apiBaseUrl = 'http://localhost:8000') {
  try {
    // 检查缓存
    const cached = localStorage.getItem(PUBLIC_KEY_CACHE_KEY)
    if (cached) {
      const { publicKey, timestamp } = JSON.parse(cached)
      const now = Date.now()
      // 如果缓存未过期，使用缓存的公钥
      if (now - timestamp < PUBLIC_KEY_CACHE_EXPIRY) {
        return publicKey
      }
    }

    // 从后端获取公钥
    const response = await fetch(`${apiBaseUrl}/api/v1/auth/public-key`)
    if (!response.ok) {
      throw new Error('获取公钥失败')
    }
    
    const data = await response.json()
    const publicKey = data.public_key

    // 缓存公钥
    localStorage.setItem(PUBLIC_KEY_CACHE_KEY, JSON.stringify({
      publicKey,
      timestamp: Date.now()
    }))

    return publicKey
  } catch (error) {
    console.error('获取RSA公钥失败:', error)
    throw error
  }
}

/**
 * 使用RSA公钥加密数据
 * @param {string} plainText - 明文
 * @param {string} publicKey - RSA公钥（PEM格式）
 * @returns {string} Base64编码的加密数据
 */
export function encryptWithRSA(plainText, publicKey) {
  try {
    const encrypt = new JSEncrypt()
    encrypt.setPublicKey(publicKey)
    const encrypted = encrypt.encrypt(plainText)
    
    if (!encrypted) {
      throw new Error('加密失败，请检查公钥格式')
    }
    
    return encrypted
  } catch (error) {
    console.error('RSA加密失败:', error)
    throw error
  }
}

/**
 * 加密密码（自动获取公钥并加密）
 * @param {string} password - 明文密码
 * @param {string} apiBaseUrl - API基础URL
 * @returns {Promise<string>} Base64编码的加密密码
 */
export async function encryptPassword(password, apiBaseUrl = 'http://localhost:8000') {
  try {
    // 获取公钥
    const publicKey = await fetchPublicKey(apiBaseUrl)
    
    // 加密密码
    const encryptedPassword = encryptWithRSA(password, publicKey)
    
    return encryptedPassword
  } catch (error) {
    console.error('密码加密失败:', error)
    throw new Error('密码加密失败，请重试')
  }
}

/**
 * 清除公钥缓存
 */
export function clearPublicKeyCache() {
  localStorage.removeItem(PUBLIC_KEY_CACHE_KEY)
  cachedPublicKey = null
}

