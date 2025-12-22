/**
 * 在你的网站（https://app.aidg168.uk）中添加此代码
 * 用于接收来自 Photoshop CEP 插件的主题信息
 */

// 监听来自 PS 插件的主题消息
window.addEventListener('message', function(event) {
    // 安全检查（可选）
    // if (event.origin !== 'expected-origin') return;
    
    const data = event.data;
    
    // 检查是否是 PS 主题消息
    if (data && data.type === 'PS_THEME' && data.theme) {
        const theme = data.theme;
        
        console.log('📨 收到 PS 主题:', theme);
        // theme.bgColor: 背景颜色 (例如 'rgb(50, 50, 50)')
        // theme.isLight: 是否为浅色主题 (true/false)
        // theme.fontSize: 字体大小 (数字)
        
        // 应用主题到你的网站
        applyPSTheme(theme);
    }
});

// 应用 PS 主题到网站
function applyPSTheme(theme) {
    const root = document.documentElement;
    
    // 设置 CSS 变量
    root.style.setProperty('--ps-bg-color', theme.bgColor);
    root.style.setProperty('--ps-font-size', theme.fontSize + 'px');
    
    // 根据亮度切换主题
    if (theme.isLight) {
        // 浅色主题
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
        root.style.setProperty('--ps-text-color', '#222222');
    } else {
        // 深色主题
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
        root.style.setProperty('--ps-text-color', '#dfdfdf');
    }
    
    // 直接应用到 body
    document.body.style.backgroundColor = theme.bgColor;
    
    console.log('✅ PS 主题已应用');
}

// 可选：主动请求主题（如果插件已经加载）
window.parent.postMessage({ type: 'REQUEST_THEME' }, '*');

