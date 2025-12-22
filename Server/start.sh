#!/bin/bash

# 确保在脚本出错时退出
set -e

echo "🚀 Starting DesignerCEP Backend..."

# 0. 数据库迁移 (暂时禁用，避免与手动建表冲突)
echo "🔄 Skipping Alembic Migrations (Manual SQL setup assumed)..."
# if [ -z "$(ls -A alembic/versions 2>/dev/null)" ]; then
#     echo "🆕 Initializing database migrations..."
#     alembic revision --autogenerate -m "Initial migration"
# fi
# alembic upgrade head

# 1. 强制重建数据库 (测试环境专用 - 可选)
# 用户之前要求每次启动都重新初始化数据库，如果 Alembic 工作正常，可以考虑用 downgrade base 再 upgrade head
# 但为了保持现有行为，我们先保留 recreate_db，或者根据用户意愿调整。
# 既然有了 Alembic，recreate_db 可能就太暴力了。
# 如果用户坚持每次都要“新”环境，可以：
# alembic downgrade base
# alembic upgrade head

# echo "💥 Force Recreating Database (Test Mode)..."
# python -m app.recreate_db

# 2. 创建默认管理员用户 (如果不存在)
# 既然已经通过 SQL 脚本初始化了管理员，这里可以注释掉，避免重复创建或报错
# echo "👤 Ensuring admin user exists..."
# python create_user.py admin password123 admin@example.com

# 3. 启动应用
echo "🌐 Starting FastAPI server..."
# 使用 uvicorn 启动，host 0.0.0.0 允许外部访问，端口 8000
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
