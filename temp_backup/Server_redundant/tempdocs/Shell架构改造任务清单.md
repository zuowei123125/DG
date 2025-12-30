# Shell 架构改造任务清单 (增强版)

基于您提供的 `serveradmin` 和 `upload` 逻辑，我们引入了 **“用户分组 (Gray Release)”** 和 **“一键发布 (CI/CD)”** 机制。

## 1. 插件端 (Frontend - Shell)

Shell 端不需要太大变化，主要是版本检查接口需要携带用户信息。

- `src/launcher/utils/`
  - [ ] **增强版版本检查**:
    - 请求 `POST /api/check_update`
    - 参数: `{ username: "当前登录用户" }`
    - 逻辑: 服务端会根据用户所在的组，返回不同的版本。普通用户返回 `v1.0`，测试组用户返回 `v1.1-beta`。

## 2. 服务端 (Backend - Python)

参考 `serveradmin` 逻辑进行改造。

### 2.1 数据库结构升级

需要支持不同用户获取不同版本。

- **表 `psmark_group` (用户组)**:

  - `id`: int (主键)
  - `name`: string (组名，如 "Stable", "Beta")
  - `current_version`: string (该组当前使用的版本文件名，如 "release_v1.0.zip")
  - `comment`: string

- **表 `user` (原有表增强)**:
  - `group_id`: int (外键，关联 psmark_group)

### 2.2 接口逻辑增强

- `POST /api/check_update`:
  1.  根据 `username` 查 `group_id`。
  2.  查 `psmark_group` 表获取该组的 `current_version`。
  3.  返回该版本的下载地址。
  - **优势**: 您可以在后台把某个测试用户切到 "DevGroup"，他重启插件就会立刻下载最新的测试版，而其他用户不受影响。

---

## 3. 发布流程 (Publishing Workflow)

为了实现“上传时编译”，我们将编写一个自动化脚本。

### 3.1 自动化发布脚本 (`scripts/publish.ts`)

这个脚本将在您的开发机上运行，一键完成所有操作。

- **执行流程**:

  1.  **Compile**: 运行 `npm run build:core` (生成 `dist/core`)。
  2.  **Package**: 使用 `adm-zip` 将 `dist/core` 压缩为 `code_{timestamp}.zip`。
  3.  **Upload**: 调用服务端接口 `POST /archives` 将 ZIP 上传。
  4.  **Register (可选)**: 自动调用接口将新版本注册到数据库（可选）。

- **命令**:
  ```bash
  npm run publish  # 一键发布
  ```

### 3.2 服务端支持

- 确保 `POST /archives` 接口能接收文件并保存到 `archives/` 目录 (参考 `server.py` 已有逻辑)。

---

## 4. 后台管理工具 (Admin Tool)

您可以直接复用或升级现有的 PyQt 工具 (`upload/admin.py`)。

- **功能需求**:
  - [ ] **用户分理**: 设置用户的 `group_id`。
  - [ ] **版本指派**: 设置某个 Group 使用哪个 ZIP 版本。

---

## 5. 执行路线图

1.  **Day 1 (Publishing)**: 写好 `scripts/publish.ts`，确保能一键编译并上传 ZIP 到您的服务器。
2.  **Day 2 (Backend)**: 改造 Python 后端，加入 Group 表，在此基础上实现“根据用户返回版本”的接口。
3.  **Day 3 (Shell)**: 开发插件 Shell 的下载器，对接上述接口。
