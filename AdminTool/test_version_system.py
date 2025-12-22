# -*- coding: utf-8 -*-
"""
测试版本管理系统（使用 SSH + JSON 文件）
"""
import json
import sys
import io
import paramiko

# 设置 stdout 为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_config():
    with open('deploy_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def test_connection():
    print("="*60)
    print("测试版本管理系统（SSH + JSON 文件）")
    print("="*60)
    
    config = load_config()
    
    print(f"\n📋 SSH 服务器:")
    print(f"  地址: {config['host']}")
    print(f"  端口: {config['port']}")
    print(f"  用户: {config['username']}")
    
    ssh = None
    sftp = None
    remote_file = '/var/www/app_versions/.deployments.json'
    
    try:
        print("\n🔌 连接 SSH...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=config['host'],
            port=int(config.get('port', 22)),
            username=config['username'],
            password=config['password'],
            timeout=10
        )
        print("✅ SSH 连接成功！")
        
        # 测试创建目录
        print("\n📁 检查/创建版本目录...")
        stdin, stdout, stderr = ssh.exec_command('mkdir -p /var/www/app_versions')
        stdout.channel.recv_exit_status()
        print("✅ 目录已就绪: /var/www/app_versions/")
        
        # 测试读写 JSON 文件
        print(f"\n📝 测试版本记录文件: {remote_file}")
        sftp = ssh.open_sftp()
        
        try:
            # 尝试读取现有文件
            with sftp.open(remote_file, 'r') as f:
                content = f.read().decode('utf-8')
                data = json.loads(content)
            print(f"✅ 文件已存在，读取成功")
        except IOError:
            # 文件不存在，创建新文件
            print("  文件不存在，创建新文件...")
            data = {'deployments': []}
            with sftp.open(remote_file, 'w') as f:
                f.write(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'))
            print("✅ 文件创建成功")
        
        # 显示现有记录
        print("\n📚 现有部署记录:")
        if data['deployments']:
            for i, rec in enumerate(sorted(data['deployments'], key=lambda x: x['deployed_at'], reverse=True), 1):
                status = "✅ 当前" if rec.get('is_current') else ""
                print(f"\n  [{i}] {rec['version']} {status}")
                print(f"      部署时间: {rec['deployed_at']}")
                print(f"      大小: {rec.get('file_size_mb', '-')} MB")
                print(f"      备注: {rec.get('comment') or '无'}")
        else:
            print("  (暂无记录)")
        
        # 测试写入
        print("\n✏️ 测试写入...")
        with sftp.open(remote_file, 'w') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'))
        print("✅ 写入成功")
        
        print("\n" + "="*60)
        print("✅ 测试完成！版本管理系统一切正常")
        print("="*60)
        print("\n💡 系统说明:")
        print("  - 不需要 MySQL 数据库")
        print("  - 版本信息存储在服务器的 JSON 文件中")
        print("  - 文件位置: /var/www/app_versions/.deployments.json")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n请检查:")
        print("  1. SSH 服务器是否可访问")
        print("  2. deploy_config.json 配置是否正确")
        print("  3. 服务器上是否有写入权限")
        return False
    finally:
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
    
    return True

if __name__ == "__main__":
    test_connection()

