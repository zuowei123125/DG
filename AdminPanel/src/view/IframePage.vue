<template>
  <div class="iframe-container">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <a-button size="small" @click="goBack">
        <template #icon><icon-arrow-left /></template>
        返回
      </a-button>
      <span class="url-display">{{ currentUrl }}</span>
      <a-button size="small" @click="reload">
        <template #icon><icon-refresh /></template>
        刷新
      </a-button>
      <a-button size="small" @click="openExternal">
        <template #icon><icon-export /></template>
        外部打开
      </a-button>
    </div>
    
    <!-- 加载指示器 -->
    <div v-if="loading" class="loading-overlay">
      <a-spin size="32" />
      <p>加载中...</p>
    </div>
    
    <!-- iframe -->
    <iframe 
      ref="frameRef"
      :src="currentUrl"
      class="main-frame"
      @load="onFrameLoad"
      @error="onFrameError"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { IconArrowLeft, IconRefresh, IconExport } from '@arco-design/web-vue/es/icon'

const router = useRouter()
const frameRef = ref<HTMLIFrameElement | null>(null)
const loading = ref(true)

const currentUrl = ref(
  localStorage.getItem('adminPanelUrl') || (
    __DEV__ 
      ? 'http://localhost:5173' 
      : 'https://app.aidg168.uk'
  )
)

function goBack() {
  router.push('/')
}

function reload() {
  loading.value = true
  if (frameRef.value) {
    frameRef.value.src = currentUrl.value
  }
}

function openExternal() {
  window.open(currentUrl.value, '_blank')
}

function onFrameLoad() {
  loading.value = false
  console.log('✅ iframe 加载完成')
}

function onFrameError(e: Event) {
  loading.value = false
  console.error('❌ iframe 加载失败', e)
}

onMounted(() => {
  // 设置超时
  setTimeout(() => {
    if (loading.value) {
      console.warn('⏱️ 加载超时')
    }
  }, 30000)
})
</script>

<style scoped>
.iframe-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--ps-bg, #1e1e1e);
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--color-bg-2, #2d2d2d);
  border-bottom: 1px solid var(--ps-border, #444);
}

.url-display {
  flex: 1;
  font-size: 12px;
  color: var(--ps-text, #aaa);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.main-frame {
  flex: 1;
  width: 100%;
  border: none;
}

.loading-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: var(--ps-text, white);
  z-index: 10;
}

.loading-overlay p {
  margin-top: 12px;
}
</style>

