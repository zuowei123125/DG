# 🎨 CEP 插件 UI 适配完全指南

> **目标**：将网页版 UI 完美重构为 Adobe CEP 插件原生体验，对标行业顶尖竞品。

## 📋 目录

- [核心约束](#-核心约束)
- [问题诊断](#-问题诊断)
- [UI 重构方案](#-ui-重构方案)
- [样式系统 (Design System)](#-样式系统-design-system)
- [实施路线图](#-实施路线图)
- [验收标准](#-验收标准)

---

## � 核心约束

> [!IMPORTANT] > **CEP 插件的黄金法则**：
> 能够在 **280px** 宽度的面板中完整显示所有核心功能，且无需横向滚动。

### 尺寸规范 (Manifest.xml)

| 属性         | 值               | 说明                       |
| :----------- | :--------------- | :------------------------- |
| **默认尺寸** | `280px × 600px`  | 最小可用状态               |
| **最小尺寸** | `280px × 600px`  | 锁死最小宽度，防止布局崩坏 |
| **最大尺寸** | `600px × 4080px` | 允许垂直方向无限延伸       |

---

## 🔍 问题诊断

我们在将 Web UI 移植到 CEP 环境时，面临以下主要适配挑战：

```mermaid
graph TD
    A[Web UI (1200px+)] -->|❌ 侧边栏过宽| B(180px Nav)
    A -->|❌ 网格松散| C(Card Layout)
    A -->|❌ 组件巨大| D(Large Buttons/Inputs)

    B --> E[CEP Environment (280px)]
    C --> E
    D --> E

    E -->|导致| F[⚠️ 横向滚动条]
    E -->|导致| G[⚠️ 内容被截断]
    E -->|导致| H[⚠️ 操作效率低]
```

---

## 🛠 UI 重构方案

### 1. 导航栏 (Navigation)

**现状**：`180px` 宽度的侧边栏在 `280px` 的面板中占据了 64% 的空间。
**方案**：采用 **图标栏 (Icon Bar)** 模式。

| 调整项   | Web 版       | CEP 适配版                  |
| :------- | :----------- | :-------------------------- |
| **模式** | 展开式侧边栏 | 收缩式图标栏                |
| **宽度** | `180px`      | `40px`                      |
| **标签** | 文字 + 图标  | 仅图标 (Hover 显示 Tooltip) |

### 2. 信息卡片 (Info Cards)

**现状**：卡片布局在窄屏下挤压严重。
**方案**：**CSS Grid 自适应紧凑布局**。

> [!TIP]
> 使用 `grid-template-columns: repeat(3, 1fr)` 确保在 280px 宽度下也能整齐排列。

**代码对比**：

```vue
<!-- ✅ 推荐写法 -->
<div class="cep-info-grid">
  <div class="info-card">
    <div class="card-icon">⚡</div>
    <div class="card-data">
      <span class="label">积分</span>
      <span class="value">{{ points }}</span>
    </div>
  </div>
</div>
```

### 3. 功能入口 (Feature Grid)

**现状**：每个功能占据大块面积，包含描述文字。
**方案**：**应用抽屉风格 (App Drawer)**，仅保留图标和名称。

- **移除**：详细的功能描述文本。
- **缩小**：图标尺寸从 `32px` -> `24px`。
- **布局**：使用 `repeat(auto-fill, minmax(70px, 1fr))` 实现自动换行。

---

## 🎨 样式系统 (Design System)

为了让插件看起来像原生 PS 功能，我们需要覆盖 Arco Design 的默认样式。

> [!NOTE]
> 请在 `src/style/` 下创建 `cep-override.css` 并全局引入。

### 全局样式重写 (`cep-override.css`)

```css
:root {
  /* 定义紧凑型尺寸变量 */
  --cep-padding-base: 8px;
  --cep-font-size-base: 12px;
  --cep-btn-height: 28px;
}

/* 🟢 按钮微型化 */
.arco-btn {
  height: var(--cep-btn-height) !important;
  padding: 0 12px !important;
  font-size: var(--cep-font-size-base) !important;
  border-radius: 2px !important; /* PS 风格通常更方正 */
}

/* 🟢 输入框紧凑化 */
.arco-input-wrapper {
  height: var(--cep-btn-height) !important;
  padding: 0 8px !important;
}

/* 🟢 滚动条美化 (原生风格) */
::-webkit-scrollbar {
  width: 4px; /* 极细滚动条 */
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #505050;
  border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover {
  background: #6e6e6e;
}

/* 🟢 卡片与容器 */
.cep-container {
  padding: var(--cep-padding-base);
}
.arco-card-body {
  padding: 8px !important;
}
```

---

## � 实施路线图

1.  **配置 manifest**
    - 修改 `manifest.xml` 中的 geometry 配置，锁定最小宽度。
2.  **样式注入**
    - 创建并引入 `cep-override.css`。
3.  **组件改造**
    - **Home.vue**: 将 Sider `width` 设为 40，`collapsed` 设为 true。
    - **HomePage.vue**: 重写 Grid 布局，移除多余文字描述，使用紧凑型 Icon。
4.  **响应式测试**
    - 在浏览器中将视口宽度调整为 `280px` 进行极限测试。

---

## ✅ 验收标准 (Checklist)

请逐项核对以确保完美交付：

- [ ] **宽度测试**：在 280px 宽度下，无横向滚动条。
- [ ] **侧边栏**：宽度严格控制在 40px 以内。
- [ ] **字体**：正文不大于 12px，标题不大于 14px。
- [ ] **按钮**：高度不大于 28px (Small/Mini 尺寸)。
- [ ] **深色模式**：背景色与 PS 界面融合 (通常为 `#323232` 或 `#535353`)。
- [ ] **交互**：所有点击区域即使在小尺寸下也易于点击 (增加热区 padding 不增加视觉 margin)。

> [!WARNING] > **切记**：CEP 插件是工具属性极强的应用，**效率**高于**装饰**。尽量减少无用的留白和装饰性元素。
