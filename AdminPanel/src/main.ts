import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
import './style/index'
import { initThemeListener } from './utils/theme'

const app = createApp(App)

app.use(ArcoVue)
app.use(router)

app.mount('#app')

// 初始化 PS 主题监听（自动跟随 PS 主题变换颜色）
initThemeListener()

console.log('🎨 Designer Admin Panel 已启动')

