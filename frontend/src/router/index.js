import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Calendar from '../views/Calendar.vue'
import Login from '../views/Login.vue'
import { isAuthenticated } from '../utils/auth.js'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true } // 已登录用户不能访问登录页
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true } // 需要登录才能访问
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar,
    meta: { requiresAuth: true } // 需要登录才能访问
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 权限控制
router.beforeEach((to, from, next) => {
  const authenticated = isAuthenticated()

  // 如果路由需要登录，但用户未登录，跳转到登录页
  if (to.meta.requiresAuth && !authenticated) {
    next({
      path: '/login',
      query: { redirect: to.fullPath } // 保存原始路径，登录后可以跳转回来
    })
    return
  }

  // 如果路由需要未登录状态（如登录页），但用户已登录，跳转到首页
  if (to.meta.requiresGuest && authenticated) {
    next({ path: '/' })
    return
  }

  next()
})

export default router

