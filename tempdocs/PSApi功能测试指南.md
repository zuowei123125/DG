# PSApi 功能测试指南

## 📋 已完成的修改

### 1. JSX 端（`src/jsx/index.ts`）

**添加的内容：**
```typescript
import { PSApi } from "./function/ps/api"  // 导入 PSApi 类

const psApi = new PSApi()  // 实例化 PSApi

// 新增测试函数
export function testPSApi() {
  try {
      const selectLength = psApi.layer.getSelectLength();  // 调用 PSApi 的方法
      
      return JSON_EX.stringify({ 
        success: true, 
        message: "PSApi 调用成功！",
        selectLength: selectLength,
        info: "当前选中的图层数量: " + selectLength
      });
  } catch (error: any) {
      return JSON_EX.stringify({ error: error.toString() });
  }
}

// 暴露到全局
($.global as any).testPSApi = testPSApi;
```

### 2. 前端 API（`src/api/jsxApi/evalJSX.ts`）

**添加的内容：**
```typescript
testPSApi: async () => {
    const jsonStr = await cep.evalScript("testPSApi()");
    const res = JSON.parse(jsonStr);
    return res;
}
```

### 3. 前端界面（`src/view/Home.vue`）

**添加的内容：**
- ✅ 新增"测试 PSApi"按钮
- ✅ 添加 `handleTestPSApi()` 处理函数

## 🧪 测试步骤

### 步骤 1：重新构建（如果使用简化版）

如果您还在使用临时的简化版 JSX，现在可以：

**选项 A：使用简化版测试（推荐先测）**
```powershell
# 当前的 dist_core/jsx/index.js 已经包含简化版
# 直接测试即可
```

**选项 B：重新构建完整版（包含 PSApi）**
```powershell
cd D:\main\DesignerCEP\Designer

# 重新构建 Core（会包含新的 testPSApi 函数）
npm run build:core

# 如果构建失败，需要先修复构建流程
# 或者手动更新 dist_core/jsx/index.js
```

### 步骤 2：清除缓存

```powershell
Remove-Item -Recurse -Force "$env:APPDATA\DesignerCache" -ErrorAction SilentlyContinue
```

### 步骤 3：在 Photoshop 中测试

1. **打开 Photoshop**
2. **打开 DesignerCEP 插件**
3. **登录账号**（会下载最新的 Core）
4. **在主界面点击"测试 PSApi"按钮**

### 步骤 4：观察结果

**预期成功的结果：**

**控制台日志：**
```
[__LDX] Detected Core version v1.0.5
[__LDX] Success: C:/Users/.../jsx/index.js
Call testPSApi - Testing PSApi from api.ts
```

**前端界面：**
- 弹出成功提示：`PSApi 调用成功！ - 当前选中的图层数量: 1`
- 显示选中图层数（如果没选图层则为 0）

**如果失败：**
- 查看浏览器控制台的错误信息
- 查看 ExtendScript Toolkit 的错误（如果有）

## 📊 测试场景

### 场景 1：没有选中图层
- **操作**：不选择任何图层，点击"测试 PSApi"
- **预期**：显示"选中图层数: 0"

### 场景 2：选中 1 个图层
- **操作**：在 PS 中选中 1 个图层，点击"测试 PSApi"
- **预期**：显示"选中图层数: 1"

### 场景 3：选中多个图层
- **操作**：按住 Ctrl/Cmd 选中多个图层，点击"测试 PSApi"
- **预期**：显示"选中图层数: N"（N 为实际选中数量）

## 🎯 测试的意义

### 如果测试成功，证明：

1. ✅ **可以在 JSX 中使用完整的 `api.ts`**
2. ✅ **PSApi 类的方法可以正常调用**
3. ✅ **面向对象的写法在 ExtendScript 中运行正常**
4. ✅ **可以放心使用 api.ts 中的所有功能**

### 如果测试成功，您可以：

```typescript
// 在 src/jsx/index.ts 中使用任何 PSApi 的功能

// 示例 1：图层操作
export function selectLayerById(id: number) {
  psApi.layer.onIdSelectLayer(id);
  return JSON_EX.stringify({ success: true });
}

// 示例 2：文档操作
export function getDocumentSize() {
  const size = psApi.doc.getSize();
  return JSON_EX.stringify({ 
    width: size.cx, 
    height: size.cy 
  });
}

// 示例 3：颜色操作
export function setFillColor(hex: string) {
  const col = new SolidColor();
  col.rgb.hexValue = hex;
  psApi.activeLayer.shape.setFillColor(true, col);
  return JSON_EX.stringify({ success: true });
}

// 示例 4：字体操作
export function changeFontFamily(postScriptName: string, name: string, style: string) {
  psApi.font.setFontName(postScriptName, name, style);
  return JSON_EX.stringify({ success: true });
}
```

## 🚨 常见问题

### Q1: 点击按钮没有反应
**原因：** JSX 未加载或函数未暴露到全局  
**解决：** 
- 检查控制台是否有 `[__LDX] Success` 日志
- 确认 `testPSApi` 已添加到 `$.global`

### Q2: 报错 "PSApi is not defined"
**原因：** 构建时未包含 `api.ts`  
**解决：**
- 确认 `src/jsx/index.ts` 中有 `import { PSApi } from "./function/ps/api"`
- 重新构建或检查构建配置

### Q3: 报错 "getSelectLength is not a function"
**原因：** PSApi 的方法没有正确编译  
**解决：**
- 检查 `api.ts` 是否有语法错误
- 确认构建格式为 IIFE（我们已修改）
- 查看 `dist_core/jsx/index.js` 是否包含 PSApi 的代码

### Q4: 构建时报错 "g_logger is not exported"
**原因：** 模块打包问题（我们之前遇到的）  
**解决：**
- 暂时使用简化版测试
- 或者手动修复构建流程
- 或者等待我们修复完整版构建

## 💡 下一步计划

### 如果测试通过：
1. ✅ 确认可以使用完整的 `api.ts`
2. 🔄 修复完整版的构建流程
3. 📦 重新打包包含所有功能的 Core
4. 🚀 上传到服务器供用户使用

### 如果测试失败：
1. 📝 记录详细的错误信息
2. 🔍 分析是构建问题还是代码问题
3. 🔧 逐步调试修复

---

**准备好了吗？开始测试吧！** 🚀

测试完成后，请告诉我：
- ✅ 测试成功还是失败
- 📋 控制台的完整日志
- 💬 遇到的任何问题或错误信息

