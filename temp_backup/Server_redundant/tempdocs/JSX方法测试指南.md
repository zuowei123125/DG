# JSX 方法测试指南

## 🎯 目标

测试 5 种不同的 JSX 实现方法，找出在 ExtendScript 环境中能正常运行的方式。

## 📋 测试方法列表

| 方法 | 实现方式 | 特点 |
|:-----|:---------|:-----|
| **方法1** | DOM API | 最简单，直接使用 PS 的 DOM 对象 |
| **方法2** | ActionManager | 使用 ActionDescriptor，更底层 |
| **方法3** | Object Helper | 使用对象字面量封装 |
| **方法4** | ES3 Class | 使用原型链的类实现 |
| **方法5** | PSApi Style | 模仿完整的 PSApi 结构 |

## 🧪 快速测试步骤

### 1. 替换 JSX 文件

```powershell
# 方式A：直接复制到缓存（推荐）
Copy-Item Designer\test_jsx_methods.js "$env:APPDATA\DesignerCache\v1.0.7\jsx\index.js" -Force

# 方式B：或者重新打包上传
# （如果方式A不行，说明缓存路径不对）
```

### 2. 在浏览器控制台测试

打开 Photoshop 插件，按 F12 打开控制台，逐个测试：

```javascript
// 测试方法1（DOM API）
cep.evalScript("createLayerMethod1('测试图层1')").then(r => console.log('方法1:', r))

// 测试方法2（ActionManager）
cep.evalScript("createLayerMethod2('测试图层2')").then(r => console.log('方法2:', r))

// 测试方法3（Object Helper）
cep.evalScript("createLayerMethod3('测试图层3')").then(r => console.log('方法3:', r))

// 测试方法4（ES3 Class）
cep.evalScript("createLayerMethod4('测试图层4')").then(r => console.log('方法4:', r))

// 测试方法5（PSApi Style）
cep.evalScript("createLayerMethod5('测试图层5')").then(r => console.log('方法5:', r))

// 测试获取图层数量
cep.evalScript("getLayerCount()").then(r => console.log('图层数量:', r))
```

### 3. 观察结果

**成功的结果示例：**
```json
{
  "success": true,
  "method": "DOM API",
  "layerName": "测试图层1"
}
```

**失败的结果示例：**
```json
{
  "error": "..."
}
```

## 📊 预期哪个会成功？

根据 ExtendScript 的特性，**最可能成功的是**：

1. ✅ **方法1（DOM API）** - 最简单直接
2. ✅ **方法3（Object Helper）** - 使用对象字面量
3. ⚠️ **方法2（ActionManager）** - 可能因为 API 调用问题失败
4. ⚠️ **方法4（ES3 Class）** - 依赖原型链
5. ⚠️ **方法5（PSApi Style）** - 最复杂，可能有嵌套问题

## 🔧 如果都失败了

如果所有方法都失败，可能的原因：

1. **JSX 文件没有被加载**
   - 检查控制台是否有 `Test JSX Methods Loaded` 日志
   
2. **路径不对**
   - 检查 `[__LDX]` 日志显示的路径
   - 手动找到该路径，确认文件内容

3. **ExtendScript 语法错误**
   - 在 ExtendScript Toolkit 中打开文件检查

## 💡 成功后的下一步

找到能工作的方法后：

1. 📝 **记录成功的方法**（如"方法1成功"）
2. 🔄 **使用该方法重写所有 JSX 函数**
3. 📦 **重新构建和打包 Core**
4. 🚀 **发布到服务器**

## 🎨 添加前端测试按钮（可选）

在 `Home.vue` 中添加测试按钮：

```vue
<a-button @click="testMethod1">测试方法1</a-button>
<a-button @click="testMethod2">测试方法2</a-button>
<a-button @click="testMethod3">测试方法3</a-button>
<a-button @click="testMethod4">测试方法4</a-button>
<a-button @click="testMethod5">测试方法5</a-button>
```

```typescript
const testMethod1 = async () => {
  const res = await jsxApi.evalScript("createLayerMethod1('测试1')");
  console.log('方法1结果:', res);
  Message.info(res);
};
// ... 类似地添加其他方法
```

---

**现在开始测试吧！** 告诉我哪个方法能成功 🎯

