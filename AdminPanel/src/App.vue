<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { useTheme } from '@/hooks/useTheme'

// 初始化主题
const { isDark } = useTheme()
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  /* 使用 PS 主题色 */
  background-color: var(--ps-bg, #323232);
  color: var(--ps-text, #e0e0e0);
}

.app-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--ps-bg, #323232);
  color: var(--ps-text, #e0e0e0);
}
</style>

