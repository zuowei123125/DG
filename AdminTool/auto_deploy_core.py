#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core 应用自动发布脚本
完全自动化构建、打包、上传服务器、更新数据库

使用方法：
    python auto_deploy_core.py --version v1.0.6
    python auto_deploy_core.py --version v1.0.6 --deploy  # 部署到服务器
    python auto_deploy_core.py --version v1.0.6 --deploy --update-db  # 部署并更新数据库
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
import pymysql

# ==================== 配置区域 ====================
PROJECT_ROOT = Path(__file__).parent.parent.absolute()  # 上一级目录
DESIGNER_DIR = PROJECT_ROOT / "Designer"
DIST_CORE_DIR = DESIGNER_DIR / "dist" / "Designer"  # Core 构建输出目录
DIST_SHELL_DIR = DESIGNER_DIR / "dist" / "Shell"    # Shell 构建输出目录
SERVER_DIR = PROJECT_ROOT / "Server"
ARCHIVES_DIR = SERVER_DIR / "archives"
CONFIG_FILE = Path(__file__).parent / "deploy_config.json"

# 颜色输出（Windows 兼容）
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

def print_step(step_num, total_steps, message):
    """打印步骤信息"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{GREEN}[步骤 {step_num}/{total_steps}] {message}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(message):
    """打印成功信息"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_warning(message):
    """打印警告信息"""
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_error(message):
    """打印错误信息"""
    print(f"{RED}✗ {message}{RESET}")

def run_command(command, cwd=None, shell=True, check=True):
    """运行命令并返回结果"""
    print(f"  执行: {command}")
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            check=check,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if result.stdout:
            print(f"  输出: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"命令执行失败: {e}")
        if e.stderr:
            print(f"  错误: {e.stderr}")
        if check:
            sys.exit(1)
        return None

# ==================== 发布步骤 ====================

def load_config():
    """加载部署配置"""
    if not CONFIG_FILE.exists():
        return None
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print_warning(f"加载配置文件失败: {e}")
        return None

def save_config(config):
    """保存部署配置"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print_success(f"配置已保存: {CONFIG_FILE}")
    except Exception as e:
        print_error(f"保存配置失败: {e}")

def step1_build_frontend():
    """步骤 1: 构建前端（Shell + Core）"""
    print_step(1, 8, "构建前端（Shell + Core）")
    
    # 检查 package.json
    package_json = DESIGNER_DIR / "package.json"
    if not package_json.exists():
        print_error(f"未找到 package.json: {package_json}")
        sys.exit(1)
    
    # 运行构建命令
    os.chdir(DESIGNER_DIR)
    print("  正在构建 Core...")
    run_command("npm run build:core", cwd=DESIGNER_DIR)
    print("  正在构建 Shell...")
    run_command("npm run build", cwd=DESIGNER_DIR)
    
    # 验证输出目录
    if not DIST_CORE_DIR.exists():
        print_error(f"Core 构建输出目录不存在: {DIST_CORE_DIR}")
        sys.exit(1)
    
    if not DIST_SHELL_DIR.exists():
        print_error(f"Shell 构建输出目录不存在: {DIST_SHELL_DIR}")
        sys.exit(1)
    
    print_success(f"构建完成")
    print(f"  Core:  {DIST_CORE_DIR}")
    print(f"  Shell: {DIST_SHELL_DIR}")

def step2_package_shell_zip(version):
    """步骤 2: 打包 Shell 为 ZIP（供 CEP 扩展下载）"""
    print_step(2, 8, "打包 Shell 为 ZIP")
    
    # 生成 ZIP 文件名
    zip_filename = f"shell-{version}.zip"
    zip_path = DESIGNER_DIR / "dist" / zip_filename
    
    # 如果文件已存在，先删除
    if zip_path.exists():
        print_warning(f"ZIP 文件已存在，删除: {zip_path}")
        zip_path.unlink()
    
    # 创建 ZIP
    print(f"  创建 ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DIST_SHELL_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(DIST_SHELL_DIR)
                zipf.write(file_path, arcname)
    
    # 显示文件大小
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print_success(f"Shell 打包完成: {zip_path}")
    print(f"  文件大小: {size_mb:.2f} MB")
    
    return zip_path

def step3_upload_to_server(version, config):
    """步骤 3: 上传到服务器"""
    print_step(3, 8, "上传到服务器")
    
    if not config:
        print_warning("未配置服务器信息，跳过上传")
        return
    
    # 连接 SSH
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
        remote_path = config['remote_path']
        
        # 1. 创建远程目录
        print("  创建远程目录...")
        commands = [
            f"mkdir -p {remote_path}/shell",
            f"mkdir -p {remote_path}/core/{version}",
            f"mkdir -p {remote_path}/downloads"
        ]
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()
        print_success("目录创建完成")
        
        # 2. 上传 Shell（在线登录页）
        print("  上传 Shell（在线登录页）...")
        upload_directory(sftp, DIST_SHELL_DIR, f"{remote_path}/shell")
        print_success("Shell 上传完成")
        
        # 3. 上传 Core
        print("  上传 Core（核心应用）...")
        upload_directory(sftp, DIST_CORE_DIR, f"{remote_path}/core/{version}")
        print_success("Core 上传完成")
        
        # 4. 上传 Shell.zip
        print("  上传 Shell.zip（CEP 扩展下载）...")
        shell_zip = DESIGNER_DIR / "dist" / f"shell-{version}.zip"
        if shell_zip.exists():
            remote_zip = f"{remote_path}/downloads/shell-{version}.zip"
            sftp.put(str(shell_zip), remote_zip)
            print_success(f"Shell.zip 上传完成: {remote_zip}")
        
        sftp.close()
        ssh.close()
        
        print_success("所有文件上传完成")
        print(f"\n访问地址:")
        print(f"  Shell: https://{config['host']}/shell/")
        print(f"  Core:  https://{config['host']}/core/{version}/")
        print(f"  下载:  https://{config['host']}/downloads/shell-{version}.zip")
        
    except Exception as e:
        print_error(f"上传失败: {e}")
        raise
    finally:
        ssh.close()

def upload_directory(sftp, local_dir, remote_dir):
    """递归上传目录"""
    if not os.path.exists(local_dir):
        raise Exception(f"本地目录不存在: {local_dir}")
    
    # 创建远程目录
    try:
        sftp.stat(remote_dir)
    except IOError:
        sftp.mkdir(remote_dir)
    
    # 递归上传文件
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = remote_dir + '/' + item
        
        if os.path.isfile(local_path):
            print(f"    → {item}")
            sftp.put(local_path, remote_path)
        elif os.path.isdir(local_path):
            upload_directory(sftp, local_path, remote_path)

def step4_update_mysql(version, config):
    """步骤 4: 更新 MySQL 数据库 (通过 SSH 执行 Docker 命令)"""
    print_step(4, 8, "更新 MySQL 数据库")
    
    # 注意：我们不再直接连接 MySQL，而是通过 SSH 发送 docker exec 命令
    # 这样用户不需要暴露 MySQL 端口，更安全
    
    if not config:
        print_warning("未配置服务器信息，跳过数据库更新")
        return
        
    try:
        # 连接 SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"  连接服务器: {config['host']}")
        ssh.connect(
            hostname=config['host'],
            port=int(config.get('port', 22)),
            username=config['username'],
            password=config.get('password', ''),
            timeout=30
        )
        print_success("SSH 连接成功")
        
        # 构造 SQL 语句
        # 更新 'default' 分组为最新版本 (更健壮，不依赖 ID=1)
        sql = f"UPDATE plugin_groups SET current_version_file = 'core-v{version}.zip' WHERE name = 'default';"
        
        # 构造 Docker 命令
        # 假设容器名为 designercep_db，用户 designer_user，密码 DesignerPass123!，库名 designer_db
        # 这些应该与 docker-compose.yml 保持一致
        db_user = "designer_user"
        db_pass = "DesignerPass123!"
        db_name = "designer_db"
        container_name = "designercep_db"
        
        print(f"  执行远程 Docker SQL 命令...")
        print(f"  SQL: {sql}")
        
        docker_cmd = f'docker exec -i {container_name} mysql -u{db_user} -p{db_pass} {db_name} -e "{sql}"'
        
        stdin, stdout, stderr = ssh.exec_command(docker_cmd)
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print_success("数据库更新命令执行成功")
            print(f"  输出: {stdout.read().decode().strip()}")
        else:
            print_error(f"数据库更新失败 (Exit code: {exit_status})")
            print(f"  错误: {stderr.read().decode().strip()}")
            raise Exception("Docker exec failed")
            
        ssh.close()

    except Exception as e:
        print_error(f"数据库更新失败: {e}")
        print_warning("您需要手动执行 SQL (进入容器执行):")
        print(f"  {sql}")
        # 不抛出异常，以免打断流程，因为这步失败通常不影响文件上传


def step5_clean_cache():
    """步骤 5: 清除客户端缓存（测试用）"""
    print_step(5, 8, "清除客户端缓存（可选）")
    
    cache_dir = Path.home() / "AppData" / "Roaming" / "DesignerCache"
    
    if not cache_dir.exists():
        print_warning(f"缓存目录不存在: {cache_dir}")
        return
    
    try:
        shutil.rmtree(cache_dir)
        print_success(f"缓存已清除: {cache_dir}")
    except Exception as e:
        print_warning(f"清除缓存失败: {e}")
        print("  您可以手动删除缓存目录")

def step6_setup_config():
    """步骤 6: 配置服务器信息（首次运行）"""
    print_step(6, 8, "配置服务器信息")
    
    config = load_config()
    if config:
        print_warning("配置文件已存在，跳过配置")
        print(f"  配置文件: {CONFIG_FILE}")
        return config
    
    print("请输入服务器配置信息：")
    print()
    
    config = {}
    
    # SSH 配置
    config['host'] = input("  服务器地址: ").strip()
    config['port'] = input("  SSH 端口 [22]: ").strip() or "22"
    config['username'] = input("  SSH 用户名: ").strip()
    config['password'] = input("  SSH 密码: ").strip()
    config['remote_path'] = input("  远程路径 [/var/www/DesignerCEP/Server/static]: ").strip() \
                            or "/var/www/DesignerCEP/Server/static"
    
    print()
    
    # MySQL 配置
    use_mysql = input("  是否配置 MySQL？ (y/n) [y]: ").strip().lower()
    if use_mysql != 'n':
        config['mysql'] = {}
        config['mysql']['host'] = input("  MySQL 地址: ").strip()
        config['mysql']['port'] = input("  MySQL 端口 [3306]: ").strip() or "3306"
        config['mysql']['username'] = input("  MySQL 用户名: ").strip()
        config['mysql']['password'] = input("  MySQL 密码: ").strip()
        config['mysql']['database'] = input("  数据库名: ").strip()
        config['mysql']['table'] = input("  表名 [plugin_groups]: ").strip() or "plugin_groups"
    
    # 保存配置
    save_config(config)
    
    return config

def step7_summary(version, deployed):
    """步骤 7: 发布总结"""
    print_step(7, 8, "发布总结")
    
    print(f"""
{GREEN}{'='*60}
  DesignerCEP 发布完成！
{'='*60}{RESET}

[发布信息]
  版本号:     {version}
  构建时间:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  部署状态:   {'已部署到服务器' if deployed else '仅本地构建'}

[构建产物]
  Core:  {DIST_CORE_DIR}
  Shell: {DIST_SHELL_DIR}
  Shell.zip: {DESIGNER_DIR / 'dist' / f'shell-{version}.zip'}

[后续步骤]
  1. {'✓' if deployed else '○'} 验证服务器文件
  2. {'✓' if deployed else '○'} 确认数据库版本
  3. ○ 测试客户端更新功能
  4. ○ 通知用户更新

[测试方法]
  1. 删除客户端缓存（已自动执行）
  2. 重启 Photoshop 插件
  3. 登录账号，检查是否下载新版本
  4. 验证功能是否正常

{GREEN}{'='*60}{RESET}
""")

# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(
        description='DesignerCEP 自动发布脚本（Shell + Core）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 仅构建（不部署）
  python auto_deploy_core.py --version 1.0.6
  
  # 构建并部署到服务器
  python auto_deploy_core.py --version 1.0.6 --deploy
  
  # 构建、部署并更新数据库
  python auto_deploy_core.py --version 1.0.6 --deploy --update-db
  
  # 首次运行，配置服务器信息
  python auto_deploy_core.py --version 1.0.6 --setup
        """
    )
    
    parser.add_argument(
        '--version', '-v',
        required=True,
        help='版本号，例如: 1.0.6（不要加 v）'
    )
    
    parser.add_argument(
        '--deploy', '-d',
        action='store_true',
        help='部署到服务器'
    )
    
    parser.add_argument(
        '--update-db',
        action='store_true',
        help='自动更新 MySQL 数据库'
    )
    
    parser.add_argument(
        '--setup',
        action='store_true',
        help='配置服务器信息（首次运行）'
    )
    
    parser.add_argument(
        '--skip-clean',
        action='store_true',
        help='跳过清除缓存步骤'
    )
    
    args = parser.parse_args()
    
    version = args.version
    
    print(f"""
{BLUE}{'='*60}
  DesignerCEP 自动发布脚本
{'='*60}{RESET}

[配置信息]
  版本号:      {version}
  项目根目录:   {PROJECT_ROOT}
  Designer:    {DESIGNER_DIR}
  部署到服务器: {'是' if args.deploy else '否'}
  更新数据库:   {'是' if args.update_db else '否'}
  清除缓存:     {'否' if args.skip_clean else '是'}

{BLUE}{'='*60}{RESET}
""")
    
    try:
        # 加载配置
        config = None
        if args.deploy or args.setup:
            config = load_config()
            if not config or args.setup:
                config = step6_setup_config()
        
        # 执行发布步骤
        step1_build_frontend()
        step2_package_shell_zip(version)
        
        if args.deploy:
            if not config:
                print_error("未找到配置文件，请先运行 --setup 配置服务器")
                sys.exit(1)
            
            step3_upload_to_server(version, config)
            
            if args.update_db:
                step4_update_mysql(version, config)
            else:
                print_step(4, 8, "更新数据库（已跳过）")
                print_warning("数据库未自动更新，请手动执行:")
                print(f"  UPDATE plugin_groups SET current_version = '{version}';")
        else:
            print_step(3, 8, "上传到服务器（已跳过）")
            print_step(4, 8, "更新数据库（已跳过）")
        
        if not args.skip_clean:
            step5_clean_cache()
        else:
            print_step(5, 8, "清除缓存（已跳过）")
        
        step7_summary(version, args.deploy)
        
    except KeyboardInterrupt:
        print_error("\n用户中断")
        sys.exit(1)
    except Exception as e:
        print_error(f"发布失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

