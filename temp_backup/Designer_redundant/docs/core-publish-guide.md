# Core 应用发布流程

本文档描述如何构建和发布 Core 应用的新版本。

## 前置条件

- 后端服务器已运行
- 已完成代码修改并测试

## 发布步骤

### 1. 构建 Core 应用

```powershell
cd d:\main\DesignerCEP\Designer
npm run build:core
```

这会在 `dist_core/` 目录生成构建产物。

### 2. 重命名入口文件

构建后的入口文件是 `index-core.html`，需要重命名为 `index.html`：

```powershell
Move-Item -Path ".\dist_core\index-core.html" -Destination ".\dist_core\index.html" -Force
```

### 3. 打包为 ZIP

将版本号替换为新版本（如 `v1.0.4`）：

```powershell
$version = "v1.0.4"
Compress-Archive -Path ".\dist_core\*" -DestinationPath "..\Server\archives\core-$version.zip" -Force
```

### 4. 更新数据库

编辑 `Server/update_version.py`，将版本号改为新版本，然后运行：

```powershell
cd d:\main\DesignerCEP\Server
python update_version.py
```

或者直接执行 SQL：

```sql
UPDATE plugin_groups SET current_version_file='core-v1.0.4.zip' WHERE id=1;
```

### 5. 清除客户端缓存（测试时）

用户端需要清除旧缓存才能下载新版本：

```powershell
Remove-Item -Recurse -Force "$env:APPDATA\DesignerCache" -ErrorAction SilentlyContinue
```

## 一键发布脚本

可以创建一个 PowerShell 脚本自动执行以上步骤：

```powershell
# publish-core.ps1
param([string]$version = "v1.0.0")

# 1. Build
npm run build:core

# 2. Rename
Move-Item -Path ".\dist_core\index-core.html" -Destination ".\dist_core\index.html" -Force

# 3. Package
Compress-Archive -Path ".\dist_core\*" -DestinationPath "..\Server\archives\core-$version.zip" -Force

Write-Host "Created: core-$version.zip"
Write-Host "Remember to update database: python update_version.py"
```

使用方法：

```powershell
.\publish-core.ps1 -version "v1.0.5"
```

## 项目结构说明

| 路径                            | 说明                 |
| :------------------------------ | :------------------- |
| `Designer/index.html`           | Shell 入口（登录页） |
| `Designer/index-core.html`      | Core 入口（主应用）  |
| `Designer/src/main.ts`          | Core 应用入口点      |
| `Designer/src/launcher/main.ts` | Shell 应用入口点     |
| `Designer/dist_core/`           | Core 构建输出        |
| `Server/archives/`              | ZIP 包存放目录       |
| `Server/update_version.py`      | 数据库版本更新脚本   |
