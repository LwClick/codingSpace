<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <div class="logo-container">
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
        <p class="login-subtitle">欢迎回来，请登录您的账户</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="请输入用户名"
            required
            autocomplete="username"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="请输入密码"
            required
            autocomplete="current-password"
            class="form-input"
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="login-btn" :disabled="isLoading">
          <span v-if="!isLoading">登录</span>
          <span v-else>登录中...</span>
        </button>
      </form>


    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../utils/auth.js'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

async function handleLogin() {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const result = await login(username.value, password.value)
    
    if (result.success) {
      // 登录成功，跳转到首页或之前访问的页面
      const redirect = router.currentRoute.value.query.redirect || '/'
      router.push(redirect)
    } else {
      errorMessage.value = result.message
    }
  } catch (error) {
    errorMessage.value = '登录失败，请重试'
    console.error('登录错误:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: 
    radial-gradient(circle at 20% 50%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 40% 20%, rgba(0, 100, 255, 0.1) 0%, transparent 50%),
    linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

.login-container::before {
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

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.login-box {
  width: 100%;
  max-width: 420px;
  background: rgba(10, 14, 39, 0.8);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(0, 255, 255, 0.2);
  position: relative;
  z-index: 1;
}

.login-box::before {
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
  border-radius: 20px 20px 0 0;
}

@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.login-header {
  text-align: center;
  margin-bottom: 35px;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 15px;
}

.taiji-logo {
  width: 50px;
  height: 50px;
  animation: rotate 10s linear infinite;
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.5));
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

.login-header h1 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2.2em;
  font-weight: 700;
  letter-spacing: 2px;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
}

.login-subtitle {
  color: rgba(224, 224, 224, 0.7);
  font-size: 0.95em;
  margin: 0;
}

.login-form {
  margin-bottom: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  color: #00ffff;
  font-size: 0.9em;
  font-weight: 600;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 18px;
  background: rgba(10, 14, 39, 0.6);
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 10px;
  color: #e0e0e0;
  font-size: 1em;
  outline: none;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
  background: rgba(10, 14, 39, 0.8);
}

.form-input::placeholder {
  color: rgba(224, 224, 224, 0.4);
}

.error-message {
  background: rgba(255, 77, 77, 0.2);
  border: 1px solid rgba(255, 77, 77, 0.5);
  color: #ff6b6b;
  padding: 12px;
  border-radius: 8px;
  font-size: 0.9em;
  margin-bottom: 15px;
  text-align: center;
}

.login-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  border: 2px solid rgba(0, 255, 255, 0.5);
  border-radius: 10px;
  color: #00ffff;
  font-size: 1.1em;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.login-btn:hover::before {
  left: 100%;
}

.login-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #0a0e27;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  transform: translateY(-2px);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.demo-info {
  color: rgba(224, 224, 224, 0.6);
  font-size: 0.85em;
  margin: 0;
  line-height: 1.6;
}

.demo-account {
  color: #00ffff;
  font-weight: 600;
  margin: 0 5px;
}

.demo-separator {
  color: rgba(224, 224, 224, 0.4);
  margin: 0 8px;
}

@media (max-width: 480px) {
  .login-box {
    padding: 30px 20px;
  }
  
  .login-header h1 {
    font-size: 1.8em;
  }
  
  .demo-info {
    font-size: 0.75em;
  }
}
</style>

