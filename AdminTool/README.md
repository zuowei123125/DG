# DesignerCEP AdminTool 使用说明

## 📦 安装依赖

```bash
cd AdminTool
pip install -r requirements.txt
```

---

## 🚀 一、自动化部署脚本 (auto_deploy_core.py)

### 功能说明

自动化完成以下所有步骤：
1. ✅ 构建前端（Shell + Core）
2. ✅ 打包 Shell.zip（供 CEP 扩展下载）
3. ✅ 上传到服务器（SSH/SFTP）
4. ✅ 更新 MySQL 数据库版本号
5. ✅ 清除本地缓存（测试用）

### 使用方法

#### 1. 首次使用 - 配置服务器

```bash
python auto_deploy_core.py --version 1.0.6 --setup
```

会提示你输入：
- 服务器地址
- SSH 端口、用户名、密码
- 远程路径
- MySQL 地址、端口、用户名、密码、数据库名

配置会保存到 `deploy_config.json`，下次直接使用。

#### 2. 仅构建（不部署）

```bash
python auto_deploy_core.py --version 1.0.6
```

只在本地构建 Shell 和 Core，不上传到服务器。

#### 3. 构建并部署

```bash
python auto_deploy_core.py --version 1.0.6 --deploy
```

构建并自动上传到服务器：
- Shell 在线登录页 → `/static/shell/`
- Core 核心应用 → `/static/core/1.0.6/`
- Shell.zip 下载包 → `/static/downloads/shell-1.0.6.zip`

#### 4. 构建、部署并更新数据库

```bash
python auto_deploy_core.py --version 1.0.6 --deploy --update-db
```

完整流程：构建 → 上传 → 更新 MySQL 数据库版本号。

**数据库更新 SQL：**
```sql
UPDATE plugin_groups SET current_version = '1.0.6' WHERE id = 1;
```

#### 5. 其他选项

```bash
# 跳过清除缓存
python auto_deploy_core.py --version 1.0.6 --deploy --skip-clean

# 重新配置服务器
python auto_deploy_core.py --version 1.0.6 --setup
```

### 配置文件示例

`deploy_config.json`:

```json
{
  "host": "your-server.com",
  "port": "22",
  "username": "root",
  "password": "your-password",
  "remote_path": "/var/www/DesignerCEP/Server/static",
  "mysql": {
    "host": "localhost",
    "port": "3306",
    "username": "root",
    "password": "your-mysql-password",
    "database": "designer_cep",
    "table": "plugin_groups"
  }
}
```

---

## 🎨 二、图形化管理工具 (admin_gui.py)

### 功能说明

提供可视化界面管理：
- 用户组管理
- 用户权限管理
- 版本上传和分配
- **自动化部署**（新增）

### 使用方法

```bash
python admin_gui.py
```

### 主要功能

#### 1. 组与用户管理

- 创建用户组
- 修改组备注
- 查看组内用户
- 移动用户到其他组
- 修改用户权限

#### 2. 发布与上传

- 上传 ZIP 版本文件
- 查看历史版本
- 分配版本给用户组

#### 3. 自动化部署 ⭐ (新增)

完全图形化的部署流程：

**3.1 服务器配置**
- 服务器地址、SSH 端口
- 用户名、密码
- 远程路径
- 保存/加载配置
- 测试 SSH 连接

**3.2 本地构建配置**
- 项目根目录（自动检测）
- 版本号

**3.3 部署选项**
- ☑️ 部署 Shell（在线登录页）
- ☑️ 部署 Core（核心应用）
- ☑️ 打包 Shell 为 .zip
- ☑️ 构建前端（npm run build）

**3.4 一键部署**
- 点击 "🚀 开始部署" 按钮
- 实时查看部署日志
- 进度条显示当前进度
- 部署完成后显示访问地址

---

## 📖 三、部署流程说明

### 完整部署流程

```
1. 构建前端
   └─> npm run build (Designer/)
   └─> 生成 dist/Shell/ 和 dist/Designer/

2. 打包 Shell.zip
   └─> 压缩 dist/Shell/ → shell-{version}.zip

3. 连接服务器 (SSH)
   └─> 使用配置的服务器信息

4. 创建远程目录
   └─> /static/shell/
   └─> /static/core/{version}/
   └─> /static/downloads/

5. 上传文件
   └─> Shell → /static/shell/ (在线登录页)
   └─> Core  → /static/core/{version}/ (核心应用)
   └─> shell-{version}.zip → /static/downloads/ (CEP 扩展下载)

6. 更新数据库 (MySQL)
   └─> UPDATE plugin_groups SET current_version = '{version}'

7. 完成！
   └─> 显示访问地址
```

### 服务器目录结构

```
/var/www/DesignerCEP/Server/static/
├── shell/              # Shell 在线登录页
│   ├── index.html
│   └── assets/
├── downloads/          # 下载文件
│   └── shell-1.0.6.zip
└── core/               # Core 核心应用
    ├── 1.0.5/
    └── 1.0.6/
        ├── index.html
        └── assets/
```

---

## 🔧 四、常见问题

### Q1: SSH 连接失败

**A**: 检查以下几点：
1. 服务器地址和端口是否正确
2. 用户名密码是否正确
3. 服务器防火墙是否开放 SSH 端口
4. 本地网络是否正常

### Q2: MySQL 连接失败

**A**: 检查以下几点：
1. MySQL 地址和端口是否正确
2. 用户名密码是否正确
3. 数据库是否存在
4. MySQL 是否允许远程连接

### Q3: 构建失败

**A**: 
1. 检查是否安装了 Node.js 和 npm
2. 检查项目目录是否正确
3. 运行 `npm install` 安装依赖
4. 查看错误日志

### Q4: 上传速度慢

**A**:
1. 检查网络带宽
2. 考虑使用国内服务器
3. 可以先在本地构建，然后手动上传

### Q5: 如何回滚版本？

**A**:
1. 在数据库中修改版本号为旧版本
2. 或删除 `/static/core/{new_version}/` 目录

---

## 📝 五、配置文件说明

### deploy_config.json

| 字段 | 说明 | 示例 |
|------|------|------|
| `host` | 服务器地址 | `your-server.com` |
| `port` | SSH 端口 | `22` |
| `username` | SSH 用户名 | `root` |
| `password` | SSH 密码 | `your-password` |
| `remote_path` | 远程静态文件路径 | `/var/www/DesignerCEP/Server/static` |
| `mysql.host` | MySQL 地址 | `localhost` |
| `mysql.port` | MySQL 端口 | `3306` |
| `mysql.username` | MySQL 用户名 | `root` |
| `mysql.password` | MySQL 密码 | `your-mysql-password` |
| `mysql.database` | 数据库名 | `designer_cep` |
| `mysql.table` | 表名 | `plugin_groups` |

### deploy_config.txt (admin_gui.py 使用)

纯文本格式，一行一个配置：
```
host=your-server.com
port=22
user=root
password=your-password
remote_path=/var/www/DesignerCEP/Server/static
project_root=D:\main\DesignerCEP
version=1.0.6
```

---

## 🎉 六、快速开始

### 方法一：命令行部署（推荐）

```bash
# 1. 首次配置
python auto_deploy_core.py --version 1.0.6 --setup

# 2. 部署到服务器
python auto_deploy_core.py --version 1.0.6 --deploy --update-db

# 完成！
```

### 方法二：图形化部署

```bash
# 1. 启动图形界面
python admin_gui.py

# 2. 切换到"自动化部署"标签
# 3. 配置服务器信息
# 4. 点击"开始部署"按钮

# 完成！
```

---

## 📞 技术支持

如遇到问题，请检查：
1. 部署日志输出
2. 服务器 SSH 日志
3. MySQL 连接状态
4. 网络连接情况

---

**最后更新**: 2024-12-17

