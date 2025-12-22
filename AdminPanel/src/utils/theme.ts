/// <reference types="types-for-adobe/Photoshop/2015.5"/>

/**
 * theme.ts
 * 处理 Photoshop 主题颜色同步
 * 支持两种模式：
 * 1. 直接 CEP 模式（CSInterface 可用）
 * 2. iframe 模式（通过 postMessage 接收主题）
 */

import { cep } from './cep';
import { logger } from './logger';

interface Color {
    red: number;
    green: number;
    blue: number;
    alpha: number;
}

interface PSThemeMessage {
    type: 'PS_THEME';
    theme: {
        bgColor: string;
        isLight: boolean;
        fontSize: number;
    };
}

/**
 * 将 Adobe 颜色对象转换为 CSS RGB 字符串
 */
function toHex(color: Color): string {
    const r = Math.round(color.red).toString(16).padStart(2, '0');
    const g = Math.round(color.green).toString(16).padStart(2, '0');
    const b = Math.round(color.blue).toString(16).padStart(2, '0');
    return `#${r}${g}${b}`;
}

/**
 * 计算颜色的亮度 (0-255)
 */
function getBrightness(color: Color): number {
    return (color.red * 299 + color.green * 587 + color.blue * 114) / 1000;
}

/**
 * 应用主题到页面
 */
function applyTheme(bgColor: string, isLight: boolean, fontSize?: number) {
    const root = document.documentElement;
    
    let textColorHex, borderColorHex, iconColorHex;

    if (isLight) {
        document.body.removeAttribute('arco-theme');
        textColorHex = '#222222';
        borderColorHex = '#d0d0d0';
        iconColorHex = '#333333';
    } else {
        document.body.setAttribute('arco-theme', 'dark');
        textColorHex = '#dfdfdf';
        borderColorHex = '#4a4a4a';
        iconColorHex = '#f0f0f0';
    }

    // 设置 CSS 变量
    root.style.setProperty('--ps-bg', bgColor);
    root.style.setProperty('--ps-text', textColorHex);
    root.style.setProperty('--ps-border', borderColorHex);
    root.style.setProperty('--ps-icon', iconColorHex);
    if (fontSize) {
        root.style.setProperty('--ps-font-size', `${fontSize}px`);
    }

    // Arco Design 主题变量
    root.style.setProperty('--color-bg-1', bgColor);
    root.style.setProperty('--color-bg-2', bgColor);
    root.style.setProperty('--color-bg-3', borderColorHex);
    root.style.setProperty('--color-text-1', textColorHex);
    root.style.setProperty('--color-border', borderColorHex);

    // 应用到 body
    document.body.style.backgroundColor = bgColor;
    document.body.style.color = textColorHex;
    
    logger.log(`[Theme] 已应用主题: ${isLight ? '浅色' : '深色'}, 背景: ${bgColor}`);
}

/**
 * 从 CSInterface 直接获取并更新主题
 */
export const updateTheme = () => {
    if (!cep.inCEP) {
        // 浏览器模式 - 使用默认深色主题
        applyTheme('#323232', false);
        return;
    }

    const hostEnv = cep.getHostEnvironment();
    if (!hostEnv) return;
    
    const skinInfo = hostEnv.appSkinInfo;
    const panelBgColor = skinInfo.panelBackgroundColor.color;
    const bgColorHex = toHex(panelBgColor);
    const brightness = getBrightness(panelBgColor);
    const isLight = brightness > 128;

    applyTheme(bgColorHex, isLight, skinInfo.baseFontSize);
};

/**
 * 处理来自父窗口的主题消息（iframe 模式）
 */
function handleThemeMessage(event: MessageEvent) {
    const data = event.data as PSThemeMessage;
    if (data && data.type === 'PS_THEME' && data.theme) {
        logger.log('[Theme] 收到父窗口主题消息');
        applyTheme(data.theme.bgColor, data.theme.isLight, data.theme.fontSize);
    }
}

/**
 * 初始化主题监听
 */
export const initThemeListener = () => {
    // 检测是否在 iframe 中运行
    const inIframe = window !== window.parent;
    
    if (inIframe) {
        // iframe 模式：监听来自父窗口的消息
        logger.log('[Theme] iframe 模式 - 监听 postMessage');
        window.addEventListener('message', handleThemeMessage);
        // 请求父窗口发送主题
        window.parent.postMessage({ type: 'REQUEST_THEME' }, '*');
    } else if (cep.inCEP) {
        // 直接 CEP 模式
        logger.log('[Theme] CEP 模式 - 直接监听主题变化');
        updateTheme();
        cep.addEventListener('com.adobe.csxs.events.ThemeColorChanged', updateTheme);
    } else {
        // 纯浏览器模式
        logger.log('[Theme] 浏览器模式 - 使用默认主题');
        applyTheme('#323232', false);
    }
};
