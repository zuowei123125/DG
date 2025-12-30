/**
 * 构建客户端启动器（Launcher）
 * 
 * 这个脚本只生成一个简单的 CEP 插件：
 * - index.html（跳转到服务器）
 * - manifest.xml（CEP 配置）
 * - 图标等资源
 * 
 * 用法：npx ts-node scripts/buildLauncher.ts
 */

import * as fs from 'fs';
import * as path from 'path';

// ========== 配置 ==========
const CONFIG = {
  // 服务器地址（客户打开插件后跳转到这里）
  serverURL: 'https://aidg168.uk/app/#/login',
  
  // CEP 插件信息
  name: 'Designer',
  id: 'com.designer.launcher',
  version: '1.0.0',
  displayName: '超级套版',
  
  // 面板大小
  panel: {
    width: 450,
    height: 600,
    minWidth: 400,
    minHeight: 500,
  },
  
  // 支持的 Adobe 软件
  hosts: [
    { name: 'PHXS', version: '[0.0,99.9]' },  // Photoshop
    { name: 'ILST', version: '[0.0,99.9]' },  // Illustrator
    { name: 'AEFT', version: '[0.0,99.9]' },  // After Effects
    { name: 'PPRO', version: '[0.0,99.9]' },  // Premiere Pro
  ],
  
  // 输出目录
  outputDir: 'dist/Launcher',
};

// ========== 模板 ==========

// 跳转 HTML
const htmlTemplate = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${CONFIG.displayName}</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1e1e1e;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            box-sizing: border-box;
        }
        .loading {
            text-align: center;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid #333;
            border-top-color: #0078d4;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .message {
            font-size: 14px;
            opacity: 0.8;
        }
        .error {
            color: #ff6b6b;
            display: none;
        }
    </style>
</head>
<body>
    <div class="loading">
        <div class="spinner"></div>
        <p class="message">正在连接服务器...</p>
        <p class="error" id="error">连接失败，请检查网络</p>
    </div>
    
    <script>
        // 跳转到服务器
        const serverURL = '${CONFIG.serverURL}';
        
        // 延迟跳转，让用户看到加载动画
        setTimeout(function() {
            window.location.href = serverURL;
        }, 500);
        
        // 超时检测
        setTimeout(function() {
            document.getElementById('error').style.display = 'block';
        }, 10000);
    </script>
</body>
</html>`;

// manifest.xml
const manifestTemplate = `<?xml version="1.0" encoding="UTF-8"?>
<ExtensionManifest Version="6.0" ExtensionBundleId="${CONFIG.id}" ExtensionBundleVersion="${CONFIG.version}" 
    ExtensionBundleName="${CONFIG.name}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ExtensionList>
        <Extension Id="${CONFIG.id}.panel" Version="${CONFIG.version}" />
    </ExtensionList>
    <ExecutionEnvironment>
        <HostList>
            ${CONFIG.hosts.map(h => `<Host Name="${h.name}" Version="${h.version}" />`).join('\n            ')}
        </HostList>
        <LocaleList>
            <Locale Code="All" />
        </LocaleList>
        <RequiredRuntimeList>
            <RequiredRuntime Name="CSXS" Version="6.0" />
        </RequiredRuntimeList>
    </ExecutionEnvironment>
    <DispatchInfoList>
        <Extension Id="${CONFIG.id}.panel">
            <DispatchInfo>
                <Resources>
                    <MainPath>./index.html</MainPath>
                    <CEFCommandLine>
                        <Parameter>--enable-nodejs</Parameter>
                        <Parameter>--mixed-context</Parameter>
                    </CEFCommandLine>
                </Resources>
                <Lifecycle>
                    <AutoVisible>true</AutoVisible>
                </Lifecycle>
                <UI>
                    <Type>Panel</Type>
                    <Menu>${CONFIG.displayName}</Menu>
                    <Geometry>
                        <Size>
                            <Width>${CONFIG.panel.width}</Width>
                            <Height>${CONFIG.panel.height}</Height>
                        </Size>
                        <MinSize>
                            <Width>${CONFIG.panel.minWidth}</Width>
                            <Height>${CONFIG.panel.minHeight}</Height>
                        </MinSize>
                    </Geometry>
                    <Icons>
                        <Icon Type="Normal">./img/dark.png</Icon>
                        <Icon Type="RollOver">./img/highlight.png</Icon>
                        <Icon Type="DarkNormal">./img/dark.png</Icon>
                        <Icon Type="DarkRollOver">./img/highlight.png</Icon>
                    </Icons>
                </UI>
            </DispatchInfo>
        </Extension>
    </DispatchInfoList>
</ExtensionManifest>`;

// ========== 构建函数 ==========

function copyFolder(src: string, dest: string) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  
  const files = fs.readdirSync(src);
  for (const file of files) {
    const srcPath = path.join(src, file);
    const destPath = path.join(dest, file);
    
    if (fs.statSync(srcPath).isDirectory()) {
      copyFolder(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function build() {
  console.log('🚀 构建客户端启动器...\n');
  
  const outputDir = path.resolve(__dirname, '..', CONFIG.outputDir);
  
  // 1. 清理输出目录
  if (fs.existsSync(outputDir)) {
    fs.rmSync(outputDir, { recursive: true });
  }
  fs.mkdirSync(outputDir, { recursive: true });
  console.log('✓ 创建输出目录:', outputDir);
  
  // 2. 创建 CSXS 目录
  const csxsDir = path.join(outputDir, 'CSXS');
  fs.mkdirSync(csxsDir, { recursive: true });
  
  // 3. 写入 index.html
  fs.writeFileSync(path.join(outputDir, 'index.html'), htmlTemplate);
  console.log('✓ 生成 index.html');
  
  // 4. 写入 manifest.xml
  fs.writeFileSync(path.join(csxsDir, 'manifest.xml'), manifestTemplate);
  console.log('✓ 生成 CSXS/manifest.xml');
  
  // 5. 复制图标
  const imgSrc = path.resolve(__dirname, '../plugins/jsx/template/cep/img');
  const imgDest = path.join(outputDir, 'img');
  if (fs.existsSync(imgSrc)) {
    copyFolder(imgSrc, imgDest);
    console.log('✓ 复制图标');
  }
  
  console.log('\n========================================');
  console.log('✅ 构建完成！');
  console.log('========================================');
  console.log(`📁 输出目录: ${outputDir}`);
  console.log(`🔗 跳转地址: ${CONFIG.serverURL}`);
  console.log('\n下一步：');
  console.log('1. 使用 ZXPSignCmd 签名打包成 .zxp');
  console.log('2. 或直接复制到 Adobe CEP 扩展目录测试');
}

// 执行
build();

