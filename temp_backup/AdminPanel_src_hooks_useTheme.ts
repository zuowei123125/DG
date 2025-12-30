import { ref, onMounted, onUnmounted } from 'vue';
import { initThemeListener } from '@/utils/theme';

export function useTheme() {
  const isDark = ref(true);
  
  // 简易的判断当前是否是深色主题的逻辑
  // 实际逻辑由 utils/theme.ts 中的 updateTheme 处理，它会更新 body 的 arco-theme 属性
  const checkTheme = () => {
    isDark.value = document.body.getAttribute('arco-theme') === 'dark';
  };

  onMounted(() => {
    // 初始化并开始监听
    initThemeListener();
    
    // 初始检查
    checkTheme();

    // 监听 body 属性变化 (以便在 theme.ts 更新 body 属性时我们能感知到)
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'arco-theme') {
          checkTheme();
        }
      });
    });

    observer.observe(document.body, { attributes: true });

    // Cleanup
    onUnmounted(() => {
      observer.disconnect();
    });
  });

  return {
    isDark
  };
}
