# 混合方案 Demo 说明

## 🎯 核心思想

**本地 = 简单执行 | 服务器 = 复杂计算**

---

## 📋 Demo 示例

### 功能：创建智能配色图层

#### 流程：

```
1️⃣ 用户点击"智能配色"按钮

2️⃣ 前端发送请求到服务器
   POST /api/v1/jsx_demo/calculate-color
   {
     "layer_name": "智能配色_12345",
     "base_color": "#FF6B9D"
   }

3️⃣ 🔒 服务器执行核心算法（客户端看不到）
   - 根据图层名称计算最佳颜色
   - 计算最佳不透明度
   - 选择最佳混合模式
   
   → 返回结果：
   {
     "r": 255,
     "g": 120,
     "b": 180,
     "opacity": 85,
     "blend_mode": "overlay"
   }

4️⃣ 前端接收结果，执行简单 JSX
   - 创建图层
   - 应用服务器计算的参数
   - 填充颜色
```

---

## 🔐 安全对比

### 当前内联方式（全在前端）

**前端代码：**
```typescript
const jsx = `
    var layer = doc.artLayers.add();
    layer.opacity = 85;  // ⚠️ 算法暴露
    layer.blendMode = BlendMode.OVERLAY;
    // 复杂的颜色计算逻辑
    var r = 核心算法1();  // ⚠️ 可被看到
    var g = 核心算法2();  // ⚠️ 可被看到
    var b = 核心算法3();  // ⚠️ 可被看到
`;
```

❌ **问题：** 攻击者可以看到所有代码，复制算法

---

### 混合方式（计算在服务器）

**前端代码：**
```typescript
const colorResult = await fetch('/api/calculate-color', {...});
const { r, g, b, opacity } = colorResult;

const jsx = `
    var layer = doc.artLayers.add();
    layer.opacity = ${opacity};  // ✅ 只是应用参数
    color.rgb.red = ${r};         // ✅ 只是应用参数
    color.rgb.green = ${g};
    color.rgb.blue = ${b};
`;
```

**服务器代码（客户端看不到）：**
```python
# 🔒 核心算法在这里
def calculate_color(layer_name, base_color):
    # 复杂的颜色理论计算
    # 机器学习模型推荐
    # 你的独家算法
    return {r, g, b, opacity, blend_mode}
```

✅ **优势：** 攻击者只能看到"发送请求 → 应用结果"，看不到算法

---

## 📂 新增文件（不影响现有系统）

```
✅ 保留：
   Designer/src/api/jsxApi/inline/layer.ts     (原有内联 JSX)
   Designer/src/api/jsxApi/inline/document.ts  (原有内联 JSX)

➕ 新增：
   Server/app/api/v1/jsx_demo.py               (服务器计算 Demo)
   Designer/src/api/jsxApi/inline/hybrid-demo.ts  (混合调用 Demo)
```

**两种方式并存，互不影响！**

---

## 🚀 测试 Demo

1. **启动后端**
   ```bash
   cd Server
   python main.py
   ```

2. **启动前端开发模式**
   ```bash
   cd Designer
   npm run dev
   ```

3. **点击"智能配色"按钮**
   - 会调用服务器计算颜色
   - 然后在本地创建图层并应用

4. **查看控制台**
   - 可以看到发送的参数
   - 可以看到服务器返回的结果
   - **但看不到服务器端的计算逻辑！**

---

## 💡 扩展建议

你可以把**任何核心功能**改成这种方式：

| 功能 | 本地执行 | 服务器计算 |
|------|---------|-----------|
| 创建图层 | ✅ 简单创建 | ❌ |
| 智能配色 | ✅ 应用颜色 | ✅ 计算最佳颜色 |
| AI 设计 | ✅ 应用结果 | ✅ AI 模型推理 |
| 自动排版 | ✅ 移动元素 | ✅ 计算最佳位置 |
| 滤镜参数 | ✅ 应用滤镜 | ✅ 计算最佳参数 |

**核心算法都在服务器，客户端只是"执行器"！**

