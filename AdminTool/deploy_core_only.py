#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core 快速发布脚本
仅执行：构建 Core -> 上传 Core -> 更新数据库
跳过 Shell 的构建和上传
"""

import os
import sys
import shutil
import subprocess
import argparse
import zipfile
import json
from pathlib import Path
from datetime import datetime
import paramiko

# ==================== 配置区域 ====================
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DESIGNER_DIR = PROJECT_ROOT / "Designer"
DIST_CORE_DIR = DESIGNER_DIR / "dist_core"  # Core 构建输出目录
CONFIG_FILE = Path(__file__).parent / "deploy_config.json"

# 颜色输出
try:
    import colorama
    colorama.init()
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
except ImportError:
    GREEN = YELLOW = RED = BLUE = RESET = ''

# ==================== 工具函数 ====================

def print_step(message):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{GREEN}{message}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def run_command(command, cwd=None):
    print(f"  执行: {command}")
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=True, 
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if result.stdout:
            print(f"  输出: {result.stdout.strip()[:200]}...") # 只打印前200字符
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"命令执行失败: {e}")
        if e.stderr:
            print(f"  错误: {e.stderr}")
        sys.exit(1)

def load_config():
    if not CONFIG_FILE.exists():
        print_error("未找到配置文件 deploy_config.json")
        sys.exit(1)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# ==================== 核心步骤 ====================

def step1_build_core():
    print_step("步骤 1: 构建 Core")
    
    # 检查目录
    if not DESIGNER_DIR.exists():
        print_error(f"Designer 目录不存在: {DESIGNER_DIR}")
        sys.exit(1)
    
    # 执行构建
    print("  正在构建 Core (npm run build:core)...")
    os.chdir(DESIGNER_DIR)
    run_command("npm run build:core", cwd=DESIGNER_DIR)
    
    # 验证
    if not DIST_CORE_DIR.exists():
        print_error(f"Core 构建失败，输出目录不存在: {DIST_CORE_DIR}")
        sys.exit(1)
        
    print_success("Core 构建完成")

def step2_upload_core(version, config):
    print_step("步骤 2: 上传 Core 到服务器")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"  连接服务器: {config['host']}")
        ssh.connect(
            hostname=config['host'],
            port=int(config.get('port', 22)),
            username=config['username'],
            password=config.get('password', ''),
            timeout=30
        )
        print_success("SSH 连接成功")
        
        sftp = ssh.open_sftp()
        remote_base = config['remote_path']
        remote_core_dir = f"{remote_base}/core/{version}"
        
        # 创建远程目录
        print(f"  创建远程目录: {remote_core_dir}")
        ssh.exec_command(f"mkdir -p {remote_core_dir}")
        
        # 递归上传
        print("  开始上传文件...")
        upload_count = 0
        for root, dirs, files in os.walk(DIST_CORE_DIR):
            relative_root = Path(root).relative_to(DIST_CORE_DIR)
            remote_root = f"{remote_core_dir}/{relative_root}".replace("\\", "/").rstrip("/")
            if str(relative_root) == ".":
                remote_root = remote_core_dir
            
            # 确保子目录存在
            try:
                sftp.stat(remote_root)
            except IOError:
                sftp.mkdir(remote_root)
                
            for file in files:
                local_file = Path(root) / file
                remote_file = f"{remote_root}/{file}"
                sftp.put(str(local_file), remote_file)
                upload_count += 1
                if upload_count % 10 == 0:
                    print(f"    已上传 {upload_count} 个文件...", end='\r')
                    
        print(f"\n  共上传 {upload_count} 个文件")
        print_success("Core 上传完成")
        
        sftp.close()
        ssh.close()
        
    except Exception as e:
        print_error(f"上传失败: {e}")
        raise

def step3_update_db(version, config):
    print_step("步骤 3: 更新数据库")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            hostname=config['host'],
            port=int(config.get('port', 22)),
            username=config['username'],
            password=config.get('password', ''),
            timeout=30
        )
        
        # 构造 SQL
        sql = f"UPDATE plugin_groups SET current_version_file = 'core-v{version}.zip' WHERE name = 'default';"
        
        # 数据库配置
        db_conf = config.get('mysql', {})
        db_user = db_conf.get('username', 'designer_user')
        db_pass = db_conf.get('password', 'DesignerPass123!')
        db_name = db_conf.get('database', 'designer_db')
        container_name = "designercep_db"
        
        print(f"  更新 'default' 分组版本为: core-v{version}.zip")
        docker_cmd = f'docker exec -i {container_name} mysql -u{db_user} -p{db_pass} {db_name} -e "{sql}"'
        
        stdin, stdout, stderr = ssh.exec_command(docker_cmd)
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print_success("数据库更新成功")
        else:
            print_error(f"数据库更新失败: {stderr.read().decode().strip()}")
            raise Exception("DB Update Failed")
            
        ssh.close()
        
    except Exception as e:
        print_error(f"数据库操作失败: {e}")
        raise

def step4_clean_cache():
    print_step("步骤 4: 清除本地缓存")
    cache_dir = Path.home() / "AppData" / "Roaming" / "DesignerCache"
    if cache_dir.exists():
        try:
            shutil.rmtree(cache_dir)
            print_success(f"已清除: {cache_dir}")
        except Exception as e:
            print_error(f"清除失败: {e}")
    else:
        print("  无需清除")

# ==================== 主入口 ====================

def main():
    parser = argparse.ArgumentParser(description='Core 快速发布脚本')
    parser.add_argument('--version', '-v', required=True, help='版本号 (如 1.0.7)')
    args = parser.parse_args()
    
    version = args.version
    
    print(f"{BLUE}开始发布 Core - 版本: {version}{RESET}")
    
    try:
        config = load_config()
        
        step1_build_core()
        step2_upload_core(version, config)
        step3_update_db(version, config)
        step4_clean_cache()
        
        print_step("🎉 发布全部完成！")
        print(f"  版本: {version}")
        print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print_error(f"\n发布过程中止: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
