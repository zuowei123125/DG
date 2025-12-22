import { logger } from '@/utils/logger';

/**
 * 初始化 Arco Design 暗色主题
 * 为 CEP 插件环境配置适配的暗色主题
 */
export function initTheme() {
    // 设置 Arco Design 主题为暗色模式
    document.body.setAttribute('arco-theme', 'dark');

    // 如果需要自定义 Arco Design 的颜色变量，可以在这里设置
    const root = document.documentElement;

    // 设置主色调为蓝色（可根据需要调整）
    root.style.setProperty('--primary-6', 'rgb(64, 128, 255)');

    // 可选：设置背景色以适应 CEP 插件
    root.style.setProperty('--color-bg-1', '#1a1a1a');
    root.style.setProperty('--color-bg-2', '#252525');
    root.style.setProperty('--color-bg-3', '#323232');

    logger.log('✅ Arco Design 暗色主题已初始化');
}
