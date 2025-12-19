# 使用官方 Python 轻量级镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
# 防止 Python 生成 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE=1
# 确保 Python 输出不被缓存，直接打印到终端
ENV PYTHONUNBUFFERED=1

# 安装系统依赖 (如果需要)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p archives

# 暴露端口
EXPOSE 8000

# 启动命令
# 生产环境推荐使用 gunicorn 管理 uvicorn workers，或者直接用 uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
