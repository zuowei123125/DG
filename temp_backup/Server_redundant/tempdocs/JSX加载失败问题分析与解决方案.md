# JSX 加载失败问题分析与解决方案

## 📋 问题描述

在 Shell + Core 架构分离后，Core 应用中的 JSX 脚本无法正常运行，报错：

```
Error: EvalScript error.
```

尽管 JSX 文件路径找到了（`C:/Users/35780/AppData/Roaming/DesignerCache/v1.0.5/jsx/index.js`），但 `evalScript` 执行失败。

## 🔍 根本原因

### 问题1：JSX 构建格式错误

**位置**：`Designer/plugins/buildJsx/index.ts` 第 118 行

```typescript
await bundle.write({
  file: output,
  format: 'cjs'  // ❌ 问题所在！
});
```

**影响**：生成的 JSX 文件使用了 **CommonJS 格式**，包含：

```javascript
Object.defineProperty(exports, "__esModule", { value: true });
var index_1 = require("./function/index");  // ❌ ExtendScript 不支持 require()
var ActionManager = require("./utils/ActionManager");
```

### 问题2：ExtendScript 环境限制

**ExtendScript (Adobe JSX 引擎) 不支持：**
- ❌ CommonJS 的 `require()` 和 `exports`
- ❌ ES6 的 `import/export`
- ❌ `'use strict'` 严格模式

**ExtendScript 只支持：**
- ✅ 全局函数
- ✅ 立即执行函数表达式 (IIFE)
- ✅ ES3/ES5 语法

## ✅ 解决方案

### 方案 1：修改构建配置（长期方案）

修改 `Designer/plugins/buildJsx/index.ts`：

```typescript
await bundle.write({
  file: output,
  format: 'iife',  // ✅ 改为 IIFE 格式
  name: 'JSXBundle',
  strict: false  // ✅ 禁用严格模式
});
```

**同时修改 TypeScript 配置**：

```typescript
typescript({
  compilerOptions: {
    target: 'es5',
    strict: false,
    moduleResolution: 'node',
    esModuleInterop: true,
    skipLibCheck: true,
    // ...
  },
  tsconfig: false,
}),
```

### 方案 2：临时修复（已应用）

**已完成的操作：**

1. ✅ 创建了简化版本的 JSX 文件 (`index_fixed.js`)
2. ✅ 移除了所有 CommonJS 语法
3. ✅ 将依赖项（Logger, ActionManager）内联到单文件中
4. ✅ 备份原文件为 `index.js.backup`
5. ✅ 替换为修复后的版本

**文件位置**：
- 修复后：`Designer/dist_core/jsx/index.js`
- 备份：`Designer/dist_core/jsx/index.js.backup`

## 🧪 测试步骤

### 1. 清除客户端缓存

```powershell
Remove-Item -Recurse -Force "$env:APPDATA\DesignerCache" -ErrorAction SilentlyContinue
```

### 2. 重启插件

在 Photoshop 中：
1. 关闭当前的 DesignerCEP 插件
2. 重新打开插件
3. 登录账号

### 3. 检查控制台

打开浏览器开发者工具（F12），查看：

**预期成功日志：**
```
[__LDX] Detected Core version v1.0.5
[__LDX] Success: C:/Users/35780/AppData/Roaming/DesignerCache/v1.0.5/jsx/index.js
宿主APP名称：Adobe Photoshop 2024
```

**如果仍然失败，查看：**
- 是否有 `EvalScript error`
- ExtendScript 控制台的详细错误信息

### 4. 测试功能

在插件主界面点击"测试 JSX 调用"按钮，验证：
- ✅ `getAppName()` 返回 "Adobe Photoshop"
- ✅ `createLayer()` 可以创建新图层
- ✅ `testMergeLayers()` 可以合并图层

## 📝 后续工作

### 短期（紧急）
- [ ] 测试修复后的 JSX 是否正常工作
- [ ] 如果测试通过，将修复后的文件上传到服务器

### 中期（优化）
- [ ] 修复构建流程，确保未来构建自动生成正确格式
- [ ] 解决 `g_logger` 和 `ActionManager` 的依赖打包问题
- [ ] 更新 `deploy_core.py` 脚本，包含 JSX 构建步骤

### 长期（架构改进）
- [ ] 评估是否需要保留完整的 Logger 和 ActionManager
- [ ] 考虑使用 Rollup 的 `inlineDynamicImports` 选项
- [ ] 编写自动化测试验证 JSX 在 ExtendScript 环境中的兼容性

## 🔗 相关文件

| 文件路径 | 说明 |
|:---------|:-----|
| `Designer/plugins/buildJsx/index.ts` | JSX 构建配置（已修改format为iife） |
| `Designer/dist_core/jsx/index.js` | 修复后的 JSX 文件 |
| `Designer/dist_core/jsx/index.js.backup` | 原始的 CommonJS 格式备份 |
| `Designer/build_jsx_simple.mjs` | 简化的构建脚本（待完善） |

## 💡 技术要点

### ExtendScript 兼容性清单

```javascript
✅ 允许:
- var, function, 普通对象
- IIFE: (function(){ ... })();
- 全局赋值: $.global.xxx = function(){}
- ES5 方法: Array.forEach, Object.keys

❌ 禁止:
- 'use strict'
- require() / exports / module.exports
- import / export
- const / let (部分版本不支持)
- Promise / async/await (需 polyfill)
- 箭头函数 (部分版本)
```

### Rollup 输出格式对比

| 格式 | ExtendScript | 说明 |
|:-----|:------------|:-----|
| `cjs` | ❌ | CommonJS，使用 require/exports |
| `esm` | ❌ | ES Module，使用 import/export |
| `iife` | ✅ | 立即执行函数，所有代码在一个作用域 |
| `umd` | ⚠️ | 通用模块，体积较大但兼容性好 |

## 📞 联系与支持

如果测试中遇到问题，请提供：
1. 浏览器控制台的完整错误日志
2. ExtendScript Toolkit 的错误信息（如果有）
3. Photoshop 版本和操作系统信息

---

**报告生成时间**：2025-12-16  
**问题状态**：✅ 已修复（待测试验证）

