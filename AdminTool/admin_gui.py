import sys
import os
import requests
import subprocess
import paramiko
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTabWidget, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QFileDialog, QGroupBox,
                             QComboBox, QDialog, QFormLayout, QDialogButtonBox,
                             QSplitter, QFrame, QListWidget, QListWidgetItem,
                             QInputDialog, QGridLayout, QTextEdit, QCheckBox,
                             QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Configuration
DEFAULT_API_URL = " https://backend.aidg168.uk/api/v1"
DEFAULT_ADMIN_TOKEN = "admin-secret-token"

import shutil
import zipfile
from datetime import datetime

class ApiClient:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip("/")
        self.token = token
        
    def get_headers(self):
        return {"x-admin-token": self.token}

    def list_groups(self):
        try:
            resp = requests.get(f"{self.base_url}/admin/groups", headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"获取组列表失败: {str(e)}")

    def create_group(self, name, comment):
        try:
            payload = {"name": name, "comment": comment}
            resp = requests.post(f"{self.base_url}/admin/groups", json=payload, headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"创建组失败: {str(e)}")

    def upload_version(self, file_path):
        try:
            filename = os.path.basename(file_path)
            files = {'file': (filename, open(file_path, 'rb'))}
            data = {'token': self.token}
            resp = requests.post(f"{self.base_url}/admin/upload_version", files=files, data=data)
            resp.raise_for_status()
            return resp.json().get("filename")
        except Exception as e:
            raise Exception(f"上传失败: {str(e)}")

    def list_archives(self):
        try:
            resp = requests.get(f"{self.base_url}/admin/archives", headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"获取归档列表失败: {str(e)}")

    def update_group_version(self, group_id, filename):
        try:
            payload = {"current_version_file": filename}
            resp = requests.put(f"{self.base_url}/admin/groups/{group_id}", json=payload, headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"更新组版本失败: {str(e)}")
    
    def update_group_comment(self, group_id, comment):
        try:
            payload = {"comment": comment}
            resp = requests.put(f"{self.base_url}/admin/groups/{group_id}", json=payload, headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"更新组备注失败: {str(e)}")

    def list_users(self):
        try:
            resp = requests.get(f"{self.base_url}/admin/users", headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"获取用户列表失败: {str(e)}")

    def update_user_group(self, user_id, group_id):
        try:
            # group_id is query param in backend
            resp = requests.put(f"{self.base_url}/admin/users/{user_id}/group?group_id={group_id}", headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"更新用户组失败: {str(e)}")
            
    def update_user_permissions(self, user_id, permissions):
        try:
            data = {"permissions": permissions}
            resp = requests.put(f"{self.base_url}/admin/users/{user_id}/permissions", data=data, headers=self.get_headers())
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise Exception(f"更新用户权限失败: {str(e)}")

class CreateGroupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("创建新组")
        self.layout = QFormLayout(self)
        
        self.name_edit = QLineEdit()
        self.comment_edit = QLineEdit()
        
        self.layout.addRow("组名称:", self.name_edit)
        self.layout.addRow("备注:", self.comment_edit)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)
        
    def get_data(self):
        return self.name_edit.text(), self.comment_edit.text()

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DesignerCEP 管理工具")
        self.resize(1000, 700)
        
        self.api_client = None
        self.groups_data = [] # Cache groups
        self.users_data = []  # Cache users
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 1. Connection Bar
        conn_group = QGroupBox("服务器连接")
        conn_layout = QHBoxLayout()
        
        self.url_edit = QLineEdit(DEFAULT_API_URL)
        self.token_edit = QLineEdit(DEFAULT_ADMIN_TOKEN)
        self.token_edit.setEchoMode(QLineEdit.Password)
        self.connect_btn = QPushButton("连接 / 刷新")
        self.connect_btn.clicked.connect(self.init_connection)
        
        conn_layout.addWidget(QLabel("API 地址:"))
        conn_layout.addWidget(self.url_edit, 2)
        conn_layout.addWidget(QLabel("Token:"))
        conn_layout.addWidget(self.token_edit, 1)
        conn_layout.addWidget(self.connect_btn)
        
        conn_group.setLayout(conn_layout)
        main_layout.addWidget(conn_group)
        
        # 2. Main Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setEnabled(False)
        main_layout.addWidget(self.tabs)
        
        # Tab 1: Group & User Management (Unified View)
        self.manage_tab = QWidget()
        self.setup_manage_tab()
        self.tabs.addTab(self.manage_tab, "组与用户管理")
        
        # Tab 2: Release & Upload
        self.release_tab = QWidget()
        self.setup_release_tab()
        self.tabs.addTab(self.release_tab, "发布与上传")
        
        # Tab 3: Auto Deploy
        self.deploy_tab = QWidget()
        self.setup_deploy_tab()
        self.tabs.addTab(self.deploy_tab, "自动化部署")

        # Initial Auto-Connect
        self.init_connection()

    def setup_manage_tab(self):
        layout = QHBoxLayout(self.manage_tab)
        
        # Left Panel: Group List
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("<b>用户组列表</b>"))
        
        self.group_list_widget = QListWidget()
        self.group_list_widget.currentItemChanged.connect(self.on_group_selected)
        left_layout.addWidget(self.group_list_widget)
        
        self.add_group_btn = QPushButton("新建组")
        self.add_group_btn.clicked.connect(self.create_group)
        left_layout.addWidget(self.add_group_btn)
        
        layout.addWidget(left_panel, 1)
        
        # Right Panel: Group Details & Users
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Group Details Header
        self.group_info_group = QGroupBox("组信息")
        info_layout = QGridLayout()
        
        self.lbl_group_name = QLabel("-")
        self.lbl_group_version = QLabel("-")
        self.lbl_group_comment = QLabel("-")
        
        self.btn_edit_comment = QPushButton("修改备注")
        self.btn_edit_comment.clicked.connect(self.edit_group_comment)
        
        info_layout.addWidget(QLabel("名称:"), 0, 0)
        info_layout.addWidget(self.lbl_group_name, 0, 1)
        info_layout.addWidget(QLabel("当前版本:"), 1, 0)
        info_layout.addWidget(self.lbl_group_version, 1, 1)
        info_layout.addWidget(QLabel("备注:"), 2, 0)
        info_layout.addWidget(self.lbl_group_comment, 2, 1)
        info_layout.addWidget(self.btn_edit_comment, 2, 2)
        
        self.group_info_group.setLayout(info_layout)
        right_layout.addWidget(self.group_info_group)
        
        # User List
        right_layout.addWidget(QLabel("<b>组内用户</b>"))
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "用户名", "权限", "操作"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_layout.addWidget(self.user_table)
        
        # Batch Actions
        action_layout = QHBoxLayout()
        self.btn_move_user = QPushButton("移动用户到其他组...")
        self.btn_move_user.clicked.connect(self.move_selected_user)
        self.btn_change_perm = QPushButton("修改用户权限...")
        self.btn_change_perm.clicked.connect(self.change_user_perm)
        
        action_layout.addWidget(self.btn_move_user)
        action_layout.addWidget(self.btn_change_perm)
        action_layout.addStretch()
        right_layout.addLayout(action_layout)
        
        layout.addWidget(right_panel, 3)

    def setup_release_tab(self):
        layout = QVBoxLayout(self.release_tab)
        
        # Section 1: Upload
        upload_group = QGroupBox("1. 上传新版本 (ZIP)")
        upload_layout = QHBoxLayout()
        
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.browse_file)
        self.upload_btn = QPushButton("上传")
        self.upload_btn.clicked.connect(self.upload_file)
        
        upload_layout.addWidget(self.file_path_edit)
        upload_layout.addWidget(self.browse_btn)
        upload_layout.addWidget(self.upload_btn)
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # Section 2: Archives List (New)
        archives_group = QGroupBox("2. 历史版本列表")
        archives_layout = QVBoxLayout()
        
        self.archives_list_widget = QListWidget()
        self.archives_list_widget.currentItemChanged.connect(self.on_archive_selected)
        archives_layout.addWidget(self.archives_list_widget)
        
        archives_group.setLayout(archives_layout)
        layout.addWidget(archives_group)

        # Section 3: Assign
        assign_group = QGroupBox("3. 分配版本给用户组")
        assign_layout = QFormLayout()
        
        self.uploaded_filename_label = QLabel("无")
        self.uploaded_filename_label.setStyleSheet("font-weight: bold; color: blue;")
        
        self.target_group_combo = QComboBox()
        self.assign_btn = QPushButton("更新组版本")
        self.assign_btn.clicked.connect(self.assign_version)
        
        assign_layout.addRow("选中版本:", self.uploaded_filename_label)
        assign_layout.addRow("目标组:", self.target_group_combo)
        assign_layout.addRow("", self.assign_btn)
        
        assign_group.setLayout(assign_layout)
        layout.addWidget(assign_group)
        
        #layout.addStretch() # remove stretch to let list expand
    
    def setup_deploy_tab(self):
        layout = QVBoxLayout(self.deploy_tab)
        
        # Section 1: 服务器配置
        server_group = QGroupBox("服务器配置")
        server_layout = QGridLayout()
        
        server_layout.addWidget(QLabel("服务器地址:"), 0, 0)
        self.deploy_host = QLineEdit("your-server.com")
        server_layout.addWidget(self.deploy_host, 0, 1)
        
        server_layout.addWidget(QLabel("SSH 端口:"), 0, 2)
        self.deploy_port = QLineEdit("22")
        server_layout.addWidget(self.deploy_port, 0, 3)
        
        server_layout.addWidget(QLabel("用户名:"), 1, 0)
        self.deploy_user = QLineEdit("root")
        server_layout.addWidget(self.deploy_user, 1, 1)
        
        server_layout.addWidget(QLabel("密码:"), 1, 2)
        self.deploy_password = QLineEdit()
        self.deploy_password.setEchoMode(QLineEdit.Password)
        server_layout.addWidget(self.deploy_password, 1, 3)
        
        server_layout.addWidget(QLabel("服务器路径:"), 2, 0)
        self.deploy_remote_path = QLineEdit("/var/www/DesignerCEP/Server/static")
        server_layout.addWidget(self.deploy_remote_path, 2, 1, 1, 3)
        
        btn_test_conn = QPushButton("测试连接")
        btn_test_conn.clicked.connect(self.test_ssh_connection)
        server_layout.addWidget(btn_test_conn, 3, 0)
        
        btn_save_config = QPushButton("保存配置")
        btn_save_config.clicked.connect(self.save_deploy_config)
        server_layout.addWidget(btn_save_config, 3, 1)
        
        btn_load_config = QPushButton("加载配置")
        btn_load_config.clicked.connect(self.load_deploy_config)
        server_layout.addWidget(btn_load_config, 3, 2)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # Section 2: 本地构建配置
        build_group = QGroupBox("本地构建配置")
        build_layout = QGridLayout()
        
        build_layout.addWidget(QLabel("项目根目录:"), 0, 0)
        self.deploy_project_root = QLineEdit(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        build_layout.addWidget(self.deploy_project_root, 0, 1)
        
        btn_browse_project = QPushButton("浏览...")
        btn_browse_project.clicked.connect(self.browse_project_root)
        build_layout.addWidget(btn_browse_project, 0, 2)
        
        build_layout.addWidget(QLabel("版本号:"), 1, 0)
        self.deploy_version = QLineEdit("1.0.0")
        build_layout.addWidget(self.deploy_version, 1, 1)
        
        build_group.setLayout(build_layout)
        layout.addWidget(build_group)
        
        # Section 3: 部署选项
        options_group = QGroupBox("部署选项")
        options_layout = QVBoxLayout()
        
        self.deploy_shell_check = QCheckBox("部署 Shell（在线登录页）")
        self.deploy_shell_check.setChecked(True)
        options_layout.addWidget(self.deploy_shell_check)
        
        self.deploy_core_check = QCheckBox("部署 Core（核心应用）")
        self.deploy_core_check.setChecked(True)
        options_layout.addWidget(self.deploy_core_check)
        
        self.deploy_shell_zip_check = QCheckBox("打包 Shell 为 .zip（供 CEP 扩展下载）")
        self.deploy_shell_zip_check.setChecked(True)
        options_layout.addWidget(self.deploy_shell_zip_check)
        
        self.deploy_build_check = QCheckBox("构建前端（npm run build）")
        self.deploy_build_check.setChecked(True)
        options_layout.addWidget(self.deploy_build_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Section 4: 部署按钮
        btn_layout = QHBoxLayout()
        
        self.btn_deploy_start = QPushButton("🚀 开始部署")
        self.btn_deploy_start.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_deploy_start.clicked.connect(self.start_deploy)
        btn_layout.addWidget(self.btn_deploy_start)
        
        self.btn_deploy_stop = QPushButton("⏹ 停止")
        self.btn_deploy_stop.setEnabled(False)
        btn_layout.addWidget(self.btn_deploy_stop)
        
        layout.addLayout(btn_layout)
        
        # Section 5: 进度条
        self.deploy_progress = QProgressBar()
        layout.addWidget(self.deploy_progress)
        
        # Section 6: 日志输出
        log_label = QLabel("部署日志:")
        layout.addWidget(log_label)
        
        self.deploy_log = QTextEdit()
        self.deploy_log.setReadOnly(True)
        self.deploy_log.setStyleSheet("background-color: #1E1E1E; color: #D4D4D4; font-family: Consolas, monospace;")
        layout.addWidget(self.deploy_log)
        
        # 加载配置
        self.load_deploy_config()

    def init_connection(self):
        url = self.url_edit.text()
        token = self.token_edit.text()
        self.api_client = ApiClient(url, token)
        
        try:
            self.refresh_all_data()
            self.tabs.setEnabled(True)
            self.statusBar().showMessage("连接成功", 3000)
        except Exception as e:
            QMessageBox.critical(self, "连接错误", str(e))
            self.tabs.setEnabled(False)

    def refresh_all_data(self):
        if not self.api_client: return
        try:
            self.groups_data = self.api_client.list_groups()
            self.users_data = self.api_client.list_users()
            self.archives_data = self.api_client.list_archives()
            self.update_ui_with_data()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"刷新数据失败: {e}")

    def update_ui_with_data(self):
        # Update Group List
        self.group_list_widget.clear()
        self.target_group_combo.clear()
        
        # 1. Add "Unassigned" pseudo-group
        unassigned_group = {
            'id': None,
            'name': '未分配组 (Unassigned)',
            'current_version_file': '-',
            'comment': '新注册或未分配的用户'
        }
        item_unassigned = QListWidgetItem(unassigned_group['name'])
        item_unassigned.setData(Qt.UserRole, unassigned_group)
        self.group_list_widget.addItem(item_unassigned)

        # 2. Add real groups
        for g in self.groups_data:
            item = QListWidgetItem(g['name'])
            item.setData(Qt.UserRole, g)
            self.group_list_widget.addItem(item)
            
            # Update Combo in Release Tab
            self.target_group_combo.addItem(g['name'], g['id'])
            
        # If there's a selection, refresh the user view, otherwise select first
        if self.group_list_widget.count() > 0:
             self.group_list_widget.setCurrentRow(0)

        # Update Archives List
        self.archives_list_widget.clear()
        for filename in self.archives_data:
            self.archives_list_widget.addItem(filename)

    def on_group_selected(self, current, previous):
        if not current: return
        group = current.data(Qt.UserRole)
        
        # Update Header
        self.lbl_group_name.setText(group['name'])
        self.lbl_group_version.setText(group['current_version_file'] or "无")
        self.lbl_group_comment.setText(group['comment'] or "无")
        
        # Filter Users
        if group['id'] is None:
            # Special handling for unassigned users
            group_users = [u for u in self.users_data if u['group_id'] is None]
        else:
            group_users = [u for u in self.users_data if u['group_id'] == group['id']]
            
        self.user_table.setRowCount(len(group_users))
        
        for i, u in enumerate(group_users):
            self.user_table.setItem(i, 0, QTableWidgetItem(str(u['id'])))
            self.user_table.setItem(i, 1, QTableWidgetItem(u['username']))
            self.user_table.setItem(i, 2, QTableWidgetItem(u['permissions'] or ""))
            # Store user object in first item
            self.user_table.item(i, 0).setData(Qt.UserRole, u)

    def on_archive_selected(self, current, previous):
        if not current: return
        filename = current.text()
        self.uploaded_filename_label.setText(filename)

    def create_group(self):
        dialog = CreateGroupDialog(self)
        if dialog.exec() == QDialog.Accepted:
            name, comment = dialog.get_data()
            if not name:
                QMessageBox.warning(self, "警告", "组名称必填")
                return
            try:
                self.api_client.create_group(name, comment)
                self.refresh_all_data()
                QMessageBox.information(self, "成功", f"组 '{name}' 创建成功!")
            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))

    def edit_group_comment(self):
        item = self.group_list_widget.currentItem()
        if not item: return
        group = item.data(Qt.UserRole)
        
        text, ok = QInputDialog.getText(self, "修改备注", "请输入新备注:", text=group['comment'])
        if ok:
            try:
                self.api_client.update_group_comment(group['id'], text)
                self.refresh_all_data()
            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))

    def move_selected_user(self):
        row = self.user_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "警告", "请先在列表中选择一个用户")
            return
            
        user = self.user_table.item(row, 0).data(Qt.UserRole)
        
        # Create a simple dialog with combo box
        dialog = QDialog(self)
        dialog.setWindowTitle("移动用户")
        layout = QVBoxLayout(dialog)
        combo = QComboBox()
        for g in self.groups_data:
            if g['id'] != user['group_id']:
                combo.addItem(g['name'], g['id'])
                
        layout.addWidget(QLabel(f"将用户 {user['username']} 移动到:"))
        layout.addWidget(combo)
        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addWidget(btns)
        
        if dialog.exec() == QDialog.Accepted:
            new_group_id = combo.currentData()
            if new_group_id:
                try:
                    self.api_client.update_user_group(user['id'], new_group_id)
                    self.refresh_all_data()
                    QMessageBox.information(self, "成功", "用户移动成功")
                except Exception as e:
                    QMessageBox.critical(self, "错误", str(e))

    def change_user_perm(self):
        row = self.user_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "警告", "请先在列表中选择一个用户")
            return
        
        user = self.user_table.item(row, 0).data(Qt.UserRole)
        text, ok = QInputDialog.getText(self, "修改权限", "输入权限 (逗号分隔):", text=user['permissions'] or "")
        if ok:
            try:
                self.api_client.update_user_permissions(user['id'], text)
                self.refresh_all_data()
            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))

    def browse_file(self):
        # Allow selecting either file or directory
        # QFileDialog doesn't easily support both at once, so we'll use directory for now as requested
        # Or we can add a second button. 
        # User asked to "change to folder", implies preferring folder selection.
        
        # Let's support both but via directory selector if user wants to zip folder, 
        # or maybe we can just use getExistingDirectory.
        
        # Better approach: Add a choice or just use getExistingDirectory since user asked for folder support.
        # But if they select a zip file, they can't.
        # Let's add a "Browse Folder..." logic or modify existing.
        
        # User said: "Change to folder... and auto zip".
        # I will change the dialog to getExistingDirectory.
        
        path = QFileDialog.getExistingDirectory(self, "选择发布文件夹 (自动压缩)")
        if path:
            self.file_path_edit.setText(path)

    def upload_file(self):
        path = self.file_path_edit.text()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "警告", "请先选择有效的路径。")
            return
        
        try:
            self.upload_btn.setEnabled(False)
            self.upload_btn.setText("处理中...")
            QApplication.processEvents()
            
            final_file_path = path
            
            # If directory, zip it first
            if os.path.isdir(path):
                self.upload_btn.setText("正在压缩...")
                QApplication.processEvents()
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = os.path.basename(os.path.abspath(path))
                zip_filename = f"{base_name}_{timestamp}.zip"
                # Create zip in temp or current dir? Current dir is safer/easier to debug
                # Or better, use a temporary file to avoid clutter
                
                # Exclude patterns
                def zip_directory(source_dir, output_filename):
                    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(source_dir):
                            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'dist', 'archives', '__pycache__']]
                            for file in files:
                                if file == output_filename or file.endswith('.zip') or file.endswith('.pyc'):
                                    continue
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, source_dir)
                                zipf.write(file_path, arcname)
                
                zip_directory(path, zip_filename)
                final_file_path = zip_filename
                
            self.upload_btn.setText("正在上传...")
            QApplication.processEvents()
            
            filename = self.api_client.upload_version(final_file_path)
            
            # If we created a zip, maybe delete it or keep it?
            # User might want to keep local backup. I'll keep it for now but log it.
            
            QMessageBox.information(self, "成功", f"上传成功: {filename}")
            self.refresh_all_data()
        except Exception as e:
            QMessageBox.critical(self, "上传错误", str(e))
        finally:
            self.upload_btn.setEnabled(True)
            self.upload_btn.setText("上传")

    def assign_version(self):
        filename = self.uploaded_filename_label.text()
        if filename == "无" or not filename:
            QMessageBox.warning(self, "警告", "请先上传文件。")
            return
        
        group_id = self.target_group_combo.currentData()
        if group_id is None:
            QMessageBox.warning(self, "警告", "请选择目标组。")
            return
            
        try:
            self.api_client.update_group_version(group_id, filename)
            self.refresh_all_data()
            QMessageBox.information(self, "成功", f"组版本已更新为 {filename}")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
    
    # ==================== 部署相关方法 ====================
    
    def save_deploy_config(self):
        """保存部署配置到本地文件"""
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'deploy_config.txt')
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(f"host={self.deploy_host.text()}\n")
                f.write(f"port={self.deploy_port.text()}\n")
                f.write(f"user={self.deploy_user.text()}\n")
                f.write(f"password={self.deploy_password.text()}\n")
                f.write(f"remote_path={self.deploy_remote_path.text()}\n")
                f.write(f"project_root={self.deploy_project_root.text()}\n")
                f.write(f"version={self.deploy_version.text()}\n")
            QMessageBox.information(self, "成功", "配置已保存")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置失败: {e}")
    
    def load_deploy_config(self):
        """从本地文件加载部署配置"""
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'deploy_config.txt')
            if not os.path.exists(config_file):
                return
            
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key == 'host':
                            self.deploy_host.setText(value)
                        elif key == 'port':
                            self.deploy_port.setText(value)
                        elif key == 'user':
                            self.deploy_user.setText(value)
                        elif key == 'password':
                            self.deploy_password.setText(value)
                        elif key == 'remote_path':
                            self.deploy_remote_path.setText(value)
                        elif key == 'project_root':
                            self.deploy_project_root.setText(value)
                        elif key == 'version':
                            self.deploy_version.setText(value)
        except Exception as e:
            self.log_deploy(f"加载配置失败: {e}")
    
    def browse_project_root(self):
        """浏览项目根目录"""
        path = QFileDialog.getExistingDirectory(self, "选择项目根目录")
        if path:
            self.deploy_project_root.setText(path)
    
    def test_ssh_connection(self):
        """测试 SSH 连接"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.log_deploy("正在测试 SSH 连接...")
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=10
            )
            
            stdin, stdout, stderr = ssh.exec_command('pwd')
            remote_pwd = stdout.read().decode().strip()
            
            ssh.close()
            
            QMessageBox.information(self, "连接成功", f"SSH 连接测试成功！\n当前目录: {remote_pwd}")
            self.log_deploy(f"✅ SSH 连接成功，当前目录: {remote_pwd}")
        except Exception as e:
            QMessageBox.critical(self, "连接失败", f"SSH 连接测试失败:\n{str(e)}")
            self.log_deploy(f"❌ SSH 连接失败: {e}")
    
    def log_deploy(self, message):
        """添加部署日志"""
        self.deploy_log.append(message)
        QApplication.processEvents()
    
    def start_deploy(self):
        """开始部署流程"""
        # 验证配置
        if not self.deploy_host.text() or not self.deploy_user.text():
            QMessageBox.warning(self, "配置不完整", "请先配置服务器信息")
            return
        
        if not os.path.exists(self.deploy_project_root.text()):
            QMessageBox.warning(self, "路径错误", "项目根目录不存在")
            return
        
        # 确认部署
        reply = QMessageBox.question(
            self, 
            '确认部署', 
            f"即将部署到服务器: {self.deploy_host.text()}\n\n"
            f"部署项目:\n"
            f"{'✅ Shell（在线登录页）' if self.deploy_shell_check.isChecked() else '⬜ Shell'}\n"
            f"{'✅ Core（核心应用）' if self.deploy_core_check.isChecked() else '⬜ Core'}\n"
            f"{'✅ Shell.zip（下载包）' if self.deploy_shell_zip_check.isChecked() else '⬜ Shell.zip'}\n\n"
            f"是否继续？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # 禁用按钮
        self.btn_deploy_start.setEnabled(False)
        self.btn_deploy_stop.setEnabled(True)
        self.deploy_progress.setValue(0)
        self.deploy_log.clear()
        
        try:
            self.run_deploy()
        except Exception as e:
            QMessageBox.critical(self, "部署失败", str(e))
            self.log_deploy(f"\n❌ 部署失败: {e}")
        finally:
            self.btn_deploy_start.setEnabled(True)
            self.btn_deploy_stop.setEnabled(False)
            self.deploy_progress.setValue(100)
    
    def run_deploy(self):
        """执行部署流程"""
        project_root = self.deploy_project_root.text()
        designer_path = os.path.join(project_root, 'Designer')
        version = self.deploy_version.text()
        
        self.log_deploy("="*60)
        self.log_deploy("🚀 开始自动化部署流程")
        self.log_deploy("="*60)
        
        # Step 1: 构建前端
        if self.deploy_build_check.isChecked():
            self.log_deploy("\n📦 步骤 1/5: 构建前端...")
            self.deploy_progress.setValue(10)
            
            try:
                self.log_deploy(f"执行: cd {designer_path} && npm run build")
                result = subprocess.run(
                    'npm run build',
                    cwd=designer_path,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    self.log_deploy("✅ 前端构建成功")
                else:
                    self.log_deploy(f"❌ 构建失败: {result.stderr}")
                    raise Exception("前端构建失败")
            except subprocess.TimeoutExpired:
                raise Exception("构建超时（5分钟）")
        else:
            self.log_deploy("\n⏭ 跳过前端构建")
            self.deploy_progress.setValue(10)
        
        # Step 2: 连接 SSH
        self.log_deploy("\n🔐 步骤 2/5: 连接服务器...")
        self.deploy_progress.setValue(30)
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(
                hostname=self.deploy_host.text(),
                port=int(self.deploy_port.text()),
                username=self.deploy_user.text(),
                password=self.deploy_password.text(),
                timeout=30
            )
            self.log_deploy("✅ SSH 连接成功")
        except Exception as e:
            raise Exception(f"SSH 连接失败: {e}")
        
        # Step 3: 创建服务器目录
        self.log_deploy("\n📁 步骤 3/5: 创建服务器目录...")
        self.deploy_progress.setValue(40)
        
        remote_path = self.deploy_remote_path.text()
        commands = [
            f"mkdir -p {remote_path}/shell",
            f"mkdir -p {remote_path}/core/{version}",
            f"mkdir -p {remote_path}/downloads"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()
        
        self.log_deploy("✅ 目录创建完成")
        
        # Step 4: 上传文件
        self.log_deploy("\n📤 步骤 4/5: 上传文件到服务器...")
        self.deploy_progress.setValue(50)
        
        sftp = ssh.open_sftp()
        dist_path = os.path.join(designer_path, 'dist')
        
        try:
            # 上传 Shell
            if self.deploy_shell_check.isChecked():
                self.log_deploy("  上传 Shell（在线登录页）...")
                shell_src = os.path.join(dist_path, 'Shell')
                shell_dst = f"{remote_path}/shell"
                self._upload_directory(sftp, shell_src, shell_dst)
                self.log_deploy("  ✅ Shell 上传完成")
            
            self.deploy_progress.setValue(60)
            
            # 上传 Core
            if self.deploy_core_check.isChecked():
                self.log_deploy("  上传 Core（核心应用）...")
                core_src = os.path.join(dist_path, 'Designer')
                core_dst = f"{remote_path}/core/{version}"
                self._upload_directory(sftp, core_src, core_dst)
                self.log_deploy("  ✅ Core 上传完成")
            
            self.deploy_progress.setValue(80)
            
            # 打包并上传 Shell.zip
            if self.deploy_shell_zip_check.isChecked():
                self.log_deploy("  打包 Shell.zip（供 CEP 扩展下载）...")
                shell_src = os.path.join(dist_path, 'Shell')
                zip_filename = f"shell-{version}.zip"
                zip_path = os.path.join(dist_path, zip_filename)
                
                # 创建 ZIP
                import zipfile
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(shell_src):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, shell_src)
                            zipf.write(file_path, arcname)
                
                # 上传 ZIP
                remote_zip = f"{remote_path}/downloads/{zip_filename}"
                sftp.put(zip_path, remote_zip)
                self.log_deploy(f"  ✅ Shell.zip 上传完成: {zip_filename}")
                
                # 删除本地 ZIP
                os.remove(zip_path)
            
        finally:
            sftp.close()
        
        self.deploy_progress.setValue(90)
        
        # Step 5: 验证部署
        self.log_deploy("\n✅ 步骤 5/5: 验证部署...")
        
        commands_verify = []
        if self.deploy_shell_check.isChecked():
            commands_verify.append(f"ls {remote_path}/shell/index.html")
        if self.deploy_core_check.isChecked():
            commands_verify.append(f"ls {remote_path}/core/{version}/index.html")
        if self.deploy_shell_zip_check.isChecked():
            commands_verify.append(f"ls {remote_path}/downloads/shell-{version}.zip")
        
        for cmd in commands_verify:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_code = stdout.channel.recv_exit_status()
            if exit_code != 0:
                self.log_deploy(f"  ⚠️ 验证失败: {cmd}")
        
        ssh.close()
        
        self.deploy_progress.setValue(100)
        self.log_deploy("\n" + "="*60)
        self.log_deploy("🎉 部署完成!")
        self.log_deploy("="*60)
        self.log_deploy(f"\n访问地址:")
        if self.deploy_shell_check.isChecked():
            self.log_deploy(f"  Shell: https://{self.deploy_host.text()}/shell/")
        if self.deploy_core_check.isChecked():
            self.log_deploy(f"  Core:  https://{self.deploy_host.text()}/core/{version}/")
        if self.deploy_shell_zip_check.isChecked():
            self.log_deploy(f"  下载:  https://{self.deploy_host.text()}/downloads/shell-{version}.zip")
        
        QMessageBox.information(self, "部署成功", f"部署完成！\n版本: {version}")
    
    def _upload_directory(self, sftp, local_dir, remote_dir):
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
                self.log_deploy(f"    → {item}")
                sftp.put(local_path, remote_path)
            elif os.path.isdir(local_path):
                self._upload_directory(sftp, local_path, remote_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())
