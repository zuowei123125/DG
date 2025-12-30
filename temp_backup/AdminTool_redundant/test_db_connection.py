# -*- coding: utf-8 -*-
"""
测试数据库连接和 app_deployments 表（通过 SSH 隧道）
"""
import json
import pymysql
from datetime import datetime
import sys
import io
from sshtunnel import SSHTunnelForwarder

# 设置 stdout 为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_config():
    with open('deploy_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_connection():
    print("="*60)
    print("测试 MySQL 数据库连接（通过 SSH 隧道）")
    print("="*60)
    
    config = load_config()
    mysql_config = config['mysql']
    
    print(f"\n📋 SSH 服务器:")
    print(f"  地址: {config['host']}")
    print(f"  端口: {config['port']}")
    print(f"  用户: {config['username']}")
    
    print(f"\n📋 MySQL 配置:")
    print(f"  主机: {mysql_config['host']}")
    print(f"  端口: {mysql_config['port']}")
    print(f"  用户: {mysql_config['username']}")
    print(f"  数据库: {mysql_config['database']}")
    
    tunnel = None
    
    try:
        print("\n🔌 创建 SSH 隧道...")
        tunnel = SSHTunnelForwarder(
            (config['host'], int(config.get('port', 22))),
            ssh_username=config['username'],
            ssh_password=config['password'],
            remote_bind_address=('127.0.0.1', int(mysql_config.get('port', 3306)))
        )
        tunnel.start()
        print(f"✅ SSH 隧道已建立，本地端口: {tunnel.local_bind_port}")
        
        print("\n🔌 连接 MySQL...")
        conn = pymysql.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user=mysql_config['username'],
            password=mysql_config['password'],
            database=mysql_config['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ MySQL 连接成功！")
        
        # 测试创建表
        print("\n📝 创建/检查 app_deployments 表...")
        with conn.cursor() as cursor:
            sql = """
            CREATE TABLE IF NOT EXISTS app_deployments (
                id INT PRIMARY KEY AUTO_INCREMENT,
                version VARCHAR(50) UNIQUE NOT NULL,
                deployed_at DATETIME NOT NULL,
                is_current BOOLEAN DEFAULT FALSE,
                file_size_mb DECIMAL(10, 2),
                comment VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(sql)
            conn.commit()
            print("✅ 表已就绪")
        
        # 查看表结构
        print("\n📊 表结构:")
        with conn.cursor() as cursor:
            cursor.execute("DESCRIBE app_deployments")
            for row in cursor.fetchall():
                print(f"  {row['Field']}: {row['Type']} {'(主键)' if row['Key'] == 'PRI' else ''}")
        
        # 查看现有数据
        print("\n📚 现有部署记录:")
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM app_deployments ORDER BY deployed_at DESC")
            records = cursor.fetchall()
            
            if records:
                for i, rec in enumerate(records, 1):
                    status = "✅ 当前" if rec['is_current'] else ""
                    print(f"\n  [{i}] {rec['version']} {status}")
                    print(f"      部署时间: {rec['deployed_at']}")
                    print(f"      大小: {rec['file_size_mb']} MB")
                    print(f"      备注: {rec['comment'] or '无'}")
            else:
                print("  (暂无记录)")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ 测试完成！数据库一切正常")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请检查:")
        print("  1. SSH 服务器是否可访问")
        print("  2. deploy_config.json 配置是否正确")
        print("  3. 服务器上 MySQL 服务是否运行")
        print("  4. 数据库用户权限是否足够")
        return False
    finally:
        if tunnel:
            tunnel.stop()
            print("\n🔌 SSH 隧道已关闭")
    
    return True

if __name__ == "__main__":
    test_connection()
