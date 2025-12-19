# 壳架构 (Shell Architecture) 改造计划

为了实现“登录即更新”和“代码保护”，我们将把现有的 `DesignerCEP` 单体项目拆分为 **壳 (Shell)** 和 **核 (Core)** 两部分。

## 1. 架构概览

| 模块      | 名称              | 职责                                                                                                 | 部署位置                                 | 更新频率                         |
| :-------- | :---------------- | :--------------------------------------------------------------------------------------------------- | :--------------------------------------- | :------------------------------- |
| **Shell** | 启动器 (Launcher) | 1. 负责 CEP 扩展的安装与注册<br>2. 负责用户登录鉴权<br>3. **下载并解压** Core 包<br>4. 跳转加载 Core | **本地用户电脑**<br>(安装在 PS 扩展目录) | 极低<br>(仅当下载逻辑变更时更新) |
| **Core**  | 业务核 (Business) | 1. 包含所有 Vue 业务页面<br>2. 包含核心 JSX 脚本<br>3. 通过 Shell 注入的变量与宿主交互               | **远程服务器**<br>(ZIP 压缩包)           | 极高<br>(随时发布新功能)         |

---

## 2. 目录结构改造建议

目前的 `Designer/` 目录将作为**核心业务仓库**，我们需要在其中增加一个专门构建 Shell 的入口。

```
Designer/
  ├── package.json
  ├── vite.config.ts        # [Core配置] 构建业务代码 (输出 dist/core)
  ├── vite.shell.config.ts  # [Shell配置] 构建启动器代码 (输出 dist/shell)
  │
  ├── src/
  │   ├── main.ts           # [Core入口] 业务主入口 (现在的代码)
  │   ├── App.vue           # [Core] 业务主界面
  │   │
  │   └── launcher/         # [Shell] 启动器模块 (NEW)
  │       ├── main.ts       # [Shell入口]
  │       ├── App.vue       # [Shell] 登录与更新进度条界面
  │       ├── updater.ts    # [Shell] 下载/解压/校验逻辑 (Node.js)
  │       └── login.ts      # [Shell] 登录逻辑
  │
  └── dist/
      ├── shell/            # 打包结果：这是给用户安装的 ZXP
      │    ├── CSXS/manifest.xml
      │    ├── index.html   (登录器)
      │    └── node_modules (含 fs/adm-zip 等必要依赖)
      │
      └── core/             # 打包结果：这是传到服务器的 UPDATE.zip
           ├── index.html   (业务界面)
           ├── assets/
           └── jsx/         (加密后的 JSX)
```

## 3. 核心运行流程 (Workflow)

### 3.1 启动阶段 (Shell)

1.  用户点击 PS 菜单，加载本地的 `dist/shell/index.html`。
2.  **Shell App** 启动，不再加载复杂的业务组件，只显示登录框。
3.  用户输入账号密码 -> 请求服务器 `/api/login`。
4.  登录成功 -> 获取 Token 和 **最新 Core 版本号** (比如 `v1.0.2`)。

### 3.2 更新阶段 (Updater)

1.  检查本地 `C:/Users/xxx/AppData/Roaming/DesignerCache/v1.0.2/` 是否存在。
2.  **不存在 (有更新)**:
    - 显示进度条。
    - 从 CDN/服务器下载 `core-v1.0.2.zip`。
    - 使用 Node.js (`adm-zip`) 解压到上述目录。
3.  **存在**: 直接跳过。

### 3.3 注入阶段 (Launch)

1.  **加载 JSX**:
    - Shell 调用 `CSInterface.evalScript`。
    - 读取缓存目录下的 `v1.0.2/jsx/index.jsx` 内容。
    - 执行 `$.evalFile("C:/.../v1.0.2/jsx/index.jsx")`，把业务函数注入此 ExtendScript 上下文。
2.  **加载 UI**:
    - Shell 执行 `window.location.href = "file:///C:/.../v1.0.2/index.html"`。
3.  **接管**:
    - 浏览器跳转，页面变成业务界面。
    - 此时 `window.cep` 对象依然存在，业务界面可以继续调用刚刚注入的 JSX 函数。

## 4. 兼容性评估

**现有框架可以完全兼容，只需做以下调整**：

1.  **Vite 配置拆分**: 需要新增一个 `vite.shell.config.ts`，专门用来打包轻量级的 Shell。
2.  **Node.js 依赖**: Shell 需要打包进 `adm-zip` (解压用) 和 `axios` (下载用)。由于 CEP 支持 Node.js，这完全没问题。
3.  **路由模式**: 业务代码 (Core) 读取本地文件时，路由最好使用 `Hash` 模式 (`createWebHashHistory`)，避免 file 协议下的路径问题。

## 5. 下一步行动计划

1.  **[Shell]** 创建 `src/launcher` 目录，编写简单的登录+下载器 Demo。
2.  **[Build]** 配置 `vite.shell.config.ts`，尝试打包出一个只包含登录功能的 ZXP。
3.  **[Test]** 模拟远程更新，手动把现在的业务代码打包成 ZIP 放在本地服务器，测试 Shell 能否下载并跳转。
