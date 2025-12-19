# 后端部署 Shell 完整指南

## 🎯 目标

让服务器提供 Shell 登录页面，解决退出时无法跳转回登录页的问题。

---

## 📋 需要做的事情

### ✅ 后端代码已修改完成

`Server/app/main.py` 已经修改好了，包含：
1. 挂载 Shell 目录到 `/shell/` 路径
2. 根路径重定向到 Shell 登录页

---

## 📦 需要上传的文件

### 1. 构建 Shell（在前端项目中执行）

```bash
cd Designer
npm run build:shell
```

**生成位置：** `Designer/dist/`

**生成内容：**
```
Designer/dist/
├── index.html          ← Shell 入口文件
├── assets/
│   ├── index-xxx.js    ← Shell 的 JS
│   ├── index-xxx.css   ← Shell 的 CSS
│   └── ...
├── node_modules/       ← CEP 需要的依赖
└── ...
```

---

### 2. 上传 Shell 到服务器

有两种方式：

#### 方式 1：直接复制到服务器项目（推荐）⭐

```bash
# 在项目根目录执行
# 把 Designer/dist/ 整个目录复制到服务器项目下

# Windows PowerShell
Copy-Item -Path "Designer\dist" -Destination "Server\Designer\dist" -Recurse -Force

# Linux/Mac
cp -r Designer/dist Server/Designer/dist
```

最终服务器目录结构：
```
Server/
├── app/
│   ├── main.py         ← 已修改
│   └── ...
├── Designer/           ← 新增！
│   └── dist/           ← Shell 文件
│       ├── index.html
│       └── ...
└── ...
```

#### 方式 2：使用软链接（开发环境）

```bash
# Windows（管理员权限）
cd Server
mklink /D Designer ..\Designer

# Linux/Mac
cd Server
ln -s ../Designer Designer
```

---

## 🔧 后端代码说明

### main.py 的修改（已完成）

```python
# 1. 导入 Path
from pathlib import Path

# 2. 挂载 Shell 目录
shell_dir = Path(__file__).parent.parent / "Designer"
if shell_dir.exists():
    app.mount("/shell", StaticFiles(directory=str(shell_dir), html=True), name="shell")
    print(f"✓ Shell 已挂载: {shell_dir}")
else:
    print(f"⚠️ Shell 目录不存在: {shell_dir}")
    print("  请先运行: cd Designer && npm run build:shell")

# 3. 根路径重定向到 Shell
@app.get("/")
def read_root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/shell/index.html")
```

---

## 🚀 部署步骤

### Step 1: 构建 Shell

```bash
# 在前端项目目录
cd D:\main\DesignerCEP\Designer
npm run build:shell
```

**检查输出：**
- ✅ `dist/index.html` 文件存在
- ✅ `dist/assets/` 目录存在

---

### Step 2: 复制 Shell 到服务器

**方法 A：在本地复制（推荐）**

```bash
# 在项目根目录
cd D:\main\DesignerCEP

# 创建目标目录
mkdir Server\Designer -Force

# 复制文件
Copy-Item -Path "Designer\dist" -Destination "Server\Designer\dist" -Recurse -Force
```

**方法 B：在服务器上从 Git 拉取（如果用了 Git）**

```bash
# 在服务器上
cd /path/to/DesignerCEP
git pull
cd Designer
npm run build:shell
```

---

### Step 3: 验证文件结构

```bash
cd Server
dir Designer\dist\index.html  # Windows
# 或
ls Designer/dist/index.html   # Linux
```

**应该看到：**
```
D:\main\DesignerCEP\Server\Designer\dist\index.html
```

---

### Step 4: 重启后端服务器

```bash
cd Server
python -m uvicorn app.main:app --reload
```

**启动日志应该显示：**
```
✓ Shell 已挂载: D:\main\DesignerCEP\Server\Designer\dist
INFO:     Uvicorn running on http://127.0.0.1:8000
```

如果显示：
```
⚠️ Shell 目录不存在: ...
  请先运行: cd Designer && npm run build:shell
```

说明文件没有正确复制，回到 Step 2。

---

### Step 5: 测试访问

#### 测试 1：根路径重定向

```bash
# 在浏览器访问
http://127.0.0.1:8000/
```

**预期：** 自动跳转到 `http://127.0.0.1:8000/shell/index.html` 并显示登录页

#### 测试 2：直接访问 Shell

```bash
http://127.0.0.1:8000/shell/
```

**预期：** 显示登录页面

#### 测试 3：登录并退出

1. 在 Shell 登录页输入账号密码
2. 登录成功 → 跳转到 Core
3. 在 Core 点击退出
4. **预期：** 跳转回 Shell 登录页 ✅

---

## 📁 完整目录结构

```
D:\main\DesignerCEP\
├── Designer/
│   ├── src/
│   │   ├── launcher/           ← Shell 源代码
│   │   │   ├── view/
│   │   │   │   └── Login.vue   ← 登录页面源码
│   │   │   └── utils/
│   │   │       └── updater.ts
│   │   └── view/
│   │       └── Home.vue        ← Core 页面
│   │
│   └── dist/                   ← 构建后的 Shell
│       ├── index.html          ← 需要复制到服务器
│       └── assets/
│
└── Server/
    ├── app/
    │   └── main.py             ← 已修改
    │
    ├── Designer/               ← 新增目录
    │   └── dist/               ← 从 Designer/dist/ 复制过来
    │       ├── index.html      ← Shell 登录页
    │       └── assets/
    │
    └── archives/               ← Core 下载包
        └── core-v1.2.4.zip
```

---

## 🔍 访问路径说明

| URL | 作用 | 文件位置 |
|-----|------|---------|
| `http://127.0.0.1:8000/` | 根路径，重定向到 Shell | - |
| `http://127.0.0.1:8000/shell/` | Shell 登录页 | `Server/Designer/dist/index.html` |
| `http://127.0.0.1:8000/core/v1.2.4/` | Core 业务页 | `C:/Users/.../DesignerCache/v1.2.4/` |
| `http://127.0.0.1:8000/download/` | 下载 Core 包 | `Server/archives/` |

---

## ⚠️ 常见问题

### 问题 1：启动后显示 "Shell 目录不存在"

**原因：** `Server/Designer/dist/` 目录不存在

**解决：**
```bash
# 检查目录
cd D:\main\DesignerCEP\Server
dir Designer\dist

# 如果不存在，重新复制
cd ..
Copy-Item -Path "Designer\dist" -Destination "Server\Designer\dist" -Recurse -Force
```

---

### 问题 2：访问 `/shell/` 显示 404

**原因：** 文件没有正确挂载

**解决：**
1. 检查 `Server/Designer/dist/index.html` 是否存在
2. 检查后端启动日志是否显示 "✓ Shell 已挂载"
3. 重启后端服务器

---

### 问题 3：访问 `/` 不重定向

**原因：** `main.py` 中的重定向代码没有生效

**解决：**
1. 确认 `main.py` 中有重定向代码：
```python
@app.get("/")
def read_root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/shell/index.html")
```
2. 重启后端服务器

---

### 问题 4：Shell 页面加载失败

**原因：** 资源文件路径问题

**解决：**
1. 检查 `dist/index.html` 中的资源引用是否正确
2. 确认 `assets/` 目录完整复制
3. 清除浏览器缓存后重试

---

## 🔄 更新流程

当 Shell 代码有更新时：

```bash
# 1. 重新构建 Shell
cd Designer
npm run build:shell

# 2. 复制到服务器
cd ..
Copy-Item -Path "Designer\dist" -Destination "Server\Designer\dist" -Recurse -Force

# 3. 重启后端（如果使用 --reload 则自动重启）
# 或手动重启
```

---

## ✅ 部署检查清单

部署完成后，检查以下项：

- [ ] `Server/Designer/dist/index.html` 文件存在
- [ ] 后端启动日志显示 "✓ Shell 已挂载"
- [ ] 访问 `http://127.0.0.1:8000/` 自动跳转到 Shell
- [ ] 访问 `http://127.0.0.1:8000/shell/` 显示登录页
- [ ] Shell 页面可以正常登录
- [ ] 登录后跳转到 Core
- [ ] Core 退出后跳转回 Shell 登录页 ✅

---

## 📝 快速命令汇总

```bash
# 1. 构建 Shell
cd D:\main\DesignerCEP\Designer
npm run build:shell

# 2. 复制到服务器
cd ..
Copy-Item -Path "Designer\dist" -Destination "Server\Designer\dist" -Recurse -Force

# 3. 重启后端
cd Server
python -m uvicorn app.main:app --reload

# 4. 测试访问
# 浏览器打开: http://127.0.0.1:8000/
```

---

## 🎉 完成

部署完成后：
- ✅ 用户登录后使用 Core
- ✅ 退出时自动跳转回 Shell 登录页
- ✅ 不再显示 `{"message":"Welcome to DesignerCEP Backend"}`

**现在退出流程完美了！** 🎊

