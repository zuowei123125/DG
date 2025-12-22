import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/view/Home.vue')
  },
  {
    path: '/iframe',
    name: 'IframePage',
    component: () => import('@/view/IframePage.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

