<template>
  <div class="home-view">
    <header class="header">
      <h1>Designer 管理后台</h1>
      <p class="subtitle">集成开发与资源管理中心</p>
    </header>

    <div class="card-grid">
      <div class="card" @click="goToIframe">
        <div class="icon">🌐</div>
        <h3>外部预览</h3>
        <p>嵌入式浏览器页面查看</p>
      </div>
      
      <div class="card" @click="toggleTheme">
        <div class="icon">{{ isDark ? '🌙' : '☀️' }}</div>
        <h3>主题切换</h3>
        <p>当前: {{ isDark ? '深色模式' : '浅色模式' }}</p>
      </div>
    </div>

    <div class="status-panel">
      <h3>系统状态</h3>
      <div class="status-item">
        <span>版本:</span>
        <code>{{ version }}</code>
      </div>
      <div class="status-item">
        <span>运行模式:</span>
        <span class="badge" :class="{ dev: isDev }">{{ isDev ? '开发模式' : '生产模式' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useTheme } from '@/hooks/useTheme'

const router = useRouter()
const { isDark, toggleTheme } = useTheme()

const version = __VERSION__
const isDev = __DEV__

const goToIframe = () => {
  router.push('/iframe')
}
</script>

<style scoped>
.home-view {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  margin: 10px 0 0;
  opacity: 0.6;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-4px);
  border-color: #4facfe;
}

.icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.status-panel {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 16px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-family: monospace;
}

.badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.badge.dev {
  background: #f39c12;
  color: #000;
}
</style>
